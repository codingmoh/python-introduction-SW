"""Execute notebooks in fresh kernels and optionally render a local HTML handout."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def rewrite_links(body: str, source: Path, rendered_notebooks: set[Path]) -> str:
    """Link local notebook reading copies together and other source files to GitHub."""
    def replace(match: re.Match[str]) -> str:
        url = urlsplit(html.unescape(match.group(1)))
        if url.scheme or url.netloc or not url.path:
            return match.group(0)
        target = (source.parent / unquote(url.path)).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            return match.group(0)
        if target.suffix == ".ipynb" and target in rendered_notebooks:
            address = urlunsplit(("", "", url.path.removesuffix(".ipynb") + ".html", url.query, url.fragment))
        else:
            address = "https://github.com/codingmoh/python-introduction-SW/blob/main/" + quote(target.relative_to(ROOT).as_posix())
            if url.fragment:
                address += "#" + url.fragment
        return 'href="' + html.escape(address, quote=True) + '"'

    return re.sub(r'href="([^"]*)"', replace, body)


def check_notebook(
    path: Path, output_root: Path, render_html: bool, rendered_notebooks: set[Path]
) -> None:
    """Keep submitted notebooks intact; write executed copies under build/."""
    relative = path.relative_to(ROOT)
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    kernel = KernelManager(kernel_name="python3")
    # Use the environment that launched this command, even if another kernel is installed.
    kernel.kernel_spec.argv = [
        sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"
    ]
    NotebookClient(
        notebook,
        km=kernel,
        timeout=60,
        allow_errors=False,
        record_timing=False,
        resources={"metadata": {"path": str(path.parent)}},
    ).execute(cleanup_kc=True)
    errors = [
        output
        for cell in notebook.cells
        for output in cell.get("outputs", [])
        if output.output_type == "error"
    ]
    if errors:
        raise RuntimeError(f"Unexpected error output in {relative}")
    target = output_root / "executed" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, target)

    if render_html:
        from nbconvert import HTMLExporter

        exporter = HTMLExporter(template_name="lab")
        exporter.embed_images = True
        body, _ = exporter.from_notebook_node(
            notebook,
            resources={"metadata": {"name": path.stem, "path": str(path.parent)}},
        )
        target = output_root / "html" / relative.with_suffix(".html")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rewrite_links(body, path, rendered_notebooks), encoding="utf-8")
    print(f"PASS {relative}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Specific notebook paths")
    parser.add_argument("--html", action="store_true", help="Also render executed HTML")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "build")
    args = parser.parse_args()
    paths = (
        [path.resolve() for path in args.paths]
        if args.paths
        else sorted(ROOT.glob("notebooks/*.ipynb")) + sorted(ROOT.glob("solutions/*.ipynb"))
    )
    if not paths:
        parser.error("No notebooks found")
    # Partial exports retain earlier pages and link other notebooks to their source.
    rendered_notebooks = set(paths) | {
        ROOT / page.relative_to(args.output_dir / "html").with_suffix(".ipynb")
        for folder in ("notebooks", "solutions")
        for page in (args.output_dir / "html" / folder).glob("*.html")
    }
    for path in paths:
        check_notebook(path, args.output_dir, args.html, rendered_notebooks)
    if args.html:
        entries = []
        pages = sorted((args.output_dir / "html" / "notebooks").glob("*.html"))
        pages += sorted((args.output_dir / "html" / "solutions").glob("*.html"))
        for page in pages:
            relative = page.relative_to(args.output_dir / "html")
            label = page.stem.replace("_", " ")
            entries.append(f'<li><a href="{html.escape(relative.as_posix())}">{html.escape(label)}</a></li>')
        index = args.output_dir / "html" / "index.html"
        index.write_text(
            '<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Python introduction: executed notebooks</title>'
            '<style>body{font:18px/1.6 system-ui;max-width:850px;margin:4rem auto;padding:0 1.5rem}'
            'li{margin:.5rem 0}a{color:#1257a6}</style>'
            '<h1>Python introduction</h1><p>Executed examples and optional exercise solutions.</p><ul>'
            + "".join(entries) + "</ul></html>",
            encoding="utf-8",
        )
        print(f"HTML index: {index}")
    print(f"All {len(paths)} notebooks executed successfully.")


if __name__ == "__main__":
    main()

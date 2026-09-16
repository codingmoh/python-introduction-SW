"""Runnable chapter 02 examples: object references, text, and safe local files.

Run with ``uv run examples/02_fundamentals.py``. Importing this file defines
functions without running the demonstration or creating files.
"""

from pathlib import Path
from tempfile import TemporaryDirectory


def combine_and_repeat(a, b, count):
    """Add a and b, then multiply/repeat the result by count.

    The supplied objects must support these operations; incompatible types raise
    their ordinary TypeError. Strings and lists repeat, while numbers multiply.
    """
    return (a + b) * count


def normalize_words(text: str) -> str:
    """Collapse whitespace and case-fold words; preserve punctuation."""
    normalized = []
    for word in text.split():
        normalized.append(word.casefold())
    return " ".join(normalized)


def format_report_row(name: str, count: int, mean: float) -> str:
    """Format a name, count, and mean using minimum widths and two decimals."""
    return f"{name:<10} | {count:>4} | {mean:7.2f}"


def write_notes(path: str | Path, notes: list[str]) -> None:
    """Replace a UTF-8 file with one newline-ended line per note.

    Each note must be a string without embedded newline characters. Empty notes
    and surrounding spaces are preserved. The containing directory must exist.
    """
    with Path(path).open("w", encoding="utf-8") as stream:
        for note in notes:
            stream.write(note + "\n")


def read_notes(path: str | Path) -> list[str]:
    """Return UTF-8 lines without their terminal newline; preserve other spaces.

    Missing files raise FileNotFoundError. A final unterminated line is retained.
    Python's default universal-newline reading normalizes common line endings.
    """
    with Path(path).open("r", encoding="utf-8") as stream:
        return [line.removesuffix("\n") for line in stream]


def main() -> None:
    """Show shared references, polymorphic operations, text, and cleanup."""
    original = [["red"], ["blue"]]
    alias = original
    shallow = original.copy()
    shallow[0].append("green")
    shallow.append(["black"])
    print("Alias identity:", alias is original)
    print("Shared inner list:", shallow[0] is original[0])
    print("Original:", original, "shallow copy:", shallow)
    print("Number operations:", combine_and_repeat(2, 3, 4))
    print("Text operations:", combine_and_repeat("py", "thon", 2))
    print("Normalized:", normalize_words("  PYTHON\t Straße \n"))
    print(format_report_row("sample", 3, 2.5))

    with TemporaryDirectory(prefix="python-notes-") as directory:
        path = Path(directory) / "notes.txt"
        notes = ["Grüße", "  keep spaces  ", ""]
        write_notes(path, notes)
        restored = read_notes(path)
        assert restored == notes
        print("Restored notes:", restored)
        try:
            with path.open(encoding="utf-8") as stream:
                content = stream.read()
                raise ValueError("Deliberate demonstration error")
        except ValueError:
            print("File closed after the expected error:", stream.closed)
        print("Content is still in scope:", repr(content))
    print("Temporary file removed:", not path.exists())


if __name__ == "__main__":
    main()

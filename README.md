# Python Introduction SW

Learn Python by running small examples, changing them, and solving exercises. This repository follows six course slide decks: introduction, fundamentals, data structures, functions, object-oriented programming, and functional programming.

The material contains seven learning notebooks, 36 exercises, six separate solution notebooks, and six standalone Python scripts. All explanations are in English and written for students. Examples use the Python standard library. They run locally without accounts, API keys, downloaded datasets, or a database.

## Start here

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run these commands in a terminal:

```bash
git clone https://github.com/codingmoh/python-introduction-SW.git
cd python-introduction-SW
uv sync --locked
uv run --locked jupyter lab
```

This is a private repository: cloning requires access and GitHub authentication. You can also download its ZIP from GitHub, extract it, and open a terminal in the extracted folder.

`uv` creates a project environment in `.venv`. The course uses Python 3.13; `.python-version` pins the tested 3.13.15 patch release and `uv.lock` records the package versions. Use a current version of `uv` so it can download the pinned Python interpreter when needed. Installation needs internet access; the lesson examples run offline afterwards.

JupyterLab opens in your browser. Open **[00 Getting started](notebooks/00_getting_started.ipynb)**, select the Python 3 kernel, and execute cells with **Shift+Enter**. Keep the server terminal open. Stop Jupyter with **Ctrl+C** in that terminal when finished.

If you use VS Code instead, install its Python and Jupyter extensions and select this repository's `.venv` as the notebook kernel. The running kernel matters: opening the right folder does not automatically change an already running kernel.

## Learning path

For a demonstration alongside the slides, open **[Live coding](notebooks/live_coding.ipynb)**. This is one workspace covering all six PDFs, with 46 short coding stops. Each stop shows exactly when to switch from the slides, where to resume, and a mostly blank cell for typing the implementation. A few cells include small sample inputs. Chapter and stop links let you jump directly to a topic; each stop is independent of previous cells.

Save a working copy before the session. The **[matching reference](solutions/live_coding_reference.ipynb)** has the same stop IDs and cell order with completed, tested code. Keep it in a separate tab as a fallback. The live workspace contains no completed implementations or speaker script; its unchanged Run All checks only the starter cells.

| Chapter | Main ideas | Practice |
| --- | --- | --- |
| [00 Getting started](notebooks/00_getting_started.ipynb) | Cells, kernels, execution order, errors, reproducible runs | Run, edit, restart |
| [01 Introduction](notebooks/01_introduction.ipynb) | Values, variables, arithmetic, strings, decisions, loops | [Example script](examples/01_introduction.py) · [Solutions](solutions/01_introduction_solutions.ipynb) |
| [02 Fundamentals](notebooks/02_fundamentals.ipynb) | Objects, references, identity, strings, files, modules, environments | [Example script](examples/02_fundamentals.py) · [Solutions](solutions/02_fundamentals_solutions.ipynb) |
| [03 Data structures](notebooks/03_data_structures.ipynb) | Lists, tuples, dictionaries, sets, comprehensions | [Example script](examples/03_data_structures.py) · [Solutions](solutions/03_data_structures_solutions.ipynb) |
| [04 Functions](notebooks/04_functions.ipynb) | Return values, scope, defaults, arguments, documentation | [Example script](examples/04_functions.py) · [Solutions](solutions/04_functions_solutions.ipynb) |
| [05 Object-oriented programming](notebooks/05_oop.ipynb) | Classes, methods, inheritance, protocols, exceptions | [Example script](examples/05_oop.py) · [Solutions](solutions/05_oop_solutions.ipynb) |
| [06 Functional programming](notebooks/06_functional_programming.ipynb) | Pure functions, map/filter, iterators, generators, decorators | [Example script](examples/06_functional_programming.py) · [Solutions](solutions/06_functional_programming_solutions.ipynb) |

The chapter numbers follow the supplied files. Each notebook is self-contained: start its kernel fresh and work from top to bottom. Functions are useful prerequisites for both chapters 05 and 06. The OOP slides' opening functional-programming recap is explained briefly and connected to chapter 06.

## How to practise

1. Predict what a code cell will do before running it.
2. Run it and compare the output with your prediction.
3. Change one value or condition and run the relevant cells again.
4. Complete the exercise cells, marked with `TODO` and the `exercise` tag.
5. Compare with the separate solution notebook after trying the problem yourself.
6. Use **Restart Kernel and Run All Cells** to check that your result does not depend on hidden state.

Exercise starters deliberately do not fail before you implement them. A successful Run All of the unchanged lesson therefore checks the examples, **not completion of the exercises**. Solution notebooks contain worked reasoning and executable checks, including boundary cases. They are accessible to anyone who can read this repository.

Expected error demonstrations catch the specific error and explain it. No notebook waits for keyboard input during Run All. Optional `input()` examples are shown as text so they can be tried manually. File examples use temporary directories and do not overwrite personal files.

## Run a Python script

From the repository root:

```bash
uv run --locked python examples/01_introduction.py
```

Replace the filename to run another chapter's script. These are compact, standalone applications of the notebook concepts. They complement the longer notebook explanations.

## Check everything

```bash
uv run --locked python -m unittest discover -s tests -v
uv run --locked python tools/check_notebooks.py
```

The first command checks the example scripts' behavior. The second executes every lesson and solution notebook in a separate, fresh kernel using the project environment. Executed copies go to `build/executed/`; the editable notebooks stay unchanged. GitHub Actions runs both checks on pushes and pull requests.

To create browser-readable handouts with computed outputs:

```bash
uv run --locked python tools/check_notebooks.py --html
```

Open `build/html/index.html`. HTML files are reading copies: edit and execute the `.ipynb` files in Jupyter to do the exercises. The build directory is excluded from Git.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `uv` is not found | Complete the installation and reopen your terminal. |
| A package cannot be imported | Run `uv sync --locked` in this folder and select its `.venv` kernel. |
| A name is not defined | Run the earlier definition cell, or restart and run the notebook in order. |
| The output does not match the visible code | Re-execute the cell; saved output may be stale. |
| A cell keeps running | Interrupt the kernel. Check loop conditions before running it again. |
| `input()` waits during your own experiment | Enter a value, or interrupt. Automated examples avoid interactive input. |
| Changes disappear after restarting | A restart clears Python memory; save code in cells or a `.py` file. |

## Relationship to the slides

The [source map](docs/source_map.md) connects the six source PDFs and page ranges to notebook sections. Repeated slide material is consolidated, historical setup advice is updated, and incorrect or simplified claims are clarified with runnable examples. SQLAlchemy is outside this repository's scope.

The notebooks and scripts are newly written companions, not a verbatim slide transcription. The original PDFs are not required to run the project and are not redistributed here. Consult your course's slide copies for the original illustrations and attribution.

References: [Python tutorial](https://docs.python.org/3.13/tutorial/), [uv project guide](https://docs.astral.sh/uv/guides/projects/), [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/).

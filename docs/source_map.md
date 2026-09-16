# Source map and updated explanations

These notebooks are new, executable companions to six supplied course slide decks. Their numbering follows the files. The six PDFs contain 357 pages in total, including title pages and repeated recap material. The mapping below consolidates repeated examples while retaining the distinct concepts and practice topics.

Page numbers refer to the PDF page position, starting at 1. The original PDFs remain in the course's source collection and are not required by the code. `7_alchemy_merged.pdf` is explicitly excluded; there is no SQLAlchemy chapter or dependency.

## 01 Introduction — 51 pages

Source: `1_introduction_python.pdf` → [01 Introduction](../notebooks/01_introduction.ipynb)

| PDF pages | Notebook coverage |
| --- | --- |
| 1–11 | Python's readability goals, hello world, comments and multiline strings |
| 12–19 | Variables, object types, numbers, arithmetic and booleans |
| 20–27 | Unicode strings, indexing, negative indices, slicing and conversions |
| 28–34 | Lists, nested collections, mutation and sequence operations |
| 35–42 | Console input/output, indentation, conditions, palindrome checking and truth values |
| 43–46 | `for`, `range`, `break` and `continue` |
| 47–51 | Functions, return values, prime checking and a bridge to chapter 04 |

## 02 Fundamentals — 65 pages

Source: `2_python_fundamentals.pdf` → [02 Fundamentals](../notebooks/02_fundamentals.ipynb)

| PDF pages | Notebook coverage |
| --- | --- |
| 1–23 | Recap of values, control flow and functions; cross-links to chapter 01 |
| 24–33 | Objects, names, namespaces, identity and shared references |
| 34–41 | Duck typing and the difference between `is` and `==` |
| 42–49 | Escapes, string operations, split/join and three formatting styles |
| 50–53 | Text files, modes, paths, encodings and context-managed cleanup |
| 54–56 | Scripts, modules and imports |
| 57–65 | Isolated environments and installing/running with the selected interpreter |

The [getting-started notebook](../notebooks/00_getting_started.ipynb) supplies the practical Jupyter and environment workflow used across all chapters.

## 03 Data structures — 54 pages

Source: `3_data_structures.pdf` → [03 Data structures](../notebooks/03_data_structures.ipynb)

| PDF pages | Notebook coverage |
| --- | --- |
| 1–11 | List creation, indexing, slicing, mutation, methods and nested values |
| 12–22 | Tuples, immutability, hashability, packing/unpacking, swapping, Fibonacci updates and enumeration |
| 23–30 | Dictionary keys, lookup, defaults, update/delete and views |
| 31–39 | Sets, unique values, membership, set algebra and allowed-character validation |
| 40–44 | `items`, `zip`, `reversed` and `sorted` |
| 45–54 | List, dictionary and set comprehensions; filtering and transformations |

## 04 Functions — 48 pages

Source: `4_functions.pdf` → [04 Functions](../notebooks/04_functions.ipynb)

| PDF pages | Notebook coverage |
| --- | --- |
| 1–11 | Definition, return/`None`, local scope, LEGB and object sharing |
| 12–21 | Defaults, positional/keyword calls and invalid-call examples |
| 22–30 | `*args`, `**kwargs` and unpacking calls |
| 31–37 | String formatting with arguments and combined parameter signatures |
| 38–42 | Docstrings, naming, indentation and readable function style |
| 43–48 | Function objects, aliases, attributes and passing functions as values |

## 05 Object-oriented programming — 89 pages

Source: `5_oop.pdf` → [05 OOP](../notebooks/05_oop.ipynb)

| PDF pages | Notebook coverage |
| --- | --- |
| 1–13 | Programming paradigms, objects and names; a short FP bridge to chapter 06 |
| 14–32 | Class and instance objects, attributes, instantiation and initialization |
| 33–37 | Bound methods, `self` and a stateful example |
| 38–45 | Class attributes, instance attributes and shared mutable state traps |
| 46–49 | Public interfaces, underscore conventions and naming style |
| 50–56 | Inheritance, overriding, `super`, multiple inheritance and C3 MRO |
| 57–62 | Dunder methods, object representations, operators and container protocols |
| 63–75 | Syntax/runtime errors, exception hierarchy, specific handlers and finite retries |
| 76–85 | Raising and custom exceptions, `else`, EAFP and LBYL |
| 86–89 | `finally`, resource cleanup and context managers |

The OOP slides begin with a recap of functional programming. The notebooks retain the supplied file order and introduce the needed idea briefly; chapter 06 provides its complete treatment. Neither notebook requires variables or definitions from another kernel.

## 06 Functional programming — 50 pages

Source: `6_FP.pdf` → [06 Functional programming](../notebooks/06_functional_programming.ipynb)

| PDF pages | Notebook coverage |
| --- | --- |
| 1–7 | Paradigms, pure functions, explicit state and side effects |
| 8–18 | Mapping/filtering, comprehensions and lazy consumption |
| 19–24 | Lambda expressions and appropriate uses |
| 25–30 | Iterables, iterators, `iter`, `next` and exhaustion |
| 31–34 | Generator expressions, short-circuiting and consumption |
| 35–42 | Generator functions, `yield`, bounded Fibonacci consumption and streaming |
| 43–45 | Higher-order functions and closures |
| 46–50 | Decorators, argument forwarding, returned values, metadata and caching |

## Clarifications for modern Python

| Historical or simplified claim | Explanation used here |
| --- | --- |
| Install Python 3.4 or rely on a preinstalled Python 2 | Use the project's pinned Python 3.13 environment and locked Jupyter dependencies. |
| A variable has a fixed storage box/type | Names bind to objects; the objects carry their types. Rebinding is different from mutation. |
| `id()` is always a memory address | It is an identity value, stable during the object's lifetime; implementation details are not a language guarantee. |
| Identity comparisons can replace equality | Use `==` for values and `is` for identity, including the usual `is None` check. |
| A tuple is always hashable | Every element must be hashable; a tuple containing a list is not a dictionary key. |
| Dictionaries are unordered | Modern dictionaries preserve insertion order; sets do not promise a useful iteration order. |
| `dict.popitem()` removes an arbitrary pair | Modern dictionaries remove the last inserted pair. |
| Set membership is simply O(1) | Constant time is an average-case expectation for hash-based lookup, not a worst-case guarantee. |
| Only functions create scope | Modules, class bodies and comprehensions also have relevant namespace/scope rules; a normal `if` or `for` block does not create a function-like local scope. |
| Arguments are copied into a function | Parameters refer to passed objects. Mutation may be visible to the caller; rebinding a local name is different. |
| A mutable default creates a fresh object per call | Default expressions are evaluated when the function is defined. Use an explicit fresh-object pattern when needed. |
| `__init__` creates a class | The class statement creates the class object; `__init__` initializes a new instance after allocation. |
| Attribute lookup is breadth-first | Multiple inheritance uses C3 method resolution order. Inspect `Class.__mro__`; do not substitute breadth-first search. |
| Underscores make data inaccessible | A leading underscore communicates a convention; name mangling is not an access-control boundary. |
| `map` and `filter` produce lists | They produce lazy iterators in Python 3. Materialize with `list(...)` only when needed. |
| A decorator only needs to call its wrapped function | Preserve its return value, forward arguments, and use `functools.wraps` for metadata. |
| Validation inside a cached function always runs | A cache hit skips the function body. Use a suitable cache key policy or validate outside the cached function when distinctions such as integer versus Boolean matter. |
| A bare `except` is a convenient retry strategy | Catch the expected exception type, keep retries finite in automated examples, and let unrelated problems remain visible. |

The lesson examples are deliberately small. They expose a concept clearly rather than implementing a production framework. Exercises add boundary cases and ask you to explain the observed behavior.

## Primary references

- [Python 3.13 tutorial](https://docs.python.org/3.13/tutorial/)
- [Data structures](https://docs.python.org/3.13/tutorial/datastructures.html)
- [Control flow and function definitions](https://docs.python.org/3.13/tutorial/controlflow.html)
- [Classes and scopes](https://docs.python.org/3.13/tutorial/classes.html)
- [Errors and exceptions](https://docs.python.org/3.13/tutorial/errors.html)
- [Functional programming tools](https://docs.python.org/3.13/library/functools.html)
- [uv projects](https://docs.astral.sh/uv/guides/projects/)
- [JupyterLab installation](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)

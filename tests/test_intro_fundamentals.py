"""Behavioral checks for the standalone introduction/fundamentals examples."""

import importlib.util
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_example(filename):
    """Load a numeric chapter filename without changing the import search path."""
    path = ROOT / "examples" / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


intro = load_example("01_introduction.py")
fundamentals = load_example("02_fundamentals.py")


class IntroductionTests(unittest.TestCase):
    def test_temperature_reference_points_and_fraction(self):
        for celsius, fahrenheit in [(0, 32), (100, 212), (-40, -40), (12.5, 54.5)]:
            with self.subTest(celsius=celsius):
                self.assertAlmostEqual(intro.celsius_to_fahrenheit(celsius), fahrenheit)

    def test_temperature_band_boundaries(self):
        for value, expected in [(-0.1, "freezing"), (0, "cool"), (19.9, "cool"), (20, "warm")]:
            with self.subTest(value=value):
                self.assertEqual(intro.classify_temperature(value), expected)

    def test_exact_palindrome_contract(self):
        for text in ["", "x", "level", "a a", "été"]:
            with self.subTest(text=text):
                self.assertTrue(intro.is_palindrome(text))
        for text in ["Level", "level!", "Python"]:
            with self.subTest(text=text):
                self.assertFalse(intro.is_palindrome(text))

    def test_sentinel_stops_before_even_skip_and_keeps_order(self):
        values = [3, -1, 4, 5, 0, 7]
        self.assertEqual(intro.collect_positive_odds(values), [3, 5])
        self.assertEqual(values, [3, -1, 4, 5, 0, 7])
        self.assertEqual(intro.collect_positive_odds([0, 1]), [])
        self.assertEqual(intro.collect_positive_odds([]), [])
        self.assertEqual(intro.collect_positive_odds([-3, 2, 4]), [])
        self.assertEqual(intro.collect_positive_odds([1, 1, 2, 3]), [1, 1, 3])

    def test_prime_boundaries_and_square_factors(self):
        for number in [-100, -1, 0, 1, 4, 9, 25, 49, 121, 169, 221]:
            with self.subTest(number=number):
                self.assertFalse(intro.is_prime(number))
        for number in [2, 3, 5, 29, 97, 101]:
            with self.subTest(number=number):
                self.assertTrue(intro.is_prime(number))

    def test_primes_below_excludes_limit(self):
        self.assertEqual(intro.primes_below(-10), [])
        self.assertEqual(intro.primes_below(2), [])
        self.assertEqual(intro.primes_below(3), [2])
        self.assertEqual(intro.primes_below(11), [2, 3, 5, 7])
        self.assertEqual(intro.primes_below(12), [2, 3, 5, 7, 11])
        self.assertEqual(intro.primes_below(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])


class FundamentalsTests(unittest.TestCase):
    def test_duck_typed_numbers_and_sequences(self):
        self.assertEqual(fundamentals.combine_and_repeat(2, 3, 4), 20)
        self.assertEqual(fundamentals.combine_and_repeat("py", "thon", 2), "pythonpython")
        self.assertEqual(fundamentals.combine_and_repeat([1], [2], 2), [1, 2, 1, 2])
        self.assertEqual(fundamentals.combine_and_repeat([1], [2], 0), [])
        with self.assertRaises(TypeError):
            fundamentals.combine_and_repeat([1], "2", 1)

    def test_normalization_whitespace_unicode_and_punctuation(self):
        cases = {
            "  PYTHON\t Straße \n": "python strasse",
            "": "",
            " \t\n": "",
            "Hello, WORLD!": "hello, world!",
            "a  b   c": "a b c",
        }
        for source, expected in cases.items():
            with self.subTest(source=source):
                self.assertEqual(fundamentals.normalize_words(source), expected)

    def test_report_fields_and_minimum_widths(self):
        self.assertEqual(fundamentals.format_report_row("A", 3, 2.5), "A          |    3 |    2.50")
        self.assertEqual(fundamentals.format_report_row("zero", 0, 0), "zero       |    0 |    0.00")
        self.assertEqual(fundamentals.format_report_row("cold", 2, -1.5), "cold       |    2 |   -1.50")
        self.assertEqual(
            fundamentals.format_report_row("longer than ten", 10000, 1.25),
            "longer than ten | 10000 |    1.25",
        )

    def test_note_roundtrip_preserves_unicode_spaces_and_empty_notes(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            expected = ["Grüße", "  keep spaces  ", ""]
            fundamentals.write_notes(path, expected)
            self.assertEqual(fundamentals.read_notes(path), expected)
            self.assertEqual(path.read_text(encoding="utf-8"), "Grüße\n  keep spaces  \n\n")
        self.assertFalse(path.exists())

    def test_note_replacement_empty_file_and_missing_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            fundamentals.write_notes(path, ["old", "content"])
            fundamentals.write_notes(path, ["new"])
            self.assertEqual(fundamentals.read_notes(path), ["new"])
            fundamentals.write_notes(path, [])
            self.assertEqual(fundamentals.read_notes(path), [])
            self.assertEqual(path.read_bytes(), b"")
            with self.assertRaises(FileNotFoundError):
                fundamentals.read_notes(Path(directory) / "missing.txt")

    def test_read_notes_handles_final_unterminated_line(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            path.write_text("first\n  last  ", encoding="utf-8")
            self.assertEqual(fundamentals.read_notes(path), ["first", "  last  "])

    def test_imports_are_quiet_and_do_not_run_demonstrations(self):
        for filename in ["01_introduction.py", "02_fundamentals.py"]:
            with self.subTest(filename=filename):
                path = ROOT / "examples" / filename
                program = (
                    "import runpy, sys; "
                    "runpy.run_path(sys.argv[1], run_name='import_check')"
                )
                result = subprocess.run(
                    [sys.executable, "-c", program, str(path)],
                    capture_output=True, text=True, check=True, timeout=10,
                )
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()

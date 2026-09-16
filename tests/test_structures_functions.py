"""Behavior checks for the chapter 03 and 04 reusable examples."""

import importlib.util
from pathlib import Path
import unittest


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def load_example(filename):
    """Load a numbered teaching example without running its main demonstration."""
    path = EXAMPLES / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


structures = load_example("03_data_structures.py")
functions = load_example("04_functions.py")


class DataStructuresTests(unittest.TestCase):
    def test_matrix_copy_has_independent_outer_list_and_rows(self):
        source = [[1, 2], [3, 4]]
        result = structures.copy_matrix_rows(source)
        result[0][0] = 99
        result.append([5, 6])
        self.assertEqual(source, [[1, 2], [3, 4]])
        self.assertEqual(result, [[99, 2], [3, 4], [5, 6]])
        self.assertIsNot(result[1], source[1])

    def test_row_copy_contract_is_shallow_beyond_rows(self):
        inner_object = {"value": 1}
        source = [[inner_object]]
        result = structures.copy_matrix_rows(source)
        self.assertIsNot(result[0], source[0])
        self.assertIs(result[0][0], inner_object)
        self.assertEqual(structures.copy_matrix_rows([]), [])
        self.assertEqual(structures.copy_matrix_rows([[]]), [[]])

    def test_fibonacci_boundaries_and_recurrence(self):
        self.assertEqual(structures.fibonacci_records(0), [])
        self.assertEqual(structures.fibonacci_records(1), [(0, 0)])
        records = structures.fibonacci_records(20)
        self.assertEqual([index for index, _ in records], list(range(20)))
        values = [value for _, value in records]
        self.assertEqual(values[:7], [0, 1, 1, 2, 3, 5, 8])
        self.assertEqual(values[-1], 4181)
        for index in range(2, len(values)):
            self.assertEqual(values[index], values[index - 1] + values[index - 2])
        with self.assertRaises(ValueError):
            structures.fibonacci_records(-1)

    def test_visit_grouping_keeps_repeated_visits_and_city_order(self):
        visits = [("Ada", "Graz"), ("Bo", "Vienna"), ("Ada", "Vienna"), ("Ada", "Graz")]
        original = visits.copy()
        counts, cities = structures.summarize_visits(visits)
        self.assertEqual(counts, {"Ada": 3, "Bo": 1})
        self.assertEqual(cities, {"Graz": ["Ada", "Ada"], "Vienna": ["Bo", "Ada"]})
        self.assertEqual(list(cities), ["Graz", "Vienna"])
        self.assertIsNot(cities["Graz"], cities["Vienna"])
        self.assertEqual(visits, original)
        self.assertEqual(counts.get("Missing", 0), 0)
        self.assertNotIn("Missing", counts)

    def test_visit_results_are_fresh_and_handle_empty_input(self):
        self.assertEqual(structures.summarize_visits([]), ({}, {}))
        first_counts, first_cities = structures.summarize_visits([("Ada", "Graz")])
        first_counts["Ada"] = 100
        first_cities["Graz"].append("Bo")
        self.assertEqual(structures.summarize_visits([("Ada", "Graz")]), ({"Ada": 1}, {"Graz": ["Ada"]}))

    def test_enrollment_comparisons_deduplicate_and_sort(self):
        python_students = ["Cara", "Ada", "Bo", "Ada"]
        statistics_students = ["Dee", "Bo", "Dee"]
        self.assertEqual(
            structures.compare_enrollments(python_students, statistics_students),
            {"both": ["Bo"], "either": ["Ada", "Bo", "Cara", "Dee"],
             "python_only": ["Ada", "Cara"], "exactly_one": ["Ada", "Cara", "Dee"]},
        )
        self.assertEqual(python_students, ["Cara", "Ada", "Bo", "Ada"])
        self.assertEqual(statistics_students, ["Dee", "Bo", "Dee"])

    def test_enrollment_empty_identical_and_disjoint_cases(self):
        self.assertEqual(
            structures.compare_enrollments([], []),
            {"both": [], "either": [], "python_only": [], "exactly_one": []},
        )
        identical = structures.compare_enrollments(["A", "B"], ["B", "A", "A"])
        self.assertEqual(identical["exactly_one"], [])
        self.assertEqual(identical["python_only"], [])
        disjoint = structures.compare_enrollments(["A"], ["B"])
        self.assertEqual(disjoint["both"], [])
        self.assertEqual(disjoint["exactly_one"], ["A", "B"])

    def test_word_results_keep_list_duplicates_but_collapse_mapping_keys(self):
        words = ["APPLE", "apple", "", "pear", "kiwi"]
        result = structures.word_toolkit(words)
        self.assertEqual(result["normalized"], ["apple", "apple", "", "pear", "kiwi"])
        self.assertEqual(result["long_words"], ["apple", "apple"])
        self.assertEqual(result["lengths"], {"apple": 5, "pear": 4, "kiwi": 4})
        self.assertEqual(result["initials"], {"A", "P", "K"})
        self.assertEqual(words, ["APPLE", "apple", "", "pear", "kiwi"])

    def test_word_lengths_measure_normalized_unicode_text(self):
        word = "İABC"
        self.assertEqual(len(word), 4)
        self.assertEqual(len(word.lower()), 5)
        result = structures.word_toolkit([word])
        self.assertEqual(result["lengths"], {word.lower(): 5})
        self.assertEqual(result["long_words"], [word.lower()])

    def test_word_empty_inputs_avoid_invalid_indexing(self):
        self.assertEqual(
            structures.word_toolkit([]),
            {"normalized": [], "long_words": [], "lengths": {}, "initials": set()},
        )
        empty_word = structures.word_toolkit([""])
        self.assertEqual(empty_word["normalized"], [""])
        self.assertEqual(empty_word["lengths"], {})
        self.assertEqual(empty_word["initials"], set())

    def test_ranking_is_stable_and_does_not_change_inputs(self):
        names = ["Zoe", "Ada", "Bo", "Cara"]
        scores = [80, 80, 69, 100]
        result = structures.rank_scores(names, scores)
        self.assertEqual(result["ranked"], [("Cara", 100), ("Zoe", 80), ("Ada", 80), ("Bo", 69)])
        self.assertEqual(list(result["passed"]), ["Cara", "Zoe", "Ada"])
        self.assertEqual(result["numbered"][0], (1, ("Cara", 100)))
        self.assertEqual(result["numbered"][-1], (4, ("Bo", 69)))
        self.assertEqual(names, ["Zoe", "Ada", "Bo", "Cara"])
        self.assertEqual(scores, [80, 80, 69, 100])

    def test_ranking_empty_threshold_and_mismatched_lengths(self):
        self.assertEqual(structures.rank_scores([], []), {"ranked": [], "passed": {}, "numbered": []})
        self.assertEqual(structures.rank_scores(["Ada"], [70])["passed"], {"Ada": 70})
        self.assertEqual(structures.rank_scores(["Ada"], [70], pass_mark=71)["passed"], {})
        for names, scores in [(["Ada"], []), ([], [70]), (["Ada", "Bo"], [70])]:
            with self.subTest(names=names, scores=scores):
                with self.assertRaises(ValueError):
                    structures.rank_scores(names, scores)


class FunctionTests(unittest.TestCase):
    def test_parse_reading_returns_clean_tuple_and_numeric_value(self):
        source = "  air TEMPERATURE "
        name, value = functions.parse_reading(source, " 21.5 ")
        self.assertEqual((name, value), ("Air Temperature", 21.5))
        self.assertIsInstance(value, float)
        self.assertEqual(source, "  air TEMPERATURE ")
        self.assertEqual(functions.parse_reading(" below zero ", "-4.25"), ("Below Zero", -4.25))
        self.assertEqual(functions.parse_reading("zero", "0"), ("Zero", 0.0))
        with self.assertRaises(ValueError):
            functions.parse_reading("temperature", "warm")

    def test_default_label_lists_do_not_share_state(self):
        first = functions.add_label(" A ")
        second = functions.add_label("B")
        first.append("later")
        self.assertEqual(first, ["A", "later"])
        self.assertEqual(second, ["B"])
        self.assertEqual(functions.add_label("C", None), ["C"])
        self.assertEqual(functions.add_label("  "), [""])

    def test_supplied_empty_and_nonempty_label_lists_are_mutated(self):
        empty = []
        self.assertIs(functions.add_label(" A ", empty), empty)
        self.assertEqual(empty, ["A"])
        self.assertIs(functions.add_label("B", empty), empty)
        self.assertEqual(empty, ["A", "B"])

    def test_adjusted_total_supports_defaults_unpacked_arguments_and_identity(self):
        self.assertEqual(functions.adjusted_total(2, 3), 5)
        self.assertEqual(functions.adjusted_total(), 0)
        self.assertEqual(functions.adjusted_total(offset=7), 7)
        amounts = [2, 3]
        options = {"multiplier": 2, "offset": 1}
        self.assertEqual(functions.adjusted_total(*amounts, **options), 11)
        self.assertEqual(functions.adjusted_total(2, 3, 4), 9)
        self.assertEqual(functions.adjusted_total(2, 3, multiplier=0, offset=4), 4)
        self.assertEqual(amounts, [2, 3])
        self.assertEqual(options, {"multiplier": 2, "offset": 1})

    def test_adjusted_total_negative_and_fractional_values(self):
        self.assertEqual(functions.adjusted_total(-2, 3), 1)
        self.assertAlmostEqual(functions.adjusted_total(0.1, 0.2, multiplier=0.5), 0.15)
        with self.assertRaises(TypeError):
            functions.adjusted_total(2, unexpected=3)

    def test_event_formatting_is_independent_of_keyword_insertion_order(self):
        first = {"user": "Ada", "count": 3}
        second = {"count": 3, "user": "Ada"}
        expected = "Saved\ncount: 3\nuser: Ada"
        self.assertEqual(functions.format_event("Saved", **first), expected)
        self.assertEqual(functions.format_event("Saved", **second), expected)
        self.assertEqual(list(first.items()), [("user", "Ada"), ("count", 3)])
        self.assertEqual(functions.format_event("Saved"), "Saved")
        self.assertEqual(functions.format_event("Checked", value=None, valid=False), "Checked\nvalid: False\nvalue: None")

    def test_transformation_uses_callback_without_changing_source(self):
        values = [1, 2, 3]
        result = functions.transform_values(values, functions.make_offset(10))
        self.assertEqual(result, [11, 12, 13])
        self.assertIsNot(result, values)
        self.assertEqual(values, [1, 2, 3])
        self.assertEqual(functions.transform_values(values, str), ["1", "2", "3"])
        self.assertEqual(functions.transform_values((1, 2), functions.make_offset(0.5)), [1.5, 2.5])

    def test_empty_transformation_does_not_call_callback(self):
        def must_not_run(value):
            raise AssertionError("An empty input must not call the transformation")

        self.assertEqual(functions.transform_values([], must_not_run), [])

    def test_offset_closures_retain_independent_captured_values(self):
        add_ten = functions.make_offset(10)
        subtract_two = functions.make_offset(-2)
        self.assertEqual(add_ten(5), 15)
        self.assertEqual(subtract_two(5), 3)
        self.assertEqual(add_ten(0), 10)
        self.assertEqual(subtract_two(0), -2)

    def test_score_summary_empty_and_boundary_results(self):
        self.assertEqual(functions.summarize_scores([]), {"count": 0, "mean": None, "passed": 0})
        self.assertEqual(functions.summarize_scores([50]), {"count": 1, "mean": 50.0, "passed": 1})
        self.assertEqual(functions.summarize_scores([49.9])["passed"], 0)
        self.assertEqual(functions.summarize_scores((0, 100), pass_mark=0), {"count": 2, "mean": 50.0, "passed": 2})

    def test_score_summary_preserves_input_and_accepts_only_named_threshold(self):
        scores = [40, 50, 90]
        self.assertEqual(functions.summarize_scores(scores), {"count": 3, "mean": 60.0, "passed": 2})
        self.assertEqual(functions.summarize_scores(scores, pass_mark=80), {"count": 3, "mean": 60.0, "passed": 1})
        self.assertEqual(scores, [40, 50, 90])
        with self.assertRaises(TypeError):
            functions.summarize_scores(scores, 80)


if __name__ == "__main__":
    unittest.main()

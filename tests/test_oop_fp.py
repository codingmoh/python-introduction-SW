"""Behavior checks for object state, protocols, lazy streams and decorators."""

from contextlib import redirect_stdout
import importlib.util
from io import StringIO
from itertools import islice
from pathlib import Path
import unittest


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def load_example(filename):
    path = EXAMPLES / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


oop = load_example("05_oop.py")
fp = load_example("06_functional_programming.py")


class ObjectTests(unittest.TestCase):
    def test_dog_lists_are_independent_of_instances_and_caller(self):
        original = ["sit"]
        first = oop.Dog("Ada", original)
        second = oop.Dog("Bo")
        third = oop.Dog("Cara")
        original.append("stay")
        first.teach_trick("roll over")
        second.teach_trick("come")
        self.assertEqual(first.tricks, ["sit", "roll over"])
        self.assertEqual(second.tricks, ["come"])
        self.assertEqual(third.tricks, [])
        self.assertIsNot(second.tricks, third.tricks)
        self.assertIs(first.teach_trick.__self__, first)

    def test_pizza_exhaustion_never_makes_slices_negative(self):
        toppings = ["Olives"]
        pizza = oop.Pizza(10, toppings, slices=1)
        toppings.append("Pepper")
        self.assertEqual(pizza.toppings, ("Olives",))
        self.assertTrue(pizza.eat_slice())
        for _ in range(3):
            self.assertFalse(pizza.eat_slice())
            self.assertEqual(pizza.slices_left, 0)
        self.assertFalse(oop.Pizza(10, slices=0).eat_slice())

    def test_pizza_rejects_invalid_dimensions_and_counts(self):
        for radius in [0, -1]:
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                oop.Pizza(radius)
        for slices, error in [(-1, ValueError), (1.5, TypeError), (True, TypeError)]:
            with self.subTest(slices=slices), self.assertRaises(error):
                oop.Pizza(10, slices=slices)

    def test_point_rotation_and_addition_have_distinct_mutation_contracts(self):
        point = oop.Point(3, 4)
        for _ in range(4):
            point.rotate_90_ccw()
        self.assertEqual(point, oop.Point(3, 4))
        other = oop.Point(-3, 2)
        result = point + other
        self.assertEqual(result, oop.Point(0, 6))
        self.assertEqual(point, oop.Point(3, 4))
        self.assertEqual(other, oop.Point(-3, 2))
        self.assertIsNot(result, point)
        self.assertIsNot(result, other)
        self.assertEqual(oop.Point().distance_to(point), 5.0)
        self.assertEqual(point.distance_to(point), 0.0)

    def test_point_protocols_handle_empty_sum_and_unsupported_operands(self):
        point = oop.Point(2, 3)
        self.assertEqual(tuple(point), (2, 3))
        self.assertEqual(list(point), list(point))
        self.assertEqual(sum([point, point], start=oop.Point()), oop.Point(4, 6))
        self.assertEqual(sum([], start=oop.Point()), oop.Point())
        self.assertIs(oop.Point.__add__(point, 2), NotImplemented)
        self.assertIs(oop.Point.__eq__(point, (2, 3)), NotImplemented)
        self.assertNotEqual(point, (2, 3))
        with self.assertRaises(TypeError):
            point + 2
        with self.assertRaises(TypeError):
            point.distance_to((2, 3))
        with self.assertRaises(TypeError):
            hash(point)

    def test_reading_list_has_independent_iterators_and_standard_indexing(self):
        original = ["Python", "Data", "Design"]
        shelf = oop.ReadingList(original)
        original.clear()
        self.assertEqual(len(shelf), 3)
        self.assertEqual(shelf[-1], "Design")
        self.assertEqual(shelf[1:], ["Data", "Design"])
        self.assertIn("Data", shelf)
        self.assertNotIn("Missing", shelf)
        left, right = iter(shelf), iter(shelf)
        self.assertEqual((next(left), next(left), next(right)), ("Python", "Data", "Python"))
        self.assertEqual(list(shelf), list(shelf))
        with self.assertRaises(IndexError):
            shelf[3]
        empty = oop.ReadingList()
        self.assertEqual(len(empty), 0)
        self.assertEqual(list(empty), [])
        with self.assertRaises(IndexError):
            empty[0]

    def test_subclass_initializes_and_extends_base_behavior(self):
        course = oop.OnlineCourse("Python", "Jupyter")
        self.assertIsInstance(course, oop.Course)
        self.assertEqual(course.title, "Python")
        self.assertEqual(course.describe(), "Python on Jupyter")
        self.assertEqual(oop.Course.describe(course), "Python")

    def test_failed_bookings_preserve_the_previous_state(self):
        workshop = oop.Workshop(3)
        self.assertEqual(workshop.book(2), 1)
        for places, error in [(2, oop.CapacityError), (0, ValueError), (-1, ValueError),
                              (1.5, TypeError), (True, TypeError)]:
            with self.subTest(places=places):
                with self.assertRaises(error):
                    workshop.book(places)
                self.assertEqual(workshop.booked, 2)
        self.assertEqual(workshop.book(), 0)
        with self.assertRaises(oop.CapacityError):
            workshop.book()
        self.assertEqual(workshop.booked, 3)

    def test_workshop_zero_capacity_and_invalid_capacity(self):
        empty = oop.Workshop(0)
        with self.assertRaises(oop.CapacityError):
            empty.book()
        self.assertEqual(empty.booked, 0)
        for capacity, error in [(-1, ValueError), (3.0, TypeError), (False, TypeError)]:
            with self.subTest(capacity=capacity), self.assertRaises(error):
                oop.Workshop(capacity)

    def test_parser_skips_only_bad_values_and_stops_after_success(self):
        self.assertEqual(oop.parse_first_integer(["bad", "3.5", " -4 "]), -4)
        self.assertEqual(oop.parse_first_integer(["0", None]), 0)
        with self.assertRaises(TypeError):
            oop.parse_first_integer([None, "42"])
        for candidates in [[], ["bad", "still bad"]]:
            with self.subTest(candidates=candidates), self.assertRaises(ValueError):
                oop.parse_first_integer(candidates)

    def test_eafp_pop_mutates_only_when_an_item_exists(self):
        values = [0, None]
        self.assertIsNone(oop.pop_or_default(values, "fallback"))
        self.assertEqual(values, [0])
        self.assertEqual(oop.pop_or_default(values, "fallback"), 0)
        self.assertEqual(oop.pop_or_default(values, "fallback"), "fallback")
        self.assertEqual(values, [])
        with self.assertRaises(AttributeError):
            oop.pop_or_default(None)


class FunctionalTests(unittest.TestCase):
    def tearDown(self):
        fp.fibonacci_at.cache_clear()

    def test_tax_transformation_preserves_source_and_returns_fresh_values(self):
        prices = [10, 20]
        first = fp.add_tax(prices, 0.2)
        self.assertEqual(first, [12.0, 24.0])
        self.assertEqual(prices, [10, 20])
        first.append(99)
        self.assertEqual(fp.add_tax(prices, 0.2), [12.0, 24.0])
        self.assertEqual(fp.add_tax([], 0.2), [])

    def test_prime_predicate_covers_boundaries_and_perfect_squares(self):
        for number in [-10, 0, 1, 4, 49, 121]:
            with self.subTest(number=number):
                self.assertFalse(fp.is_prime(number))
        for number in [2, 3, 29, 97]:
            with self.subTest(number=number):
                self.assertTrue(fp.is_prime(number))
        self.assertEqual(list(filter(fp.is_prime, range(10))), [2, 3, 5, 7])

    def test_cleaning_pipeline_is_lazy_single_use_and_skips_whitespace(self):
        requested = []

        def source():
            for word in [" ", " PYTHON ", "DATA"]:
                requested.append(word)
                yield word

        pipeline = fp.cleaned_words(source())
        self.assertEqual(requested, [])
        self.assertEqual(next(pipeline), "python")
        self.assertEqual(requested, [" ", " PYTHON "])
        self.assertEqual(list(pipeline), ["data"])
        self.assertEqual(list(pipeline), [])
        self.assertEqual(list(fp.cleaned_words([])), [])

    def test_countdown_exhaustion_is_stable_and_instances_independent(self):
        left, right = fp.Countdown(3), fp.Countdown(3)
        self.assertIs(iter(left), left)
        self.assertEqual(next(left), 3)
        self.assertEqual(list(left), [2, 1])
        self.assertEqual(list(right), [3, 2, 1])
        self.assertEqual(list(left), [])
        for _ in range(2):
            with self.assertRaises(StopIteration):
                next(left)
        self.assertEqual(list(fp.Countdown(0)), [])
        for start, error in [(-1, ValueError), (True, TypeError), (2.5, TypeError)]:
            with self.subTest(start=start), self.assertRaises(error):
                fp.Countdown(start)

    def test_fibonacci_consumers_obey_count_and_value_bounds(self):
        left, right = fp.fibonacci_numbers(), fp.fibonacci_numbers()
        self.assertEqual(list(islice(left, 8)), [1, 1, 2, 3, 5, 8, 13, 21])
        self.assertEqual(next(right), 1)
        self.assertEqual(next(left), 34)
        self.assertEqual(list(fp.fibonacci_up_to(1)), [1, 1])
        self.assertEqual(list(fp.fibonacci_up_to(20)), [1, 1, 2, 3, 5, 8, 13])
        self.assertEqual(list(fp.fibonacci_up_to(0)), [])
        self.assertEqual(list(fp.fibonacci_up_to(-5)), [])
        with self.assertRaises(TypeError):
            list(fp.fibonacci_up_to(float("inf")))
        left.close()
        right.close()

    def test_finite_generator_handles_empty_and_exclusive_stop(self):
        self.assertEqual(list(fp.generate_ints(0)), [])
        self.assertEqual(list(fp.generate_ints(4)), [0, 1, 2, 3])

    def test_closures_keep_independent_divisors_and_reject_zero(self):
        by_three = fp.make_divisibility_test(3)
        by_five = fp.make_divisibility_test(5)
        self.assertTrue(by_three(0))
        self.assertTrue(by_three(-6))
        self.assertFalse(by_three(10))
        self.assertTrue(by_five(10))
        self.assertTrue(fp.make_divisibility_test(-2)(4))
        for divisor, error in [(0, ValueError), (True, TypeError), ("3", TypeError)]:
            with self.subTest(divisor=divisor), self.assertRaises(error):
                fp.make_divisibility_test(divisor)

    def test_perform_twice_preserves_results_and_keyword_arguments(self):
        calls = []

        def operation(value, *, increment):
            calls.append(value)
            return value + increment

        self.assertEqual(fp.perform_twice(operation, 2, increment=3), (5, 5))
        self.assertEqual(calls, [2, 2])

    def test_debug_preserves_metadata_returns_and_original_exception(self):
        failure = ValueError("deliberate failure")

        def operation(value, *, increment=1):
            """A documented operation."""
            if value < 0:
                raise failure
            return value + increment

        wrapped = fp.debug(operation)
        with redirect_stdout(StringIO()) as output:
            self.assertEqual(wrapped(2, increment=4), 6)
            with self.assertRaises(ValueError) as caught:
                wrapped(-1)
        self.assertIs(caught.exception, failure)
        self.assertEqual(wrapped.__name__, "operation")
        self.assertEqual(wrapped.__doc__, operation.__doc__)
        self.assertIs(wrapped.__wrapped__, operation)
        self.assertIn("Calling operation", output.getvalue())

    def test_decorator_factory_configurations_do_not_interfere(self):
        def total(a, *, b):
            """Sum two numbers."""
            return a + b

        doubled = fp.scale_result(2)(total)
        zeroed = fp.scale_result(0)(total)
        self.assertEqual(doubled(3, b=4), 14)
        self.assertEqual(zeroed(3, b=4), 0)
        self.assertEqual(total(3, b=4), 7)
        self.assertEqual(doubled.__name__, "total")
        self.assertIs(doubled.__wrapped__, total)
        with self.assertRaises(TypeError):
            doubled(3, unexpected=4)

    def test_cache_reuses_results_without_new_misses(self):
        fp.fibonacci_at.cache_clear()
        self.assertEqual(fp.fibonacci_at(20), 6765)
        before = fp.fibonacci_at.cache_info()
        self.assertEqual(fp.fibonacci_at(20), 6765)
        after = fp.fibonacci_at.cache_info()
        self.assertEqual(after.misses, before.misses)
        self.assertEqual(after.hits, before.hits + 1)
        self.assertEqual(after.currsize, before.currsize)
        self.assertEqual(fp.fibonacci_at(0), 0)
        self.assertEqual(fp.fibonacci_at(1), 1)
        for index, error in [(-1, ValueError), (True, TypeError), (2.5, TypeError)]:
            with self.subTest(index=index), self.assertRaises(error):
                fp.fibonacci_at(index)

    def test_typed_cache_cannot_bypass_validation_with_equal_keyword_keys(self):
        fp.fibonacci_at.cache_clear()
        self.assertEqual(fp.fibonacci_at(index=1), 1)
        self.assertEqual(fp.fibonacci_at(index=0), 0)
        for index in [True, False, 1.0, 0.0]:
            with self.subTest(index=index), self.assertRaises(TypeError):
                fp.fibonacci_at(index=index)
        self.assertEqual(fp.fibonacci_at(index=1), 1)


if __name__ == "__main__":
    unittest.main()

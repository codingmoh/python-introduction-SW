"""Runnable examples and reusable functions for chapter 01.

Run from the repository with ``uv run examples/01_introduction.py``.
The example is noninteractive and uses only the Python standard library.
"""

from math import isqrt


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a numeric Celsius temperature to Fahrenheit."""
    return celsius * 9 / 5 + 32


def is_palindrome(text: str) -> bool:
    """Test exact text equality with its reversal, including case and spaces.

    Empty text and single-character text are palindromes under this definition.
    """
    return text == text[::-1]


def classify_temperature(celsius: float) -> str:
    """Classify a number as freezing (<0), cool (<20), or warm (>=20)."""
    if celsius < 0:
        return "freezing"
    if celsius < 20:
        return "cool"
    return "warm"


def collect_positive_odds(values: list[int]) -> list[int]:
    """Collect positive odd integers before the first zero; keep duplicates."""
    result = []
    for value in values:
        if value == 0:
            break
        if value < 0 or value % 2 == 0:
            continue
        result.append(value)
    return result


def is_prime(number: int) -> bool:
    """Return whether an integer is prime; all values below 2 are nonprime."""
    if number < 2:
        return False
    for divisor in range(2, isqrt(number) + 1):
        if number % divisor == 0:
            return False
    return True


def primes_below(limit: int) -> list[int]:
    """Return prime integers in increasing order, strictly below the limit."""
    result = []
    for candidate in range(2, limit):
        if is_prime(candidate):
            result.append(candidate)
    return result


def main() -> None:
    """Demonstrate the chapter's ideas without waiting for keyboard input."""
    print("Hello world!")
    print("Arithmetic:", 5 / 2, 5 // 2, -7 // 3, 7 % 3, 2**4)
    word = "Arthur"
    print("Slices:", word[:2], word[-3:], word[1:5:2], word[::-1])
    basket = ["bread", "milk"]
    basket.append("apples")
    basket[1] = "oat drink"
    print("Basket:", basket, "items:", len(basket))
    simulated_input = "12"
    limit = int(simulated_input)
    print(f"Primes below {limit}: {primes_below(limit)}")
    print("Positive odds before 0:", collect_positive_odds([3, -1, 4, 5, 0, 7]))
    for temperature in [-1, 0, 19.9, 20]:
        print(f"{temperature} °C = {celsius_to_fahrenheit(temperature):.2f} °F; "
              f"{classify_temperature(temperature)}")
    for text in ["level", "Level", ""]:
        print(f"{text!r} is an exact palindrome: {is_palindrome(text)}")
    try:
        int("not a number")
    except ValueError:
        print("Caught the expected invalid-integer conversion.")


if __name__ == "__main__":
    main()

"""Runnable functional Python examples using only the standard library."""

from functools import lru_cache, wraps
from itertools import islice


def add_tax(prices, rate):
    """Return new values without mutating the caller's input sequence."""
    return [price * (1 + rate) for price in prices]


def is_prime(number):
    """Return whether an integer is prime; numbers below two are not prime."""
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def cleaned_words(words):
    """Lazily strip, lowercase and keep nonempty text values."""
    return filter(None, map(lambda word: word.strip().lower(), words))


class Countdown:
    """A single-use iterator yielding start, start - 1, ..., 1."""

    def __init__(self, start):
        if isinstance(start, bool) or not isinstance(start, int):
            raise TypeError("start must be an integer")
        if start < 0:
            raise ValueError("start must not be negative")
        self.remaining = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining == 0:
            raise StopIteration
        result = self.remaining
        self.remaining -= 1
        return result


def generate_ints(stop):
    """Yield the integers from zero up to, but excluding, stop."""
    yield from range(stop)


def fibonacci_numbers():
    """Yield the infinite stream 1, 1, 2, 3, 5, ...; consume it with a bound."""
    a, b = 0, 1
    while True:
        a, b = b, a + b
        yield a


def fibonacci_up_to(limit):
    """Yield Fibonacci numbers no greater than a finite integer limit."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    for number in fibonacci_numbers():
        if number > limit:
            return
        yield number


def make_divisibility_test(divisor):
    """Return a predicate retaining its own nonzero integer divisor."""
    if isinstance(divisor, bool) or not isinstance(divisor, int):
        raise TypeError("divisor must be an integer")
    if divisor == 0:
        raise ValueError("divisor must not be zero")

    def divisible(number):
        return number % divisor == 0

    return divisible


def perform_twice(function, *args, **kwargs):
    """Call a function twice and preserve both return values."""
    return function(*args, **kwargs), function(*args, **kwargs)


def debug(function):
    """Print call arguments while preserving metadata, results and errors."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"Calling {function.__name__}: {args!r}, {kwargs!r}")
        return function(*args, **kwargs)
    return wrapper


def scale_result(factor):
    """Build a decorator that multiplies a numeric return value."""
    def decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return factor * function(*args, **kwargs)
        return wrapper
    return decorate


@lru_cache(maxsize=None, typed=True)
def fibonacci_at(index):
    """Return F(index) for a small nonnegative integer; F(0)=0, F(1)=1.

    Typed keys keep booleans and floats separate from validated integer keys.
    Caching avoids repeated recursive subproblems. Very large indices should
    use an iterative algorithm to avoid Python's recursion limit.
    """
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("index must be an integer")
    if index < 0:
        raise ValueError("index must not be negative")
    if index < 2:
        return index
    return fibonacci_at(index - 1) + fibonacci_at(index - 2)


def main():
    print("Tax:", add_tax([10, 20], 0.2))
    print("Primes:", list(filter(is_prime, range(20))))
    print("Words:", list(cleaned_words([" Python ", "", " FUNCTIONAL "])))
    countdown = Countdown(3)
    print("Countdown:", list(countdown), list(countdown))
    print("Ten Fibonacci numbers:", list(islice(fibonacci_numbers(), 10)))
    print("Fibonacci up to 20:", list(fibonacci_up_to(20)))
    print("Multiples of 3:", list(filter(make_divisibility_test(3), range(10))))

    @debug
    def total(a, b, multiplier=1):
        return (a + b) * multiplier

    print("Decorated result:", total(2, 3, multiplier=4))
    print("Cached F(30):", fibonacci_at(30))
    print("Cache:", fibonacci_at.cache_info())


if __name__ == "__main__":
    main()

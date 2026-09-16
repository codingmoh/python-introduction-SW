"""Object-oriented examples: independent state, protocols, inheritance and errors.

Run this file with Python 3.13 or newer. Importing it does not run the demo.
"""

from math import hypot


class Dog:
    """Each dog owns its own list of tricks, including when a list is supplied."""

    kind = "Canine"

    def __init__(self, name, tricks=None):
        self.name = name
        self.tricks = [] if tricks is None else list(tricks)

    def teach_trick(self, trick):
        self.tricks.append(trick)


class Pizza:
    """Track the remaining slices of one pizza."""

    def __init__(self, radius, toppings=(), slices=8):
        if radius <= 0:
            raise ValueError("radius must be positive")
        if isinstance(slices, bool) or not isinstance(slices, int):
            raise TypeError("slices must be an integer")
        if slices < 0:
            raise ValueError("slices must not be negative")
        self.radius = radius
        self.toppings = tuple(toppings)
        self.slices_left = slices

    def eat_slice(self):
        """Consume a slice and return True, or return False when empty."""
        if self.slices_left == 0:
            return False
        self.slices_left -= 1
        return True

    def __repr__(self):
        return (f"Pizza(radius={self.radius!r}, toppings={self.toppings!r}, "
                f"slices={self.slices_left!r})")


class Point:
    """A mutable two-dimensional point with addition and coordinate iteration."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def rotate_90_ccw(self):
        """Rotate this point 90 degrees counterclockwise around the origin."""
        self.x, self.y = -self.y, self.x

    def distance_to(self, other):
        if not isinstance(other, Point):
            raise TypeError("other must be a Point")
        return hypot(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"

    def __str__(self):
        return f"({self.x}, {self.y})"


class ReadingList:
    """A small container that delegates its operations to a private list."""

    def __init__(self, titles=()):
        self._titles = list(titles)

    def __len__(self):
        return len(self._titles)

    def __contains__(self, title):
        return title in self._titles

    def __getitem__(self, index):
        return self._titles[index]

    def __iter__(self):
        return iter(self._titles)


class Course:
    """A base class whose method a subclass can extend."""

    def __init__(self, title):
        self.title = title

    def describe(self):
        return self.title


class OnlineCourse(Course):
    def __init__(self, title, platform):
        super().__init__(title)
        self.platform = platform

    def describe(self):
        return f"{super().describe()} on {self.platform}"


class CapacityError(Exception):
    """A booking would exceed the available capacity."""


class Workshop:
    """Keep bookings between zero and a fixed nonnegative integer capacity."""

    def __init__(self, capacity):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity < 0:
            raise ValueError("capacity must not be negative")
        self.capacity = capacity
        self.booked = 0

    def book(self, places=1):
        if isinstance(places, bool) or not isinstance(places, int):
            raise TypeError("places must be an integer")
        if places <= 0:
            raise ValueError("places must be positive")
        if self.booked + places > self.capacity:
            raise CapacityError("not enough places available")
        self.booked += places
        return self.capacity - self.booked


def parse_first_integer(candidates):
    """Return the first valid integer string; a finite input gives a finite retry.

    Invalid strings are skipped. Unsupported types such as None raise TypeError.
    """
    for candidate in candidates:
        try:
            return int(candidate)
        except ValueError:
            continue
    raise ValueError("no valid integer was supplied")


def pop_or_default(items, default=None):
    """Remove the final item, returning a default only when the list is empty."""
    try:
        return items.pop()
    except IndexError:
        return default


def main():
    dog = Dog("Astro")
    dog.teach_trick("sit")
    print(dog.name, dog.kind, dog.tricks)
    pizza = Pizza(14, ("Olives",), slices=1)
    print(repr(pizza), pizza.eat_slice(), pizza.eat_slice())
    point = Point(3, 5)
    point.rotate_90_ccw()
    print(point, repr(point + Point(9, -2)))
    print("Sum:", sum([Point(1, 2), Point(3, 4)], start=Point()))
    print(OnlineCourse("Python", "Jupyter").describe())
    workshop = Workshop(1)
    workshop.book()
    try:
        workshop.book()
    except CapacityError as error:
        print(type(error).__name__, str(error))
    print("Parsed:", parse_first_integer(["not yet", "42"]))


if __name__ == "__main__":
    main()

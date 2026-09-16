"""Chapter 04: functions with explicit contracts and independently runnable demos."""


def parse_reading(name, raw_value):
    """Return (stripped title-case name, float value); invalid values raise ValueError."""
    return name.strip().title(), float(raw_value)


def add_label(label, labels=None):
    """Append a stripped label and return labels, creating a list when omitted.

    An explicitly supplied list is mutated and returned unchanged in identity.
    Empty stripped labels are retained.
    """
    if labels is None:
        labels = []
    labels.append(label.strip())
    return labels


def adjusted_total(*amounts, multiplier=1, offset=0):
    """Return sum(amounts) * multiplier + offset; an empty sum is zero."""
    return sum(amounts) * multiplier + offset


def format_event(event, **details):
    """Return event followed by alphabetically ordered 'key: value' lines."""
    lines = [event]
    for key, value in sorted(details.items()):
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def transform_values(values, transform):
    """Return a new list of transformed values without modifying the input list.

    A supplied callback can have its own side effects; use a pure callback when
    the objects inside the input must also remain unchanged.
    """
    return [transform(value) for value in values]


def make_offset(offset):
    """Return a function that adds the captured offset to its argument."""
    def add_offset(value):
        return value + offset
    return add_offset


def summarize_scores(scores, *, pass_mark=50):
    """Return count, mean, and passing count for a sequence of numeric scores.

    Scores equal to pass_mark pass. Empty input has mean None and zero counts.
    The supplied sequence is not modified.
    """
    count = len(scores)
    mean = sum(scores) / count if count else None
    passed = sum(1 for score in scores if score >= pass_mark)
    return {"count": count, "mean": mean, "passed": passed}


def main():
    """Demonstrate returns, defaults, unpacking, and function objects."""
    name, value = parse_reading("  air TEMPERATURE ", " 21.5 ")
    print("Parsed reading:", name, value)
    print("Independent defaults:", add_label(" A "), add_label("B"))
    existing = []
    add_label(" C ", existing)
    print("Explicitly shared list:", existing)

    amounts = [2, 3]
    settings = {"multiplier": 2, "offset": 1}
    print("Adjusted total:", adjusted_total(*amounts, **settings))
    print(format_event("Saved", user="Ada", count=3))

    offset_ten = make_offset(10)
    print("Transformed values:", transform_values([1, 2, 3], offset_ten))
    print("Score summary:", summarize_scores([40, 50, 90]))
    print("Empty summary:", summarize_scores([]))
    try:
        summarize_scores([70], 60)
    except TypeError:
        print("Expected TypeError: pass_mark must be supplied by keyword.")


if __name__ == "__main__":
    main()

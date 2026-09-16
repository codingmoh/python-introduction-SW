"""Chapter 03: reusable container examples; run this file for sample results."""


def copy_matrix_rows(matrix):
    """Copy the outer list and each row; objects inside rows remain shared."""
    return [row.copy() for row in matrix]


def fibonacci_records(n):
    """Return (index, Fibonacci number) pairs for nonnegative integer n."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    values = []
    a, b = 0, 1
    for _ in range(n):
        values.append(a)
        a, b = b, a + b
    return list(enumerate(values))


def summarize_visits(visits):
    """Return (counts_by_person, visitors_by_city), preserving encounter order."""
    visit_counts = {}
    people_by_city = {}
    for name, city in visits:
        visit_counts[name] = visit_counts.get(name, 0) + 1
        people_by_city.setdefault(city, []).append(name)
    return visit_counts, people_by_city


def compare_enrollments(python_students, statistics_students):
    """Return sorted membership comparisons; repeated signups count once."""
    python_set = set(python_students)
    statistics_set = set(statistics_students)
    return {
        "both": sorted(python_set & statistics_set),
        "either": sorted(python_set | statistics_set),
        "python_only": sorted(python_set - statistics_set),
        "exactly_one": sorted(python_set ^ statistics_set),
    }


def word_toolkit(words):
    """Return lowercase forms, long words, word lengths, and unique initials."""
    normalized = [word.lower() for word in words]
    long_words = [word for word in normalized if len(word) >= 5]
    lengths = {word: len(word) for word in normalized if word}
    initials = {word[0].upper() for word in words if word}
    return {
        "normalized": normalized,
        "long_words": long_words,
        "lengths": lengths,
        "initials": initials,
    }


def rank_scores(names, scores, pass_mark=70):
    """Return ranked, passed, and numbered records for distinct student names.

    Raise ValueError if the input lengths differ. Preserve input order on ties.
    Names are assumed unique because the passed result uses names as dict keys.
    """
    records = list(zip(names, scores, strict=True))
    ranked = sorted(records, key=lambda record: record[1], reverse=True)
    passed = {name: score for name, score in ranked if score >= pass_mark}
    numbered = list(enumerate(ranked, start=1))
    return {"ranked": ranked, "passed": passed, "numbered": numbered}


def main():
    """Run a small, deterministic demonstration of the chapter's containers."""
    queue = ["Ada", "Ben", "Cara"]
    queue.append("Dee")
    queue.insert(1, "Eli")
    queue.remove("Cara")
    print("Served:", queue.pop(0))
    print("Remaining:", queue)
    print("Reverse view:", list(reversed(queue)))

    matrix = [[1, 2], [3, 4]]
    copied = copy_matrix_rows(matrix)
    copied[0][0] = 99
    print("Original and copied matrix:", matrix, copied)
    print("Fibonacci records:", fibonacci_records(7))

    visits = [("Ada", "Vienna"), ("Bo", "Graz"), ("Ada", "Vienna")]
    print("Visit counts and groups:", summarize_visits(visits))
    print("Enrollment comparison:", compare_enrollments(["Ada", "Bo", "Ada"], ["Bo", "Cara"]))

    word_results = word_toolkit(["Apple", "pear", "BANANA", "pear", "", "kiwi"])
    print("Normalized words:", word_results["normalized"])
    print("Initials (sorted for display):", sorted(word_results["initials"]))
    print("Ranked scores:", rank_scores(["Ada", "Bo", "Cara"], [88, 65, 88]))

    try:
        rank_scores(["Ada"], [])
    except ValueError:
        print("Expected ValueError: names and scores need matching lengths.")


if __name__ == "__main__":
    main()

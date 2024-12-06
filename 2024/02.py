"""Advent of Code 2024: Day 2"""

import itertools

# --- Part One --- #


def preprocess_one(report: list[int]) -> list[int]:
    distances = []
    for one, two in itertools.pairwise(report):
        distances.append(two - one)
    return distances


def preprocess_all(given: list[list[int]]):
    for report in given:
        yield preprocess_one(report)


def valid_values(distances: list[int]) -> list[int]:
    # Must be (1) all in 1–3 and (2) all either decreasing or increasing
    valid = [1, 2, 3]
    if distances[0] < 0:
        valid = [-val for val in valid]
    return valid


def are_safe(distances: list[int]) -> bool:
    valid = valid_values(distances)
    return all(dist in valid for dist in distances)


def part_one(given: list[list[int]]) -> int:
    safe = 0
    for distances in preprocess_all(given):
        if are_safe(distances):
            safe += 1
    return safe


# --- Part Two --- #


def report_safe(report):
    # Already safe
    if are_safe(preprocess_one(report)):
        return True

    # Try removing one by one
    for i in range(len(report)):
        without = report[:i] + report[i + 1 :]
        if are_safe(preprocess_one(without)):
            return True

    return False


def part_two(given):
    safe = 0
    for report in given:
        if report_safe(report):
            safe += 1
    return safe


# --- Main Program --- #


with open("02_input", encoding="utf-8") as fh:
    given = [[int(el) for el in line.rstrip().split()] for line in fh.readlines()]

print(f"Part One: {part_one(given)}")
print(f"Part Two: {part_two(given)}")

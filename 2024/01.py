"""Advent of Code 2024: Day 1"""

# --- Part One --- #


def preprocess(given: list[list[int]]) -> tuple[list[int], list[int]]:
    left, right = [], []
    for lf, rg in given:
        left.append(lf)
        right.append(rg)
    return left, right


def part_one(given: list[list[int]]) -> int:
    left, right = preprocess(given)
    left.sort()
    right.sort()
    distance = 0
    for lf, rg in zip(left, right):
        distance += abs(rg - lf)
    return distance


# --- Part Two --- #


def part_two(given: list[list[int]]) -> int:
    left, right = preprocess(given)
    similarity_score = 0
    for lf in left:
        appearances_in_right = right.count(lf)
        similarity_score += lf * appearances_in_right

    return similarity_score


# --- Main Program --- #


with open("01_input", encoding="utf-8") as fh:
    given = []
    for line in fh.readlines():
        given.append([int(el) for el in line.rstrip().split()])

print(f"Part One: {part_one(given)}")
print(f"Part Two: {part_two(given)}")

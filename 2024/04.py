"""Advent of Code 2024: Day 4"""

import itertools

# --- Part One --- #


def find_letter(field: list[list[str]], letter: str) -> list[tuple[int, int]]:
    coordinates = []
    for i, row in enumerate(given):
        for j, el in enumerate(row):
            if el == letter:
                coordinates.append((i, j))
    return coordinates


def step(
    start: tuple[int, int], direction: tuple[int, int], size: int
) -> tuple[int, int]:
    assert len(start) == len(direction) == 2
    return start[0] + direction[0] * size, start[1] + direction[1] * size


def has_target(
    field: list[list[str]],
    start: tuple[int, int],
    direction: tuple[int, int],
    target: str,
) -> bool:
    end_i, end_j = step(start, direction, 3)
    # Check if the word would reach outside the field from the given start
    if end_i not in range(len(field)) or end_j not in range(len(field[0])):
        return False

    for mult in range(1, 4):
        i_coord, j_coord = step(start, direction, mult)
        if field[i_coord][j_coord] != target[mult]:
            return False

    return True


def part_one(given: list[list[str]]) -> int:
    xs = find_letter(given, "X")

    directions = list(itertools.product([0, 1, -1], repeat=2))
    directions.remove((0, 0))

    xmas_count = 0
    for x_pos in xs:
        for direction in directions:
            if has_target(given, x_pos, direction, target="XMAS"):
                xmas_count += 1

    return xmas_count


# --- Part Two --- #


def is_x_mas(field: list[list[str]], i: int, j: int) -> bool:
    pair_coordinates = [
        ((i - 1, j - 1), (i + 1, j + 1)),
        ((i - 1, j + 1), (i + 1, j - 1)),
    ]
    for pair in pair_coordinates:
        my_letters = []
        for p_i, p_j in pair:
            my_letters.append(field[p_i][p_j])
        if sorted(my_letters) != ["M", "S"]:
            return False

    return True


def part_two(given: list[list[str]]) -> int:
    a_s = find_letter(given, "A")
    x_mas_count = 0
    for i, j in a_s:
        # Too close to border
        if i not in range(1, len(given) - 1) or j not in range(1, len(given[0]) - 1):
            continue

        if is_x_mas(given, i, j):
            x_mas_count += 1

    return x_mas_count


# --- Main Program --- #


with open("04_input", encoding="utf-8") as fh:
    given = [list(line.rstrip()) for line in fh.readlines()]

print(f"Part One: {part_one(given)}")
print(f"Part Two: {part_two(given)}")

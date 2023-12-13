""" Advent of Code 2023: Day 13 """

FILE_TO_READ = "13_input"

# A square pattern is given. Is the pattern reflected along any axis?
# E.g.: #.##. is reflected between the two "#"s (additional columns can be ignored).
# Sum up: (# of columns left of each reflection line) + 100 * (# of rows above each)


import itertools
from pprint import pprint
from typing import Iterable


class Pattern(list):
    """A pattern matrix that we represent by a list of `str`s."""

    def column_line_reflects(self, leftright: tuple[int, int]) -> bool:
        # Check row by row
        for row in self:
            left, right = leftright
            while left >= 0 and right < len(row):
                if row[left] != row[right]:
                    return False
                left -= 1
                right += 1
        # If no check failed, we found a reflection line
        return True

    def row_line_reflects(self, topbottom: tuple[int, int]) -> bool:
        # Check column by column (assuming all rows have equal length)
        for col_idx in range(len(self[0])):
            top, bottom = topbottom
            while top >= 0 and bottom < len(self):
                if self[top][col_idx] != self[bottom][col_idx]:
                    return False
                top -= 1
                bottom += 1
        # If no check failed, we found a reflection line
        return True


def given() -> Iterable[Pattern]:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        text = given_file.read()
    for pattern_line in text.split("\n\n"):
        yield Pattern([l.rstrip("\n") for l in pattern_line.rstrip("\n").split("\n")])


# --- Part One --- #


def part_one():
    result: int = 0
    for pattern in given():
        # Check columns
        reflecting_column_lines: list[tuple[int, int]] = []
        for left, right in itertools.pairwise(range(len(pattern[0]))):
            if pattern.column_line_reflects((left, right)):
                reflecting_column_lines.append((left, right))
        # Check rows
        reflecting_row_lines: list[tuple[int, int]] = []
        for top, bottom in itertools.pairwise(range(len(pattern))):
            if pattern.row_line_reflects((top, bottom)):
                reflecting_row_lines.append((top, bottom))

        # Calculate
        for left, _ in reflecting_column_lines:
            result += left + 1  # index that counts to the left is 0-based
        for top, _ in reflecting_row_lines:
            result += 100 * (top + 1)
    return result


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

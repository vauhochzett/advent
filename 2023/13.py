""" Advent of Code 2023: Day 13 """

FILE_TO_READ = "13_input"

# A square pattern is given. Is the pattern reflected along any axis?
# E.g.: #.##. is reflected between the two "#"s (additional columns can be ignored).
# Sum up: (# of columns left of each reflection line) + 100 * (# of rows above each)


import itertools
from typing import Iterable, Optional


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

    def reflecting_column_lines(self) -> list[tuple[int, int]]:
        reflecting_column_lines: list[tuple[int, int]] = []
        for left, right in itertools.pairwise(range(len(self[0]))):
            if self.column_line_reflects((left, right)):
                reflecting_column_lines.append((left, right))
        return reflecting_column_lines

    def reflecting_row_lines(self) -> list[tuple[int, int]]:
        reflecting_row_lines: list[tuple[int, int]] = []
        for top, bottom in itertools.pairwise(range(len(self))):
            if self.row_line_reflects((top, bottom)):
                reflecting_row_lines.append((top, bottom))
        return reflecting_row_lines

    def calculate_reflection_score(self) -> int:
        return calculate_reflection_score(
            self.reflecting_column_lines(), self.reflecting_row_lines()
        )


def calculate_reflection_score(
    reflecting_column_lines: list[tuple[int, int]],
    reflecting_row_lines: list[tuple[int, int]],
) -> int:
    """Find reflection lines, count columns and rows before, return score."""
    result: int = 0
    for left, _ in reflecting_column_lines:
        result += left + 1  # index that counts to the left is 0-based
    for top, _ in reflecting_row_lines:
        result += 100 * (top + 1)
    return result


def given() -> Iterable[Pattern]:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        text = given_file.read()
    for pattern_line in text.split("\n\n"):
        yield Pattern(
            [list(l.rstrip("\n")) for l in pattern_line.rstrip("\n").split("\n")]
        )


# --- Part One --- #


def part_one():
    return sum([pattern.calculate_reflection_score() for pattern in given()])


# --- Part Two --- #


def new_reflection_line(
    base: list[tuple[int, int]], changed: list[tuple[int, int]]
) -> Optional[tuple[int, int]]:
    """If a new reflection line is in `changed` that is not in `base`, return it.
    Otherwise, return `None`."""
    if not changed:
        return None

    if not base:
        assert len(changed) == 1
        return changed[0]

    assert len(base) == 1
    if len(changed) > 1:
        base_removed = list(set(changed) - set(base))
        assert len(base_removed) == 1
        return base_removed[0]

    assert len(changed) == 1
    if base[0] != changed[0]:
        return changed[0]
    return None


def part_two():
    result: int = 0
    for pattern in given():
        base_reflecting_column_lines = pattern.reflecting_column_lines()
        base_reflecting_row_lines = pattern.reflecting_row_lines()
        assert len(base_reflecting_column_lines) <= 1
        assert len(base_reflecting_row_lines) <= 1

        # Try to flip each cell once and check if a new reflection line appears
        for row_i, col_i in itertools.product(
            range(len(pattern)), range(len(pattern[0]))
        ):
            stored_val = pattern[row_i][col_i]
            pattern[row_i][col_i] = "#" if stored_val == "." else "."
            # Check if a new column reflection line has appeared
            new_rcl = new_reflection_line(
                base_reflecting_column_lines, pattern.reflecting_column_lines()
            )
            if new_rcl is not None:
                result += calculate_reflection_score([new_rcl], [])
                break
            # Check for rows
            new_rrl = new_reflection_line(
                base_reflecting_row_lines, pattern.reflecting_row_lines()
            )
            if new_rrl is not None:
                result += calculate_reflection_score([], [new_rrl])
                break
            # Reset changed cell
            pattern[row_i][col_i] = stored_val
    return result


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

""" Advent of Code 2023: Day 18 """

FILE_TO_READ = "18_input"

# Given: "dig plan" with lines in the form of "R 6 (#70c710)" – (U|D|L|R), # steps, color
# Digger digs an "outline"
# Fill in everything "within" the outline

import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Optional


def ranges_overlap(r1: range, r2: range) -> bool:
    """Return True if the ranges touch (my start == other's end) or overlap."""
    return r2.start <= r1.stop and r2.stop >= r1.start


def pop_single_overlap(range_: range, others: list[range]) -> Optional[range]:
    overlaps = list(filter(lambda s: ranges_overlap(s, range_), others))
    if not overlaps:
        return None

    assert len(overlaps) == 1
    # Remove the overlapped range from the list
    return others.pop(others.index(overlaps[0]))


@dataclass
class DigInstruction:
    direction: str
    steps: int
    color: str


@dataclass
class Trench:
    t: dict[int, list[range]] = field(default_factory=lambda: defaultdict(list))
    current_row: int = 0
    current_col: int = 0
    # Covering a row, starting in a column, pointing left or right
    # e.g. `1 : range(1, inf)` would be: [1] . # > > > >
    row_streaks: dict[int, list[range]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def _dig(self, row: int, trench: range) -> None:
        overlapped = pop_single_overlap(trench, self.t[row])
        if overlapped is not None:
            trench = range(
                min(trench.start, overlapped.start),
                max(trench.stop, overlapped.stop),
            )
        self.t[row].append(trench)

    def _new_left_streaks(self, rows: range) -> None:
        # Left streaks are inverse, so our "start" is the range stop!

        # Start a streak (== end the range) just left of the current trench
        streak = range(-sys.maxsize, self.current_col)

        for row in rows:
            # Would this streak hit a trench? Then cut it at the first trench hit.
            if row in self.t:
                rightmost_stop: int = -sys.maxsize
                # Find the rightmost trench that is still left of our streak
                for trench in filter(lambda t: t.stop <= self.current_col, self.t[row]):
                    rightmost_stop = max(rightmost_stop, trench.stop)
                # The stop is exclusive, meaning the trench is one left of it.
                # Our streak's end is our range start (inclusive), so it's placed on the trench stop.
                streak = range(rightmost_stop, streak.stop)

            # Would the cut streak overlap an opposite-facing streak? Then remove the
            # overlapped streak and merge them.
            # As we cut at the nearest trench first, we know that only opposite-facing streaks remain.
            if row in self.row_streaks and (
                (overlapped := pop_single_overlap(streak, self.row_streaks[row]))
                is not None
            ):
                # The overlapped streak must be left of ours
                assert overlapped.start < streak.stop

                # Merge with our streak
                streak = range(overlapped.start, streak.stop)

            self.row_streaks[row].append(streak)

    def _new_right_streaks(self, rows: range) -> None:
        # Start a streak just right of the current trench
        streak = range(self.current_col + 1, sys.maxsize)

        for row in rows:
            # Would this streak hit a trench? Then cut it at the first trench hit.
            if row in self.t:
                leftmost_start: int = sys.maxsize
                # Find the leftmost trench that is still right of our streak
                for trench in filter(lambda t: t.start > self.current_col, self.t[row]):
                    leftmost_start = min(leftmost_start, trench.start)
                # The start is inclusive, meaning the trench is on it.
                # Accordingly, our streak's end (which is exclusive) is placed on it.
                streak = range(streak.start, leftmost_start)

            # Overlaps an opposite-facing streak? Remove and merge
            if row in self.row_streaks and (
                (overlapped := pop_single_overlap(streak, self.row_streaks[row]))
                is not None
            ):
                # The overlapped streak must be right of ours
                assert overlapped.stop >= streak.start

                # Merge with our streak
                streak = range(streak.start, overlapped.stop)

            self.row_streaks[row].append(streak)

    def _cut_overlapped_streak(self, direction: str, covered_cols: range):
        """Remove any previous streaks that are now overlapped by our trench."""
        overlapped = pop_single_overlap(
            covered_cols, self.row_streaks[self.current_row]
        )
        if overlapped is None:
            return

        if direction == "L":
            assert covered_cols.stop == overlapped.stop
            cut = range(overlapped.start, covered_cols.start)
        else:
            assert direction == "R"
            assert covered_cols.start == overlapped.start
            cut = range(covered_cols.stop, overlapped.stop)
        self.row_streaks[self.current_row].append(cut)

    def dig(self, dig_instruction: DigInstruction) -> None:
        covered_cols = None

        match dig_instruction.direction:
            case "R":
                new_col = self.current_col + dig_instruction.steps
                covered_cols = range(self.current_col + 1, new_col + 1)
                self._dig(self.current_row, covered_cols)
                self._cut_overlapped_streak(dig_instruction.direction, covered_cols)
                self.current_col = new_col
            case "L":
                new_col = self.current_col - dig_instruction.steps
                covered_cols = range(new_col, self.current_col)
                self._dig(self.current_row, covered_cols)
                self._cut_overlapped_streak(dig_instruction.direction, covered_cols)
                self.current_col = new_col
            case "D":
                new_row = self.current_row + dig_instruction.steps
                covered_rows = range(self.current_row + 1, new_row + 1)
                for r in covered_rows:
                    self._dig(r, range(self.current_col, self.current_col + 1))
                # Left-facing streaks
                self._new_left_streaks(covered_rows)
                self.current_row = new_row
            case "U":
                new_row = self.current_row - dig_instruction.steps
                covered_rows = range(new_row, self.current_row)
                for r in covered_rows:
                    self._dig(r, range(self.current_col, self.current_col + 1))
                # Right-facing streaks
                self._new_right_streaks(covered_rows)
                self.current_row = new_row
            case _:
                raise NotImplementedError()


def parse_line(line: str) -> DigInstruction:
    match = re.fullmatch(r"(U|D|L|R) (\d+) \((#(?:\d|\w+))\)", line)
    return DigInstruction(match.group(1), int(match.group(2)), match.group(3))


def given() -> Iterable[DigInstruction]:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        for line in given_file:
            yield parse_line(line.rstrip("\n"))


# --- Part One --- #


# How many cubes are filled?
# Assumption: Overall, the digger will make a circle in clockwise direction.

# Idea: - While digging, add imaginary "streaks" of interior that start from the trench
#         and extend infinitely far towards the "right".
#       - When the streak is crossed again, add an "end" to it.
#       - Finally, calculate the area of all streaks.


def part_one():
    trench = Trench()

    for dig_instruction in given():
        trench.dig(dig_instruction)

    # Calculate area covered by trenches (trenches are overlap-free)
    trench_area: int = 0
    for row in trench.t.values():
        for a_trench in row:
            trench_area += len(a_trench)

    # Calculate area covered by streaks
    # Warning: Due to our algorithm's logic, some "infinite" streaks remain!
    streak_area: int = 0
    for row in trench.row_streaks.values():
        for streak in row:
            if abs(streak.start) == sys.maxsize or abs(streak.stop) == sys.maxsize:
                continue
            streak_area += len(streak)

    return trench_area + streak_area


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

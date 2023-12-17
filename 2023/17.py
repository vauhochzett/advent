""" Advent of Code 2023: Day 17 """

FILE_TO_READ = "17_input"

# Grid (= city map), with each cell represented by a digit
# Lava is transported through
# Digits stand for the heat loss on that particular cell
# Start: top left. Target: bottom right
# Starting block heat loss is not counted
# Container can move at most three blocks in a single direction, then it must turn
# 90 degrees left or right.
# Also can't reverse direction.

from collections import deque
from dataclasses import dataclass, field
import itertools
from typing import Optional
import math


@dataclass
class Path:
    # coordinates of the steps taken
    steps: list[tuple[int, int]] = field(default_factory=lambda: [(0, 0)])
    heat_loss: int = 0
    # last three direction commands
    last_three_directions: deque[tuple[int, int]] = field(
        default_factory=lambda: deque(maxlen=3)
    )

    @property
    def head(self) -> tuple[int, int]:
        return self.steps[-1]

    def copy(self):  # type: () -> Path
        return Path(
            self.steps.copy(), self.heat_loss, self.last_three_directions.copy()
        )

    def step(self, city, d_row, d_col):  # type: (Map, int, int) -> bool
        """Continue this path one step in the given direction."""
        assert d_row == 0 or d_col == 0
        assert abs(d_row) + abs(d_col) == 1

        next_row, next_col = self.head[0] + d_row, self.head[1] + d_col
        # Out of city bounds?
        if next_row not in (range(len(city))) or next_col not in range(len(city[0])):
            return False

        next_direction = (d_row, d_col)
        # Legal step?
        if self.last_three_directions:
            # Reverse?
            last_dr, last_dc = self.last_three_directions[-1]
            if (d_row + last_dr) == 0 and (d_col + last_dc) == 0:
                return False
            # More than three steps in one direction?
            if (
                # We have taken at least three steps...
                len(self.last_three_directions) == 3
                # ...and our three last steps and the next one are all the same.
                and len(set(self.last_three_directions) | set([next_direction])) == 1
            ):
                return False

        next_cell = city[next_row][next_col]
        next_loss = self.heat_loss + next_cell.heat_loss
        # Would we incur more loss than the global maximum?
        if next_loss > city.GLOBAL_MAX:
            return False

        # Next cell was already stepped to more cheaply?
        # TODO The naive solution to this does not work! Even if we can theoretically step here more cheaply, that is just a local optimum! As our stepping is restricted, the path that is cheaper here may become more expensive over the next steps.
        next_cheapest = next_cell.cheapest_way_here
        # if next_cheapest is not None and next_cheapest.heat_loss <= next_loss:
        #     return False

        # Take the step
        self.steps.append((next_row, next_col))
        self.heat_loss = next_loss
        self.last_three_directions.append(next_direction)

        # Add ourselves as the cheapest way to the cell
        # TODO While we disable the trimming above, we cannot assume that we are the cheapest path always.
        if next_cheapest is None or next_cheapest.heat_loss > next_loss:
            next_cell.cheapest_way_here = self.copy()

        # TODO if another path came here before but was more expensive,
        # we could try to kill it

        # If we reached the end, update the global maximum
        if (next_row, next_col) == (len(city), len(city[0])):
            city.GLOBAL_MAX = min(city.GLOBAL_MAX, next_loss)

        return True

    def possible_futures(self, city):  # type: (Map) -> list[Path]
        """Return paths of all possible steps taken from this path."""
        futures = [(self.copy(), r, c) for (r, c) in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
        return [
            future
            for future, d_row, d_col in futures
            if future.step(city, d_row, d_col)
        ]


@dataclass
class Cell:
    heat_loss: int
    cheapest_way_here: Optional[Path] = None


class Map(list):  # list[list[Cell]]
    GLOBAL_MAX: int = math.inf
    def reset_cells(self) -> None:
        for row in self:
            for cell in row:
                cell.cheapest_way_here = None


def given() -> Map:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        lines = [l.rstrip("\n") for l in given_file]
    return Map([[Cell(int(c)) for c in line] for line in lines])


# --- Part One --- #

# Find the path through the grid that incurs the least heat loss.


def part_one():
    city_map: Map = given()

    # 1. Determine global maximum
    maximum_path = Path()
    diagonal_stepper = iter(itertools.cycle([(0, 1), (1, 0)]))
    # We know that the map is square, so this works
    while maximum_path.head != (len(city_map) - 1, (len(city_map[0])) - 1):
        maximum_path.step(city_map, *next(diagonal_stepper))

    city_map.reset_cells()
    city_map.GLOBAL_MAX = maximum_path.heat_loss

    # 2. Exhaustively check map
    paths: deque[Path] = deque([Path()])

    while paths:
        # a. Take next path from front
        path = paths.popleft()

        # b. Take all possible steps
        #    - Deduplicates within itself
        #    - Checks map for cheaper paths
        #    - Kills all inferior paths and returns only the optimum
        #    - May return the empty list
        new_paths = path.possible_futures(city_map)
        paths.extend(new_paths)

    least_heat_loss: int = city_map[-1][-1].cheapest_way_here.heat_loss
    return least_heat_loss


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

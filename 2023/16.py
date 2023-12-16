""" Advent of Code 2023: Day 16 """

FILE_TO_READ = "16_input"

# Grid of empty space (.), mirrors (/, \), and splitters (|, -)
# Light beam starting from top left
# Goes through empty space
# Splitters: If entering pointy end (e.g., >-), goes through, otherwise splits (<->)
# Mirrors: Redirected by 90 degrees

from dataclasses import dataclass, field
import itertools
import numpy as np


@dataclass
class LightPoint:
    # position
    row: int
    col: int
    # direction
    d_row: int
    d_col: int
    def __hash__(self):
        return hash(f"{self.row},{self.col};{self.d_row},{self.d_col}")


@dataclass
class Cell:
    kind: str

    def translate(self, d_row: int, d_col: int) -> list[tuple[int, int]]:
        assert d_row == 0 or d_col == 0
        assert abs(d_row) + abs(d_col) == 1

        # Unchanged
        if (
            self.kind == "."
            or (self.kind == "-" and abs(d_col) == 1)
            or (self.kind == "|" and abs(d_row) == 1)
        ):
            return [(d_row, d_col)]
        # Split (we already check the non-split direction above)
        elif self.kind == "-":
            return [(0, -1), (0, 1)]
        elif self.kind == "|":
            return [(-1, 0), (1, 0)]
        # Mirrored upwards
        elif (self.kind == "/" and d_col == 1) or (self.kind == "\\" and d_col == -1):
            return [(-1, 0)]
        # Mirrored downwards
        elif (self.kind == "/" and d_col == -1) or (self.kind == "\\" and d_col == 1):
            return [(1, 0)]
        # Mirrored left
        elif (self.kind == "/" and d_row == 1) or (self.kind == "\\" and d_row == -1):
            return [(0, -1)]
        # Mirrored right
        elif (self.kind == "/" and d_row == -1) or (self.kind == "\\" and d_row == 1):
            return [(0, 1)]

    def move(self, light: LightPoint) -> list[LightPoint]:
        new_directions = self.translate(light.d_row, light.d_col)
        new_lights = []
        for new_dir in new_directions:
            new_row, new_col = np.array((light.row, light.col)) + np.array(new_dir)
            new_lights.append(LightPoint(new_row, new_col, *new_dir))
        return new_lights


class Grid(list):  # list[list[Cell]]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The previous light positions (considered static)
        self.light_tails: set[LightPoint] = set()
        # The "tip" of the light stream (actively moving)
        self.light_heads: set[LightPoint] = {LightPoint(row=0, col=0, d_row=0, d_col=1)}

    def iterate(self) -> None:
        """Move all light heads one step."""
        new_light_heads = set()
        while self.light_heads:
            lh = self.light_heads.pop()
            for new_head in self[lh.row][lh.col].move(lh):
                # Deduplicate
                if new_head in self.light_tails:
                    continue
                # Check for out of bounds lights
                if new_head.row < 0 or new_head.row >= len(self) or new_head.col < 0 or new_head.col >= len(self[0]):
                    continue
                new_light_heads.add(new_head)
            self.light_tails.add(lh)
        self.light_heads = new_light_heads

    def print(self) -> str:
        result = []
        for row in self:
            result.append([c.kind for c in row])
        for lp in itertools.chain(self.light_heads, self.light_tails):
            row, col = lp.row, lp.col
            if result[row][col] == ".":
                result[row][col] = "#"
        for row in result:
            print("".join(row))


def given() -> Grid:
    grid_lines = []
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        for line in [l.rstrip("\n") for l in given_file]:
            grid_lines.append([Cell(c) for c in list(line)])
    return Grid(grid_lines)


# --- Part One --- #

# How many cells are "energized" (light passing through them)?


def part_one():
    grid = given()
    while grid.light_heads:
        grid.iterate()
    energized = set()
    for lt in grid.light_tails:
        energized.add((lt.row, lt.col))
    return len(energized)


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

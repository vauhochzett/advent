""" Advent of Code 2023: Day 10 """

FILE_TO_READ = "10_input"

# The field is packed with pipes:
# - | is a vertical pipe connecting north and south.
# - - is a horizontal pipe connecting east and west.
# - L is a 90-degree bend connecting north and east.
# - J is a 90-degree bend connecting north and west.
# - 7 is a 90-degree bend connecting south and west.
# - F is a 90-degree bend connecting south and east.
# - . is ground; there is no pipe in this tile.
# - S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

from dataclasses import dataclass, field
import itertools


@dataclass
class Cell:
    n: str  # name
    row: int
    col: int
    distance: int = -1

    def connections(self) -> list[str]:
        match self.n:
            case ".":  # no connection
                return []
            case "|":
                return ["N", "S"]
            case "-":
                return ["W", "E"]
            case "L":
                return ["N", "E"]
            case "J":
                return ["N", "W"]
            case "7":
                return ["S", "W"]
            case "F":
                return ["S", "E"]
            case "S":  # fully connected
                return ["N", "S", "E", "W"]

    def __hash__(self):
        return hash(f"{self.n}{self.row}{self.col}")


@dataclass
class Grid:
    cells: list[list[Cell]] = field(default_factory=list)
    start: Cell = Cell("-1", -1, -1)

    def append_line(self, line: str):
        row: int = len(self.cells)
        self.cells.append([Cell(n, row=row, col=col) for col, n in enumerate(line)])
        if "S" in line:
            self.start = self.get(len(self.cells) - 1, line.index("S"))
            self.start.distance = 0

    def get(self, row: int, col: int) -> Cell:
        return self.cells[row][col]

    def get_connected(self, cell: Cell) -> list[Cell]:
        compass: list[str] = cell.connections()
        compass_to_pointer: dict[str, tuple[int, int]] = {
            "N": (cell.row - 1, cell.col),
            "S": (cell.row + 1, cell.col),
            "E": (cell.row, cell.col + 1),
            "W": (cell.row, cell.col - 1),
        }
        compass_to_mirror: dict[str, str] = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E",
        }

        result = []
        for cd in compass:
            pointer = compass_to_pointer[cd]
            # Outside of bounds
            if -1 in pointer:
                continue
            other = self.get(*pointer)
            # Other is not a pipe
            if other.n == ".":
                continue
            # Other does not connect back to us
            if compass_to_mirror[cd] not in other.connections():
                continue
            result.append(other)

        return result

def given() -> Grid:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        lines = [l.rstrip("\n") for l in given_file]
    grid = Grid()
    for line in lines:
        grid.append_line(line)
    return grid


# --- Part One --- #


def part_one():
    grid = given()
    traversed: set[Cell] = {grid.start}
    changed: bool = True
    while changed:
        changed = False
        to_add = set()
        # Traverse one step
        for cell in traversed:
            connected = grid.get_connected(cell)
            dist_from_cell = cell.distance + 1
            # (Re)calculate distance and add to traversed set
            for conn in connected:
                if conn.distance == -1 or conn.distance > dist_from_cell:
                    conn.distance = dist_from_cell
                    changed = True
                to_add.add(conn)
        traversed |= to_add  # union

    # Get cell of maximum distance
    last_cell = grid.start
    for t in traversed:
        if t.distance > last_cell.distance:
            last_cell = t
    return last_cell.distance


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

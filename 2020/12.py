import re
import sys
import time
from enum import Enum
from typing import List, Tuple, Union, cast

# pylint: disable=unsubscriptable-object

# Rain Risk
#
# - Input: Navigation instructions
#   + \w\d+
#     * Move N (north), S (south), E (east), W (west)
#     * Turn L (left), R (right), Move F (forward)
# - Starting position: Unknown, facing east


class MoveShip(Enum):
    FORWARD = "F"


class MoveWaypoint(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    LEFT = "L"
    RIGHT = "R"

    def get_trajectory_base(self) -> Tuple[int, int, int]:
        if self is MoveWaypoint.NORTH:
            return (-1, 0, 0)
        elif self is MoveWaypoint.SOUTH:
            return (1, 0, 0)
        elif self is MoveWaypoint.WEST:
            return (0, -1, 0)
        elif self is MoveWaypoint.EAST:
            return (0, 1, 0)
        elif self is MoveWaypoint.LEFT:
            return (0, 0, -1)
        elif self is MoveWaypoint.RIGHT:
            return (0, 0, 1)
        else:
            raise ValueError(f"Unknown self: {self.name}")


class Instruction:
    def __init__(self, instruction_s: str, value: int) -> None:
        self.value: int = value

        self.action: Union[MoveWaypoint, MoveShip]

        try:
            self.action = MoveWaypoint(instruction_s)
        except ValueError:
            # Intentionally provoke an exception if it does not match either
            self.action = MoveShip(instruction_s)

        if (self.action in [MoveWaypoint.LEFT, MoveWaypoint.RIGHT]) and not (
            self.value % 90 == 0
        ):
            raise ValueError("For LEFT and RIGHT, only multiples of 90 are allowed!")

    def get_trajectory(self) -> Tuple[int, int, int]:
        """
        Translate the contained (action, value) pair to a trajectory.
        Only valid for `MoveWaypoint` instructions.

        Returns: Trajectory in the form of (x, y, turn)
        """
        base_trajectory: Tuple[int, int, int]
        if type(self.action) is MoveShip:
            raise ValueError("Not valid for MoveShip action")

        self.action = cast(MoveWaypoint, self.action)
        base_trajectory = self.action.get_trajectory_base()

        r, c, a = base_trajectory  # row, col, angle
        # For a(ngle), the value is transformed to represent quarter turns with 1
        return (r * self.value, c * self.value, a * (self.value // 90))


class Ship:
    def __init__(self, row: int, col: int, wp_row: int, wp_col: int) -> None:
        self.row: int = row
        self.col: int = col
        self.waypoint_row: int = wp_row
        self.waypoint_col: int = wp_col

    def copy(self):
        # type: () -> Ship
        return Ship(
            row=self.row,
            col=self.col,
            wp_row=self.waypoint_row,
            wp_col=self.waypoint_col,
        )

    def move(self, instruction: Instruction):
        # Move by value * waypoint offset
        if type(instruction.action) is MoveShip:
            trajectory_row: int = instruction.value * self.waypoint_row
            trajectory_col: int = instruction.value * self.waypoint_col
            self.row += trajectory_row
            self.col += trajectory_col
        # Move waypoint by value or turn
        elif type(instruction.action) is MoveWaypoint:
            trajectory: Tuple[int, int, int] = instruction.get_trajectory()
            self.waypoint_row += trajectory[0]
            self.waypoint_col += trajectory[1]

            # We have four options: no change, flip, turn right, turn left
            number_of_turns: int = trajectory[2] % 4
            temp_row: int = self.waypoint_row
            if number_of_turns == 0:  # do nothing
                return
            elif number_of_turns == 1:  # turn right
                # +col (east) -> +row (south) and opposite
                self.waypoint_row = self.waypoint_col
                # -row (north) -> +col (east) and opposite
                self.waypoint_col = -(temp_row)
            elif number_of_turns == 2:  # flip
                self.waypoint_row *= -1
                self.waypoint_col *= -1
            elif number_of_turns == 3:  # turn left
                # +col (east) -> -row (north) and opposite
                self.waypoint_row = -(self.waypoint_col)
                # -row (north) -> -col (west) and opposite
                self.waypoint_col = temp_row
            else:
                raise ValueError(f"More than 3 turns: {number_of_turns}")


t0 = time.perf_counter()

instructions: List[Instruction] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        m = re.fullmatch(r"(\w)(\d+)\n", l)
        if not m:
            raise ValueError(f"Invalid line: {l}")

        ins: str
        val_s: str
        ins, val_s = m.groups()
        val: int = int(val_s)

        instructions.append(Instruction(instruction_s=ins, value=val))

t1 = time.perf_counter()

# Ship: 0, 0; Waypoint: 1 north, 10 east
ship_start: Ship = Ship(row=0, col=0, wp_row=-1, wp_col=10)
ship: Ship = ship_start.copy()

for instruction in instructions:
    ship.move(instruction)

t2 = time.perf_counter()

# Get Manhattan distance between original and final ship position


def manhattan_distance(start: Ship, end: Ship) -> int:
    north_south: int = abs(start.row - end.row)
    east_west: int = abs(start.col - end.col)
    return north_south + east_west


md: int = manhattan_distance(ship_start, ship)

t3 = time.perf_counter()


from util import tf

print(
    f"Manhattan distance = {md}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Move ship: {tf(t2-t1)}\n"
    f"Calculate Manhattan distance: {tf(t3-t2)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)

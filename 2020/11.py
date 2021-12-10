import sys
import time
from typing import Callable, Dict, Iterable, List, Optional, Tuple, cast

# pylint: disable=unsubscriptable-object

# Seating System
#
# - 2D layout
# - Floor (.), empty seat (L), or occupied seat (#)
# - Placement rules
#   + Empty seat with no occupied seats around: Occupied
#   + Occupied seat is emptied if...
#     * 4+ occupied seats adjacent (pt. 1)
#     * 5+ occupied seats visible (pt. 2)
#   + Otherwise: stable
#   + Floor is stable

# Simulate until situation is stable; how many seats are occupied?

t0 = time.perf_counter()


class Position:
    def __init__(self, state: str):
        self.state: str = state
        self.visible_seats: List[Tuple[int, int]] = []
        self._initialized: bool = False

    def set_visible_seats(self, visible: List[Tuple[int, int]]) -> None:
        self.visible_seats = visible
        self._initialized = True

    def is_occupied_seat(self) -> bool:
        return self.state == "#"

    def is_empty_seat(self) -> bool:
        return self.state == "L"

    def is_seat(self) -> bool:
        return self.is_occupied_seat() or self.is_empty_seat()

    def get_visible_seats(self, seat_map):
        # type: (List[List[Position]]) -> List[Position]
        if not self._initialized:
            raise RuntimeError()
        return [seat_map[i][j] for i, j in self.visible_seats]


seat_map: List[List[Position]] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        seat_map.append([Position(state=s) for s in l[:-1]])


def iterate(seat_map: List[List[Position]]) -> Iterable[Tuple[int, int, Position]]:
    for i in range(len(seat_map)):
        for j in range(len(seat_map[i])):
            yield i, j, seat_map[i][j]


t1 = time.perf_counter()


def get_seat_positions(seat_map: List[List[Position]]) -> Dict[int, List[int]]:
    seat_positions: Dict[int, List[int]] = {i: [] for i in range(len(seat_map))}

    for i, j, position in iterate(seat_map):
        if position.is_seat():
            seat_positions[i].append(j)

    return seat_positions


def simulate_seat(row: int, col: int, seat_limit: int) -> Optional[str]:
    global seat_map
    own_seat: Position = seat_map[row][col]

    visible_seats: List[Position] = own_seat.get_visible_seats(seat_map)
    occupied: int = sum([1 if s.is_occupied_seat() else 0 for s in visible_seats])

    if own_seat.is_empty_seat() and occupied == 0:
        return "#"
    elif own_seat.is_occupied_seat() and occupied >= seat_limit:
        return "L"
    else:
        return None


def simulate(seat_positions: Dict[int, List[int]], seat_limit: int) -> bool:
    """ Simulate one round. Returns flag denoting if any change happened. """
    global seat_map

    # We need a copy to not influence later seats with in-place modifications.
    changes: List[Tuple[int, int, str]] = []

    for i, js in seat_positions.items():
        # change_occurred |= any([simulate_seat(seat_map_copy, row=i, col=j) for j in js])
        for j in js:
            if change := simulate_seat(row=i, col=j, seat_limit=seat_limit):
                changes.append((i, j, change))

    for i, j, new_state in changes:
        seat_map[i][j].state = new_state

    return len(changes) > 0


seat_positions: Dict[int, List[int]] = get_seat_positions(seat_map=seat_map)

t2 = time.perf_counter()

# Set visible seats

# Part 1: All surrounding seats
def get_surrounding_seats(row: int, col: int) -> List[Tuple[int, int]]:
    """ Get seats that immediately neighbor the given coordinate. """
    min_row: int = max(0, row - 1)
    min_col: int = max(0, col - 1)
    max_row: int = min(row + 1, len(seat_map) - 1)
    max_col: int = min(col + 1, len(seat_map[max_row]) - 1)

    seats: List[Tuple[int, int]] = []

    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if i == row and j == col:
                continue

            if seat_map[i][j].is_seat():
                seats.append((i, j))

    return seats


# Part 2: The first seat in each direction
def get_first_seat_in_direction(
    row: int, col: int, direction: Tuple[int, int]
) -> Optional[Tuple[int, int]]:
    global seat_map
    r: int = row
    c: int = col
    while True:
        r += direction[0]
        c += direction[1]
        # Reached the end of the map
        if r < 0 or r >= len(seat_map) or c < 0 or c >= len(seat_map[r]):
            return None

        if seat_map[r][c].is_seat():
            return r, c


def get_first_seats_in_each_direction(row: int, col: int) -> List[Tuple[int, int]]:
    seats: List[Tuple[int, int]] = []
    for direction in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        direction = cast(Tuple[int, int], direction)
        if seat := get_first_seat_in_direction(row, col, direction):
            seats.append(seat)
    return seats


def set_visible_seats(
    seat_positions: Dict[int, List[int]],
    seat_getter: Callable[[int, int], List[Tuple[int, int]]],
):
    global seat_map
    for i, js in seat_positions.items():
        for j in js:
            seat_map[i][j].set_visible_seats(seat_getter(i, j))


seat_limit: int

# Part 1
# seat_limit = 4
# set_visible_seats(seat_positions, seat_getter=get_surrounding_seats)
# Part 2
seat_limit = 5
set_visible_seats(seat_positions, seat_getter=get_first_seats_in_each_direction)

t3 = time.perf_counter()

while simulate(seat_positions, seat_limit=seat_limit):
    pass

t4 = time.perf_counter()

occupied_seats: int = sum(
    [sum([p.is_occupied_seat() for p in row]) for row in seat_map]
)

t5 = time.perf_counter()


from util import tf

print(
    f"Part 2: Occupied seats = {occupied_seats}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Get seat positions: {tf(t2-t1)}\n"
    f"Get neighbors: {tf(t3-t2)}\n"
    f"Simulate: {tf(t4-t3)}\n"
    f"Count occupied seats: {tf(t5-t4)}\n"
    f"=====\n"
    f"Total: {tf(t5-t0)}"
)

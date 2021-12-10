import sys
import time
from typing import List, Tuple

# Binary Boarding
#
# In: FBFBBFFRLR
# First 7: F / B; specify 1 / 128 rows (numbered 0-127).
# Last 3:  L / R; specify 1 / 8   columns
#
# Seat ID: ROW * 8 + COL

# For each boarding pass, get column and row
# Then, calculate seat ID
# Derive highest ID


# Functions


def _get_position(spec: str, upper_key: str, lowest: int, highest: int) -> int:
    for s in spec:
        difference: int = highest - lowest
        # half defines the index between both halves
        # int(x) is slightly faster than math.floor(x)
        half: int = int(highest - (difference / 2))
        # upper half = round up
        if s == upper_key:
            lowest = half + 1
        # lower half = round down
        else:
            highest = half

    return lowest


def get_row_col(specification: str) -> Tuple[int, int]:

    row_spec: str = specification[:7]
    col_spec: str = specification[7:]

    row: int = _get_position(row_spec, "B", lowest=0, highest=127)
    col: int = _get_position(col_spec, "R", lowest=0, highest=7)

    return row, col


def get_seat_id(row: int, col: int) -> int:
    return row * 8 + col


# Main algo

t0 = time.perf_counter()

# What is the highest seat ID on a boarding pass?

highest: int = 0
ids: List[int] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        row: int
        col: int
        row, col = get_row_col(l)
        id: int = get_seat_id(row=row, col=col)
        ids.append(id)
        if id > highest:
            highest = id

t1 = time.perf_counter()

# What is your own ID? It should be...
# - missing from the list
# - smaller than the highest ID
# - but both the ID -1 and +1 from it should exist in the list.

own: int = -1

for i in range(highest + 1):
    if i not in ids:
        if (i - 1 in ids) and (i + 1 in ids):
            own = i

t2 = time.perf_counter()


from util import tf

print(
    f"Own ID: {own}\n"
    f"Highest ID: {highest}\n\n"
    f"Find highest: {tf(t1-t0)}\n"
    f"Find own: {tf(t2-t1)}\n"
    f"Total: {tf(t2-t0)}"
)

import math
import sys
import time
from collections import namedtuple
from typing import List, Tuple

# . = empty, # = tree
#
# ..##.......
# #...#...#..
# .#....#..#.


Slope = namedtuple("Slope", ["slope_w", "slope_h"])


def next_position(pos: Tuple[int, int], slope: Slope) -> Tuple[int, int]:
    """ New position based on given slope """
    h = pos[0] + slope.slope_h
    w = (pos[1] + slope.slope_w) % width
    return (h, w)


def count_trees(slope: Slope) -> int:
    trees_encountered: int = 0
    curr_position: Tuple[int, int] = (0, 0)
    while curr_position[0] < len(t_map):
        # Check if and count tree
        if t_map[curr_position[0]][curr_position[1]] == "#":
            trees_encountered += 1

        # Get next position
        curr_position = next_position(curr_position, slope)

    return trees_encountered


t0 = time.perf_counter()

t_map: List[str] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        t_map.append(l[:-1])

height: int = len(t_map)
width: int = len(t_map[0])

# Slopes: width, height
slopes: List[Slope] = [
    Slope(slope_w=1, slope_h=1),
    Slope(slope_w=3, slope_h=1),
    Slope(slope_w=5, slope_h=1),
    Slope(slope_w=7, slope_h=1),
    Slope(slope_w=1, slope_h=2),
]

t1 = time.perf_counter()

trees_encountered: List[int] = []

for slope in slopes:
    trees_encountered.append(count_trees(slope))

t2 = time.perf_counter()

# Starting at the top-left corner of your map and following a given slope,
# how many trees would you encounter?
print(
    f"Result: {math.prod(trees_encountered)}\n\n"
    f"Slopes and trees: {list(zip(slopes, trees_encountered))}\n\n"
    f"File read: {(t1-t0)*1000} ms\nAlgorithm: {(t2-t1)*1000} ms\n"
    f"Total: {(t2-t0)*1000} ms"
)

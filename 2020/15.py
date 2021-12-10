import sys
import time
from typing import Dict, List

# pylint: disable=unsubscriptable-object

# Rambunctious Recitation
#
# - Puzzle input: Starting numbers
# - Memory game
# - Players take turns saying numbers
#   + Start from starting number
#   + Then consider last spoken number
#     * If it was spoken for the first time, say 0
#     * Else, say number of turns since the number was last spoken

# Part 1: Find 2020th number spoken
# Part 2: Find 30_000_000th number spoken

t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    lines: List[str] = f.readlines()

first_line_cut: str = lines[0][:-1]
starting_numers: List[int] = [int(n) for n in first_line_cut.split(",")]
cached_number: int = starting_numers[-1]
numbers: Dict[int, int] = {n: i for (i, n) in enumerate(starting_numers[:-1])}

t1 = time.perf_counter()

current_index: int = len(numbers)

number_2020: int = -1
number_30000000: int = -1

while True:
    next_number: int
    try:
        last_spoken_index: int = numbers[cached_number]
        next_number = current_index - last_spoken_index
    except KeyError:
        next_number = 0

    numbers[cached_number] = current_index
    current_index += 1
    cached_number = next_number

    # Index is 0-based, count is 1-based
    numbers_spoken: int = 1 + current_index

    if numbers_spoken == 2020:
        number_2020 = cached_number
        t2 = time.perf_counter()
    elif numbers_spoken >= 30000000:
        number_30000000 = cached_number
        break

t3 = time.perf_counter()


from util import tf

print(
    f"Part 1: 2020th number = {number_2020}\n"
    f"Part 2: 30,000,000th number = {number_30000000}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Part 1: Find 2020th: {tf(t2-t1)}\n"
    f"Part 2: 30,000,000th: {tf(t3-t2)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)

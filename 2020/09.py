import sys
import time
from itertools import combinations
from typing import List

# Encoding Error
#
# XMAS encoding
# - preamble of 25 numbers
# - any following number must be sum of two numbers from the preamble
# - sliding window, so for each index, the previous 25 numbers are its preamble

# Part 1: Find the first number that does not correspond to the encoding

buffer_size: int = int(sys.argv[2])
numbers: List[int] = []


def valid_number(num: int, buffer: List[int]) -> bool:
    for x, y in combinations(buffer, 2):
        if x + y == num:
            return True

    return False


t0 = time.perf_counter()

invalid_value: int = -1

with open(sys.argv[1], "r") as f:
    for l in f:
        value: int = int(l[:-1])

        # Only start checking when buffer is large enough
        if (
            (len(numbers) >= buffer_size)
            and (invalid_value == -1)
            and (
                not valid_number(value, numbers[-buffer_size:])
            )  # slice until end, as number is not appended yet
        ):
            invalid_value = value

        numbers.append(value)

t1 = time.perf_counter()

# Part 2: Find encryption weakness:
#   a) Identify the first contiguous set of numbers that sum up to the invalid number.
#   b) Add together the smallest and largest number in the range.


def find_range() -> List[int]:
    for i in range(len(numbers)):
        for j in range(i + 2, len(numbers) + 1):
            found_rng: List[int] = numbers[i:j]
            range_sum: int = sum(found_rng)
            if range_sum == invalid_value:
                return found_rng

    raise RuntimeError("NOT FOUND!")


found_rng: List[int] = find_range()
encryption_weakness: int = min(found_rng) + max(found_rng)

t2 = time.perf_counter()


from util import tf

print(
    f"Part 1: Invalid number = {invalid_value}\n"
    f"Part 2: Encryption weakness = {encryption_weakness}\n"
    f"\n"
    f"Parse file and find invalid value: {tf(t1-t0)}\n"
    f"Identify encryption weakness: {tf(t2-t1)}\n"
    f"=========\n"
    f"Total: {tf(t2-t0)}"
)

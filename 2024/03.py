"""Advent of Code 2024: Day 3"""

import re

# --- Part One --- #


def part_one(given: str) -> int:
    summed = 0
    for valid_instruction in re.finditer(r"mul\((\d+)\,(\d+)\)", given):
        first, second = [int(group) for group in valid_instruction.groups()]
        summed += first * second
    return summed


# --- Part Two --- #


def part_two(given):
    summed = 0
    pattern = r"(mul\((\d+)\,(\d+)\))|(do(n't)?\(\))"
    enabled = True
    for valid_instruction in re.finditer(pattern, given):
        found_mul, first, second, found_do, _ = valid_instruction.groups()

        # Process enabled/disabled
        if found_do is not None:
            enabled = found_do == "do()"
            continue

        if not enabled:
            continue

        assert found_mul is not None

        first, second = int(first), int(second)
        summed += first * second
    return summed


# --- Main Program --- #


with open("03_input", encoding="utf-8") as fh:
    given = "".join(fh.readlines())

print(f"Part One: {part_one(given)}")
print(f"Part Two: {part_two(given)}")

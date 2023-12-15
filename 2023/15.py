""" Advent of Code 2023: Day 15 """

FILE_TO_READ = "15_input"

# HASH algorithm: Turn string of characters into a single value in range [0, 255]
# - Start at 0
# - Increase the current value by the ASCII code of the next character
# - Multiply by 17
# - Set the current value to the remainder of dividing itself by 256


from typing import Iterable


def HASH(value: str) -> int:
    result: int = 0
    for char in value:
        result += ord(char)
        result *= 17
        result %= 256
    return result


def given() -> Iterable[str]:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        lines = given_file.readlines()
    assert len(lines) == 1
    line = lines[0].rstrip("\n")
    yield from line.split(",")


# --- Part One --- #


def part_one():
    summed_hashes: int = 0
    for value in given():
        summed_hashes += HASH(value)
    return summed_hashes


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

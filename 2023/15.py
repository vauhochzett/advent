""" Advent of Code 2023: Day 15 """

FILE_TO_READ = "15_input"

# HASH algorithm: Turn string of characters into a single value in range [0, 255]
# - Start at 0
# - Increase the current value by the ASCII code of the next character
# - Multiply by 17
# - Set the current value to the remainder of dividing itself by 256


from dataclasses import dataclass
import re
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


# HASHMAP sequence ;)

# Manipulate lenses
# - Set of 256 boxes, labeled 0–255
# - Each operation targets box HASH(operation)
# - xx=5 adds (or replaces) a lens labeled "xx" with focal strength 5
# - xx- removes a lens labeled "xx" if it exists
# - Lenses are added to the back of the list

# Calculate focusing power
# Multiply: (1 + box number) * (1-based slot number) * (focal length)


@dataclass
class Lens:
    label: str
    focal_length: int

    def focusing_power(self, box_no: int, slot_no: int) -> int:
        return (1 + box_no) * slot_no * self.focal_length


class Box(list):  # list[Lens]
    def focusing_power(self, box_no: int) -> int:
        result: int = 0
        for i, lens in enumerate(self, start=1):
            result += lens.focusing_power(box_no, slot_no=i)
        return result


def split_operation(operation: str) -> tuple[str, str]:
    match = re.fullmatch(r"(\w+)((?:-|=)\d*)", operation)
    return match.group(1), match.group(2)


def operate(box: Box, label: str, action: str) -> None:
    """Perform `action` with lens `label` on `box`."""
    index: int = -1
    for i, lens in enumerate(box):
        if lens.label == label:
            index = i

    if action == "-":
        if index == -1:
            return
        box.pop(index)
        return

    assert action.startswith("=")
    focal_length = int(action[1:])
    if index == -1:
        box.append(Lens(label, focal_length))
        return
    box[index].focal_length = focal_length


def part_two():
    boxes: dict[int, Box] = dict()
    for number in range(256):
        boxes[number] = Box()

    # Perform lens changes on boxes
    for value in given():
        label, action = split_operation(value)
        box_id = HASH(label)
        operate(boxes[box_id], label, action)

    # Calculate the focusing power
    focusing_power: int = 0
    for box_no, box in boxes.items():
        focusing_power += box.focusing_power(box_no=box_no)
    return focusing_power


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

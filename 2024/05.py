"""Advent of Code 2024: Day 05"""

from collections import defaultdict
from dataclasses import dataclass, field
from functools import total_ordering

# --- Part One --- #


@dataclass
class BeforeAndAfter:
    befores: list[int] = field(default_factory=list)
    afters: list[int] = field(default_factory=list)


def is_valid(befores_and_afters: dict[int, BeforeAndAfter], update: list[int]):
    for i, num in enumerate(update):
        if i == len(update) - 1:
            break
        for other in update[i + 1 :]:
            if other in befores_and_afters[num].befores:
                return False
            if num in befores_and_afters[other].afters:
                return False
    return True


def part_one(
    befores_and_afters: dict[int, BeforeAndAfter], updates: list[list[int]]
) -> int:
    befores_and_afters = get_befores_and_afters(rules)
    summed_middle_page_numbers = 0
    for update in updates:
        if not is_valid(befores_and_afters, update):
            continue
        middle = update[len(update) // 2]
        summed_middle_page_numbers += middle
    return summed_middle_page_numbers


# --- Part Two --- #


@total_ordering
class Order:
    befores_and_afters: dict[int, BeforeAndAfter] = None

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return (
            other.value in befores_and_afters[self.value].afters
            or self.value in befores_and_afters[other.value].befores
        )


def part_two(
    befores_and_afters: dict[int, BeforeAndAfter], updates: list[list[int]]
) -> int:
    summed_middle_page_numbers = 0
    Order.befores_and_afters = befores_and_afters
    for update in updates:
        ordered = sorted(update, key=Order)
        if ordered == update:
            continue
        middle = ordered[len(update) // 2]
        summed_middle_page_numbers += middle
    return summed_middle_page_numbers


# --- Main Program --- #


def get_befores_and_afters(rules: list[tuple[int, int]]) -> dict[int, BeforeAndAfter]:
    befores_and_afters = defaultdict(BeforeAndAfter)
    for first, second in rules:
        befores_and_afters[first].afters.append(second)
        befores_and_afters[second].befores.append(first)
    return befores_and_afters


with open("05_input", encoding="utf-8") as fh:
    all_lines = fh.readlines()

rules = []
for i, line in enumerate(all_lines):
    if line == "\n":
        break
    first, second = line.rstrip().split("|")
    rules.append((int(first), int(second)))

updates = []
for line in all_lines[i + 1 :]:
    updates.append([int(num) for num in line.rstrip().split(",")])

befores_and_afters = get_befores_and_afters(rules)

print(f"Part One: {part_one(befores_and_afters, updates)}")
print(f"Part Two: {part_two(befores_and_afters, updates)}")

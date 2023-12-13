""" Advent of Code 2023: Day 12 """

FILE_TO_READ = "12_input"

# Rows of "spring records" (#.#..??. 1,1,3) indicating which springs function.
# Operational (.), damaged (#), unknown (?)
# Second part is different encoding of the same info: the size of each contiguous
# group (greedy, so maximum size) of damaged springs, in the order of appearance
# in the set.
# Different numbers of arrangements could "fit" the definition. Sum up the number
# of possible arrangements.

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass
class SpringInfo:
    patterns: list[str]  # only (potentially) broken, e.g., ["???", ###"]
    groups: list[int]  # e.g., [1, 1, 3]


def parse_line(line: str) -> SpringInfo:
    pattern_str, group_str = line.split(" ")

    # Split pattern groups
    patterns: list[str] = re.findall(r"[^\.]+", pattern_str)
    # Split group lengths
    groups: list[int] = [int(v) for v in group_str.split(",")]

    return SpringInfo(patterns=patterns, groups=groups)


def given() -> Iterable[SpringInfo]:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        for line in given_file:
            yield parse_line(line.rstrip("\n"))


# --- Part One --- #


def obvious_match(pattern: str, group_size: int) -> bool:
    assert len(pattern) >= group_size

    # Patterns are delimited by periods, so we know this group fully consumes it.
    # E.g., #??, ###, ??? for 3
    if len(pattern) == group_size:
        return True

    # From this point on, if we don't have at least one hash, we cannot be sure.
    if "#" not in pattern:
        return False

    matched = re.fullmatch(r"(\??)(\#+)(\??)", pattern)
    if matched is None:
        return False
    q_left, h_cnt, q_right = [len(group) for group in matched.groups()]

    # Also obvious if we already have all hashes even if we have more characters.
    # E.g., ?###, ?###? for 3 (### already found above)
    if h_cnt == group_size:
        return True

    # Also if we only have question marks on one side, as we then cannot move the group.
    # E.g., ?##, ?????##, #???? for 3
    return q_left == 0 or q_right == 0


def remove_obvious_matches(
    patterns: list[str], groups: list[int], check_index: int
) -> None:
    """Remove all pattern-group pairs where the `pattern` has exactly `group` hashes."""
    while True:
        if len(patterns) == 0:
            assert len(groups) == 0
            return
        if not obvious_match(patterns[check_index], groups[check_index]):
            return
        patterns.pop(check_index)
        groups.pop(check_index)


def possible_arrangements(pattern: str, group_sizes: list[int]) -> int:
    """Recursively count maximum number of arrangements for given group sizes in the pattern.
    Consumes group sizes that have been matched and removes them from the given list.
    Cuts off the matched part from the pattern and returns it."""
    arrangement_count: int = 0

    for group_size in group_sizes:
        # If there is not enough question marks in the beginning to place our group
        # (would require group_size + 1, as we need at least one delimiter), we know
        # the group must contain the hash.
        if "#" in pattern[: group_size + 1]:
            subpattern = re.match(r"^(\?*\#+\??)", pattern).group(1)
            breakpoint()
            if obvious_match(subpattern, group_size):
                arrangement_count += 1
                return arrangement_count + possible_arrangements(
                    pattern[len(subpattern) :], group_sizes[1:]
                )

            raise NotImplementedError()


def count_arrangement_options(patterns: list[str], group_sizes: list[int]) -> int:
    assert len(group_sizes) >= len(patterns)

    # Remove all pattern-group pairs from the outside that are obvious
    remove_obvious_matches(patterns, group_sizes, 0)
    remove_obvious_matches(patterns, group_sizes, -1)

    # All matches were obvious
    if not patterns and not group_sizes:
        return 1

    # Each pattern must correspond to one group (also handles case of both lists being empty)
    if len(patterns) == len(group_sizes):
        result += sum(
            [possible_arrangements(p, [g]) for p, g in zip(patterns, group_sizes)]
        )
        return result

    # At least one group more than patterns, so we need to resolve
    result += possible_arrangements(patterns.pop(0), group_sizes)

    # Finished
    if len(patterns) == 0:
        return result

    # Recursively check the other groups (we recurse so that we can again remove obvious matches)
    result += count_arrangement_options(patterns[1:], group_sizes)
    return result


def part_one():
    sum_of_arrangement_options: int = 0
    for spring_info in given():
        sum_of_arrangement_options += count_arrangement_options(
            spring_info.patterns, spring_info.groups
        )
    return sum_of_arrangement_options


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

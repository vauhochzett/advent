import sys
import time
from typing import List, Tuple, overload

# Ticket Translation
#
# - Field rules for tickets
#   + "class: 1-3 or 5-7"
# - Ticket: Single CSV line
#   + Values in order of appearance
#   + Between tickets, order is the same
# - Find *completely* invalid tickets
#   + Have values which aren't valid in *any* field
#   + Position or field is irrelevant

# Part 1: Find ticket scanning error rate: Sum of completely invalid values.


class Ticket:
    def __init__(self, values: List[int]) -> None:
        self.values = values


class Rule:
    def __init__(self, field_name: str, valid_ranges: List[Tuple[int, int]]) -> None:
        self.field_name: str = field_name
        # TODO IDEAS: Merge ranges, store all valid values (lookup with "in"), ...
        self.valid_ranges: List[Tuple[int, int]] = valid_ranges

    @overload
    def is_valid(self, value: int) -> bool:
        raise NotImplementedError()

    @overload
    def is_valid(self, ticket: Ticket) -> bool:
        raise NotImplementedError()

    @staticmethod
    def from_string(rule_string):
        # type: (str) -> Rule
        raise NotImplementedError()


# Parsing:
# 1. Get rules
# 2. Get own ticket
# 3. Get other tickets

t0 = time.perf_counter()

rules_parsed: bool = False
own_ticket_parsed: bool = False

rules: List[Rule] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        if not rules_parsed:
            if l == "\n":
                rules_parsed = True
                continue

        pass

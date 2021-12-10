import re
import sys
import time
from collections import namedtuple
from typing import Dict, List, Tuple

# Handy Haversacks
#
# - bags must be color-coded
# - bags must contain specific quantities of other color-coded bags
#
# - own bag is shiny gold
# - to carry it in at least one other bag, how many colors would eventually be valid for the outermost bag?
#
# Test code
# 1. bright white -> shiny gold
# 2. muted yellow -> shiny gold (+x)
# 3. dark orange -> bright white -> shiny gold
#                `-> muted yellow -> shiny gold
# 4. light red -> bright white -> shiny gold
#              `-> muted yellow -> shiny gold

# A) Read and parse rules, build bag container rule tree; important: allow traversal in both directions!

# parents: List[str], children: Dict[str, int]
BagRule = namedtuple("BagRule", ["parents", "children"])

bag_name_ptn = r"(\w|\s)+"


def parse_rule(rule_definition: str) -> Tuple[str, BagRule]:
    m1 = re.fullmatch(f"({bag_name_ptn})" r" bags contain (.+)\.", l[:-1])
    if not m1:
        raise ValueError()

    parent: str
    rule: str
    parent, _, rule = m1.groups()

    bag_rule: BagRule = BagRule(parents=[], children=dict())

    if rule == "no other bags":
        # Empty rule means no children defined
        return parent, bag_rule

    while rule:
        m2 = re.fullmatch(r"(\d+)" f" ({bag_name_ptn})" r" bags*(, (.+))*", rule)
        if not m2:
            raise ValueError()
        number: str
        kind: str
        # bag_name_ptn contains an extra group, and we are only interested in the inner group at the end
        number, kind, _, _, rule = m2.groups()

        # Save rule
        bag_rule.children[kind] = int(number)

    # We are done when all rules have been parsed and saved into `bag_rule`
    return parent, bag_rule


t0 = time.perf_counter()

bag_containment: Dict[str, BagRule] = dict()

# First, we parse all in one direction (parent -> child)
with open(sys.argv[1], "r") as f:
    for l in f:
        parent: str
        rule: BagRule
        parent, rule = parse_rule(l[:-1])
        # We assume that only one rule line exists per parent
        bag_containment[parent] = rule

# Second, we add the (child -> parent) relationships

t1 = time.perf_counter()

for parent, rule in bag_containment.items():
    for child, _ in rule.children.items():
        bag_containment[child].parents.append(parent)


# B / PART 1: How many potential parent bags exist for a shiny gold bag?

t2 = time.perf_counter()


def get_parent_paths(bag: str) -> List[List[str]]:
    """ Return a list of paths from this bag to all potential root bags. """
    parent_paths: List[List[str]] = list()

    # Recursion end: No potential parents
    #   => Skips for loop and returns empty list

    for parent in bag_containment[bag].parents:
        # a) Add path up to this parent
        parent_paths.append([bag, parent])

        # b) Recurse and add paths beyond this parent
        for beyond_path in get_parent_paths(parent):
            # Each beyond path starts with the given parent
            parent_paths.append([bag, *beyond_path])

    return parent_paths


# # First, we get all possible paths that end in shiny gold.
# paths: List[List[str]] = get_parent_paths("shiny gold")
# # Second, we remove duplicates and count.
# t3 = time.perf_counter()
# roots: Set[str] = {p[-1] for p in paths}
# t4 = time.perf_counter()

# B / PART 2: How many bags must a shiny gold bag contain?


def count_children(bag: str) -> int:
    children: Dict[str, int] = bag_containment[bag].children

    sum: int = 0

    # Recurse; recursion end is reached if no more children are available
    for child, child_count in children.items():
        # For each child, add the sum of its children plus one of myself
        sum += child_count * (1 + count_children(child))

    return sum


t3 = time.perf_counter()
# Traverse through all children and sum up
children_count: int = count_children("shiny gold")

t4 = time.perf_counter()


from util import tf

print(
    f"Number of children: {children_count}\n\n"
    f"Parse file and add p -> c relationships: {tf(t1-t0)}\n"
    f"Traverse to get c -> p relationships: {tf(t2-t1)}\n"
    f"Get all parent paths: {tf(t3-t2)}\n"
    f"Get number of children: {tf(t4-t3)}\n"
    f"=========\n"
    f"Total: {tf(t4-t0)}"
)

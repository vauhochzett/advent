""" Advent of Code 2023: Day 8 """

FILE_TO_READ = "08_input"

import re
import itertools
from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    left: str
    right: str

    def step(self, instruction: str):
        if instruction == "R":
            return self.right
        else:
            return self.left

    def __hash__(self):
        return hash(self.name + self.left + self.right)


def parse_node(line: str) -> Node:
    match = re.fullmatch(r"(\w+) = \((\w+)\, (\w+)\)", line)
    return Node(match.group(1), match.group(2), match.group(3))


def given() -> tuple[str, dict[str, Node]]:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        lines = [l.rstrip("\n") for l in given_file.readlines()]
    instructions = lines[0]
    node_dict = {n.name: n for n in [parse_node(l) for l in lines[2:]]}
    return instructions, node_dict


# --- Part One --- #


def part_one():
    instructions, node_dict = given()
    instr_cycle = itertools.cycle(instructions)
    current = node_dict["AAA"]
    steps = 0
    while current.name != "ZZZ":
        instr = next(instr_cycle)
        steps += 1
        if instr == "R":
            current = node_dict[current.right]
        else:
            current = node_dict[current.left]
    return steps


# --- Part Two --- #

# Problem: The naive algorithm takes too long.
# Idea:
#  - We have relatively few instructions that are repeated relatively often.
#  - That means we start again at the first instructions repeatedly.
#  - We can precompute for each node for which steps in the instructions, starting from the first, it would reach a Z node.
#  - In addition, we can precompute the node we would arrive at after completing one round of instructions.
#  - Then we can only compare those sets for all current nodes => if they do not match, we can skip over all instructions


@dataclass
class JumpableNode(Node):
    # name, left, right inherited from Node
    z_node_steps: set[int] = field(default_factory=set)
    rounds: int = 0
    end_node = None  # type: JumpableNode

    @staticmethod
    def from_node(node: Node):
        return JumpableNode(node.name, node.left, node.right)

    def make_jumpable(
        self,
        nj_table,  # type: dict[str, JumpableNode]
        z_node_steps: set[int],
        rounds: int,
        end_node_key: str,
    ):
        self.left = nj_table[self.left]
        self.right = nj_table[self.right]
        self.z_node_steps = z_node_steps
        self.rounds = rounds
        self.end_node = nj_table[end_node_key]

    def step(self, instruction: str):
        if instruction == "R":
            return self.right
        else:
            return self.left

    def __hash__(self):
        return hash(self.name + self.left.name + self.right.name)


def jump_table(
    instructions: str, node_dict: dict[str, Node]
) -> dict[str, JumpableNode]:
    """Calculate for each node:
    - After which steps of the instructions would we reach a Z node?
    - Which node would we end up with if we completed one round of instructions starting here?
    """
    nj_table = {key: JumpableNode.from_node(value) for key, value in node_dict.items()}
    for start_node in nj_table.values():
        z_node_steps = set()
        stepped_to = start_node
        steps = 0
        ins_iter = iter(instructions)
        try:
            while True:
                # Could be ourselves (before stepping)
                if stepped_to.name.endswith("Z"):
                    z_node_steps.add(steps)
                instruction = next(ins_iter)
                steps += 1
                stepped_to = node_dict[stepped_to.step(instruction)]
        except StopIteration:
            pass
        start_node.make_jumpable(
            nj_table=nj_table,
            z_node_steps=z_node_steps,
            rounds=1,
            end_node_key=stepped_to.name,
        )
    return nj_table


def check_jump_intersection(current_nji: list[JumpableNode]) -> set[int]:
    """Return the intersection of the number of steps in the instruction set to arrive
    at a Z node for all current nodes."""
    completion_steps: set[int] = current_nji[0].z_node_steps
    for other in current_nji[1:]:
        completion_steps = completion_steps.intersection(other.z_node_steps)
        if not completion_steps:  # cancel early if no more steps remain-
            return set()
    return completion_steps


def skip_to_end(current: list[JumpableNode]) -> list[JumpableNode]:
    """Return a list of all end nodes of the given node list."""
    return [jumpable.end_node for jumpable in current]


def part_two():
    instructions, node_dict = given()
    nj_table = jump_table(instructions, node_dict)
    instructions_count = len(instructions)

    all_current: list[JumpableNode] = list(
        filter(lambda n: n.name.endswith("A"), nj_table.values())
    )
    steps = 0
    while True:
        # 1) First, check if we found a terminating path and return the shortest one
        if completion_steps := check_jump_intersection(all_current):
            return steps + min(completion_steps)

        # 2) If not, skip ahead by the number of rounds that we compared.
        all_current = skip_to_end(all_current)

        # 3) Finally, replace each node's end node with it's end node's end node
        # (transitive relationship). We replace the end node to minimize memory
        # requirements while still maximizing the steps we skip.
        new_end_nodes = dict()  # make a copy to not overwrite while reading
        rounds: int = all_current[0].rounds  # same for all
        for key, nji in nj_table.items():
            # Calculate relative z node steps via current end node
            relative_z_node_steps = set(
                rounds * instructions_count + zns for zns in nji.end_node.z_node_steps
            )
            new_end_nodes[key] = (nji.end_node, relative_z_node_steps)

        for key, (new_end, relative_zns) in new_end_nodes.items():
            # Update jump data in our node
            nj_table[key].z_node_steps |= relative_zns
            nj_table[
                key
            ].rounds *= 2  # rounds always double, as we step all by the same
            nj_table[key].end_node = new_end

        # 4) Update steps – we have skipped over `rounds` of instructions
        steps += rounds * instructions_count
    return steps


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

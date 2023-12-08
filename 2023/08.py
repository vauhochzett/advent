""" Advent of Code 2023: Day 8 """

FILE_TO_READ = "08_input"

import re
import itertools
from dataclasses import dataclass

@dataclass
class Node:
	name: str
	left: str
	right: str

def parse_node(line: str) -> Node:
	match = re.fullmatch(r"(\w+) = \((\w+)\, (\w+)\)", line)
	return Node(match.group(1), match.group(2), match.group(3))

def given() -> tuple[str, list[Node]]:
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		lines = [l.rstrip("\n") for l in given_file.readlines()]
	instructions = lines[0]
	nodes = [parse_node(l) for l in lines[2:]]
	return instructions, nodes

# --- Part One --- #

def part_one():
	instructions, nodes = given()
	node_dict = {
		n.name: n
		for n in nodes
	}
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

def part_two():
	return "NOT IMPLEMENTED"

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

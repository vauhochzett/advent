""" Advent of Code 2023: Day 9 """

FILE_TO_READ = "09_input"

from dataclasses import dataclass
import itertools
import re

@dataclass
class ValueHistory:
	data: list[int]
	def deltas(self):  # type: () -> ValueHistory
		values = []
		for a, b in itertools.pairwise(self.data):
			values.append(b-a)
		return ValueHistory(values)
	def all_zeroes(self) -> bool:
		return all(d == 0 for d in self.data)
	def next_value(self) -> int:
		if self.all_zeroes():
			return 0
		return self.data[-1] + self.deltas().next_value()

def parse_line(line: str) -> ValueHistory:
	return ValueHistory([int(v) for v in line.split(" ")])

def given():
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		for line in given_file:
			yield parse_line(line.rstrip("\n"))

# --- Part One --- #

def part_one():
	sum_of_next_values: int = 0
	for value_history in given():
		sum_of_next_values += value_history.next_value()
	return sum_of_next_values

# --- Part Two --- #

def part_two():
	return "NOT IMPLEMENTED"

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

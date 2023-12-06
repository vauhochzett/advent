""" Advent of Code 2023: Day 5 """

FILE_TO_READ = "05_input"

import re

class Map:
	def __init__(self, source: str, target: str):
		self.source = source
		self.target = target
		self.mappings: list[tuple[int, int, int]] = []

	def add_mapping(self, dest_start: int, source_start: int, length: int):
		self.mappings.append((dest_start, source_start, length))

	def resolve(self, given: int) -> int:
		for dest_start, source_start, length in self.mappings:
			if given in range(source_start, source_start + length):
				return dest_start + (given - source_start)
		return given

	def __repr__(self) -> str:
		return f"Map({self.source}, {self.target}) -> {self.mappings}"

def process_map(lines: list[str]) -> Map:
	descriptor_match = re.fullmatch(r"(\w+)-to-(\w+) map:", lines[0])
	source = descriptor_match.group(1)
	target = descriptor_match.group(2)
	map_ = Map(source, target)
	for definition in lines[1:]:
		map_.add_mapping(*[int(v) for v in definition.split(" ")])
	return map_

def given() -> tuple[list[int], dict[tuple[str, str], Map]]:
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		lines = [l.rstrip("\n") for l in given_file.readlines()]
	seed_definition = [int(s) for s in lines[0][7:].split(" ")]
	maps: dict[str, tuple[str, Map]] = dict()

	# Make sure we catch the last map by also delimiting it with an empty line
	lines.append("")
	to_process = []
	for line in lines[2:]:
		if line == "":
			map_ = process_map(to_process)
			maps[map_.source] = (map_.target, map_)
			to_process = []
			continue
		to_process.append(line)

	return seed_definition, maps

def min_location_from_seeds(seeds, maps) -> int:
	current_level = "seed"
	current_items = seeds.copy()
	while current_level != "location":
		current_level, map_ = maps[current_level]
		current_items = [map_.resolve(item) for item in current_items]
	return min(current_items)

# --- Part One --- #

def part_one():
	seed_definition, maps = given()
	return min_location_from_seeds(seed_definition, maps)

# --- Part Two --- #

def part_two():
	raise NotImplementedError()

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

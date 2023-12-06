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

# --- Part One --- #

def min_location_from_seeds(seeds, maps) -> int:
	current_level = "seed"
	current_items = seeds.copy()
	while current_level != "location":
		current_level, map_ = maps[current_level]
		current_items = [map_.resolve(item) for item in current_items]
	return min(current_items)

def part_one():
	seeds, maps = given()
	return min_location_from_seeds(seeds, maps)

# --- Part Two --- #

from collections import deque

def sort_and_merge_ranges(ranges: list[range]) -> list[range]:
	"""Sort ranges by start and merge overlapping ranges. Return a copy."""
	sorted_ranges = sorted(ranges, key=lambda r: r.start)
	merged_ranges = deque(sorted_ranges[:1])
	for slice_ in sorted_ranges[1:]:
		# slice is disconnected from previous
		if slice_.start > merged_ranges[-1].stop:
			merged_ranges.append(slice_)
			continue

		# slice is contained in previous
		if slice_.stop <= merged_ranges[-1].stop:
			continue

		# slice overlaps and extends -> merge
		merged_ranges[-1] = range(merged_ranges[-1].start, slice_.stop)
	return merged_ranges

def min_locations_efficient(seed_ranges, maps) -> int:
	# Idea: Instead of processing individual items, we can process ranges as a whole
	# - Each map represents a list of ranges plus a transformation for each value (addition by a fixed value)
	# - Meaning, we can simply shift the range ends according to the transformation rule
	# - Difficult step: Slicing the correct ranges in the first place

	range_processing_deque = deque(sorted([range(s, s + l) for s, l in seed_ranges], key=lambda r: r.start))

	current_level = "seed"
	while current_level != "location":
		current_level, map_ = maps[current_level]

		# 1. Slice ranges to match those in the map...
		# 2. ...and transform ranges according to map
		map_ranges = [(range(s, s + l), d-s) for d, s, l in map_.mappings]
		map_ranges.sort(key=lambda r_o: r_o[0].start)

		sliced_ranges = []
		mapr_idx = 0
		map_range = range(-1, -1)

		while len(range_processing_deque) > 0 and mapr_idx < len(map_ranges):

			# Both lists of ranges are overlap free at this point
			cur_range = range_processing_deque.popleft()
			map_range, offset = map_ranges[mapr_idx]

			# Map is already overtaken -> switch to next
			if cur_range.start >= map_range.stop:
				mapr_idx += 1
				# Still needs to be processed
				range_processing_deque.appendleft(cur_range)
				continue

			# Processed range is not covered at all -> add to result unprocessed and continue
			if map_range.start >= cur_range.stop:
				sliced_ranges.append(cur_range)
				continue

			# Slice away segments that fall outside the currently considered map range
			# - left of: add to result unprocessed
			if cur_range.start < map_range.start:
				sliced_ranges.append(range(cur_range.start, map_range.start))  # stop is exclusive
				cur_range = range(map_range.start, cur_range.stop)

			# - right of: re-add to deque
			if cur_range.stop > map_range.stop:
				range_processing_deque.appendleft(range(map_range.stop, cur_range.stop))
				cur_range = range(cur_range.start, map_range.stop)

			# The remaining range is fully covered by the map rule and can be processed by adding the offset.
			processed_rest = range(cur_range.start + offset, cur_range.stop + offset)
			sliced_ranges.append(processed_rest)

		# Add any unprocessed ranges if they exist
		sliced_ranges.extend(range_processing_deque)

		# 3. Sort and merge ranges to purge overlap before next step
		sorted_and_merged_ranges = sort_and_merge_ranges(sliced_ranges)
		range_processing_deque = deque(sorted_and_merged_ranges)

	# 4. Get smallest value of smallest final range
	return(range_processing_deque[0].start)

def part_two():
	seed_definition, maps = given()
	seed_ranges = []
	for i in range(0, len(seed_definition) - 1, 2):
		range_start = seed_definition[i]
		range_len = seed_definition[i+1]
		seed_ranges.append((range_start, range_len))
	return min_locations_efficient(seed_ranges, maps)

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

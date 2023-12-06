""" Advent of Code 2023: Day 3 """

FILE_TO_READ = "03_input"

import re
import itertools

def given():
	matrix = []
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		for line in given_file:
			matrix.append(list(line.rstrip("\n")))

	# Make our life easy by adding a context line to the first and last line
	empty_line = ["."] * len(matrix[0])
	matrix.insert(0, empty_line)
	matrix.append(empty_line)
	return matrix

def iterate_matrix(matrix) -> list[list[str]]:
	# Check each line plus its context (except for the first and last, because we added those ourselves)
	for i in range(1, len(matrix) - 1):
		# Get "context" (line and adjacent lines)
		full_context = matrix[i-1 : i+2]  # inclusive : exclusive
		current_line = "".join(full_context[1])
		yield (full_context, current_line)

# --- Part One --- #

# Any number adjacent to a symbol (except for ".") is a "part number".
# What is the sum of all part numbers in the engine schematic?

def check_digit(full_context, current_line, start, end) -> int:
	"""Return part number if digit is adjacent to symbol. Otherwise, return 0."""
	context_start = max(0, start - 1)  # start is inclusive
	context_end = min(len(current_line), end)  # end is exclusive
	digit_context = [
		fc[context_start : context_end + 1] for fc in full_context
	]
	for char in itertools.chain.from_iterable(digit_context):
		if char != "." and not re.match(r"\d", char):
			return int(current_line[start : end])
	return 0

def part_one():
	matrix = given()
	sum_of_part_numbers: int = 0

	for full_context, current_line in iterate_matrix(matrix):
		# Get positions of all continuous numbers
		digit_positions = []
		for match in re.finditer(r"\d+", current_line):  # matches are greedy
			digit_positions.append(match.span())

		# Check surroundings of each number
		for start, end in digit_positions:
			sum_of_part_numbers += check_digit(full_context, current_line, start, end)

	return sum_of_part_numbers

# --- Part Two --- #

# Any star ("*") adjacent to exactly two part numbers is a "gear". Its gear ratio is the multiple of the part numbers.
# What is the sum of all the gear ratios?

def check_star(full_context: list[list[str]], position: int):
	# Collect adjacent numbers
	adjacent_part_numbers: list[int] = []
	for line in full_context:
		line_str = "".join(line)
		for match in re.finditer(r"\d+", line_str):
			start, end = match.span()
			# Adjacent if the span is adjacent to `position`
			if position in range(start - 1, end + 1):
				adjacent_part_numbers.append(int(line_str[start : end]))

	if len(adjacent_part_numbers) == 2:
		return adjacent_part_numbers[0] * adjacent_part_numbers[1]

	return 0


def part_two():
	matrix = given()
	sum_of_gear_ratios: int = 0

	for full_context, current_line in iterate_matrix(matrix):
		# Get positions of all star symbols
		star_positions = []
		for match in re.finditer(r"\*", current_line):
			star_positions.append(match.span()[0])

		# Check surroundings of each star
		for position in star_positions:
			sum_of_gear_ratios += check_star(full_context, position)
	return sum_of_gear_ratios


# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

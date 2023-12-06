""" Advent of Code 2023: Day 2 """

FILE_TO_READ = "02_input"

import re

def parse_line(line: str) -> tuple[int, dict[str, int]]:
	"""Transform line to (<id>, (# red, # green, # blue)) tuple."""

	# Given, e.g.: "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
	match = re.fullmatch(r"Game (\d+): (.*)\n", line)
	game_id = int(match.group(1))
	games = match.group(2)

	max_shown: dict[str, int] = {
		"red": 0,
		"green": 0,
		"blue": 0,
	}

	# `games` is, e.g.: "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
	for game in games.split("; "):
		# `shown` is, e.g.: "4 red"
		for shown in game.split(", "):
			match = re.fullmatch(r"(\d+) (\w+)", shown)
			count = int(match.group(1))
			name = match.group(2)
			max_shown[name] = max(max_shown[name], count)

	return (game_id, max_shown)

def given():
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		for line in given_file:
			yield parse_line(line)

# --- Part One --- #

# Which games would be possible with 12 red cubes, 13 green cubes, and 14 blue cubes?
# What is the sum of the IDs of those games?

max_possible: dict[str, int] = {
	"red": 12,
	"green": 13,
	"blue": 14,
}

def part_one():
	sum_of_ids: int = 0
	for game_id, max_shown in given():
		valid = True
		for name, count in max_possible.items():
			if max_shown[name] > count:
				valid = False
		if valid:
			sum_of_ids += game_id
	return sum_of_ids

# --- Part Two --- #

# What is the minimum number of cubes necessary for each game? Multiply them.
# What is the sum of the power (multiplied minimums) for the sets?

def part_two():
	sum_of_powers: int = 0
	for game_id, max_shown in given():
		sum_of_powers += max_shown["red"] * max_shown["green"] * max_shown["blue"]
	return sum_of_powers

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

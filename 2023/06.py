""" Advent of Code 2023: Day 6 """

FILE_TO_READ = "06_input"

import itertools
import re

# Races are limited in time.
# Boats have a button that charges the speed, but the time of the race passes.
# How long to hold the button to maximize the traversed distance within the race time?

# remaining_time = race_time - button_hold_time
# speed = button_hold_time (in mm / s)
# we know that distance = speed * time
#   it follows: distance = button_hold_time * remaining_time
# we can replace remaining_time to obtain:
#   distance = button_hold_time * (race_time - button_hold_time)
#   distance = button_hold_time*race_time - button_hold_time^2

# Note that the remaining_time is directly dependent on the button_hold_time.
# Further note that for remaining_time = race_time, button_hold_time = 0; and for button_hold_time = race_time, remaining_time = 0
# That means, we can halve our search space, as the result of the distance function follows a symmetric curve.
# Assumption: The maximum of the curve lies exactly at the halfpoint.

class Race:
	def __init__(self, time: int, distance: int):
		self.time: int = time
		self.distance: int = distance

	def how_far_with(self, button_hold_time: int) -> int:
		"""Return the distance for the given button_hold_time."""
		remaining_time = self.time - button_hold_time
		return button_hold_time * remaining_time

	def __repr__(self) -> str:
		return f"Race(time={self.time}, distance={self.distance})"

# --- Part One --- #

# How many distinct ways exist to win the race based on the button_hold_time?
# Multiply the distinct ways for each race.

def process_number_table(line: str) -> list[int]:
	"""Convert string with a list of numbers separated by arbitrary number of spaces into `int`s."""
	line = line[11:]
	line_normalized = re.sub(" +", " ", line.strip())
	return [int(value) for value in line_normalized.split(" ")]

def given_one():
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		lines = [l.rstrip("\n") for l in given_file.readlines()]
	times = process_number_table(lines[0])
	distances = process_number_table(lines[1])
	races = []
	assert len(times) == len(distances)
	for time, distance in zip(times, distances):
		races.append(Race(time, distance))
	return races

def search_win_bounds(race: Race) -> tuple[int, int]:
	"""Return minimum and maximum button_hold_time to exceed the race distance."""

	# Idea: Binary search between 1 and (race_time // 2)
	lower = 0
	upper = race.time // 2  # floor division
	pairs = list(itertools.pairwise(range(lower, upper + 1)))

	distance_left = -1
	distance_right = -1
	search_window = (0, len(pairs) - 1)

	# We search a pair of button_hold_times for which left doesn't win but right wins
	while True:
		search_cursor = int((search_window[0] + search_window[1] + 1) / 2)  # ceiling division
		left, right = pairs[search_cursor]
		distance_left = race.how_far_with(left)
		distance_right = race.how_far_with(right)

		# Found
		if distance_left <= race.distance and distance_right > race.distance:
			return right, race.time - right

		# Not found -> shift search window
		# - we need to look upwards if we don't win at all
		if distance_right <= race.distance:
			search_window = (search_cursor, search_window[1])
		# - if we win for both, we need to look downwards
		elif distance_left > race.distance:
			search_window = (search_window[0], search_cursor)
		else:
			raise RuntimeError("something went wrong")

def part_one():
	races = given_one()

	number_of_ways = 1

	for race in races:
		lower, upper = search_win_bounds(race)
		number_of_ways *= (upper - lower + 1)

	return number_of_ways

# --- Part Two --- #

def process_number_line(line: str) -> list[int]:
	"""Convert string with a single number separated by arbitrary number of spaces into an `int`."""
	line = line[11:]
	line_normalized = re.sub(" +", "", line.strip())
	return int(line_normalized)

def given_two():
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		lines = [l.rstrip("\n") for l in given_file.readlines()]
	time = process_number_line(lines[0])
	distance = process_number_line(lines[1])
	return Race(time, distance)

def part_two():
	race = given_two()
	lower, upper = search_win_bounds(race)
	return (upper - lower + 1)

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

""" Advent of Code 2023: Day 4 """

FILE_TO_READ = "04_input"

import re

def to_int(nums: str) -> list[int]:
	nums = re.sub(" +", " ", nums.strip())
	return [int(el) for el in nums.split(" ")]

def parse_line(line: str):
	line_match = re.fullmatch(r"Card +(\d+): (.*)", line)
	card_number = int(line_match.group(1))
	winning_numbers, my_numbers = line_match.group(2).split(" | ")
	return card_number, to_int(winning_numbers), to_int(my_numbers)

def given():
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		for line in given_file:
			yield parse_line(line.rstrip("\n"))

def my_winners(winning_numbers: list[int], my_numbers: list[int]) -> list[int]:
	return [my for my in my_numbers if my in winning_numbers]

# --- Part One --- #

# How many of my numbers are winning numbers? The first awards one point, each following one doubles the points.
# What is the sum of the points won for each card?

def part_one():
	total_score: int = 0
	for _, winning_numbers, my_numbers in given():
		card_score: int = 0
		for winner in my_winners(winning_numbers, my_numbers):
			if card_score == 0:
				card_score = 1
			else:
				card_score *= 2
		total_score += card_score
	return total_score

# --- Part Two --- #

# Instead of winning points, we win additional scratchcards.
# For each card i with j winning numbers, we win a copy of each card [i+1, j].
# How many total scratch cards do we end up with?

def part_two():
	all_cards = list(given())
	win_counts = dict()
	card_counts = dict()
	for card_no, winning_numbers, my_numbers in all_cards:
		win_counts[card_no] = len(my_winners(winning_numbers, my_numbers))
		card_counts[card_no] = 1

	for card_no, winning_numbers, my_numbers in all_cards:
		for _ in range(card_counts[card_no]):
			wins = win_counts[card_no]
			for j in range(card_no+1, card_no+1+wins):
				card_counts[j] += 1

	return sum(card_counts.values())

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

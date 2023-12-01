""" Advent of Code 2023: Day 1 """

import re

# --- Part One --- #

def part_one(given):
	summed_calibration_values = 0
	for l in given:
		digits = re.findall(r"\d", l)
		calibration_value = int(digits[0] + digits[-1])
		summed_calibration_values += calibration_value
	return summed_calibration_values

# --- Part Two --- #

def reverse_string(string):
	return "".join(reversed(string))

digit_map = {
	"one": 1,
	"two": 2,
	"three": 3,
	"four": 4,
	"five": 5,
	"six": 6,
	"seven": 7,
	"eight": 8,
	"nine": 9,
}

def convert_digit(string):
	try:
		return int(string)
	except ValueError:
		return digit_map[string]

def part_two(given):
	summed_calibration_values = 0
	for l in given:
		# pattern in form of (\d|one|...)
		dig_pattern = r"(\d|" + "|".join(digit_map.keys()) + ")"
		first_digit = re.search(dig_pattern, l).group(1)
		# to find the last, we search from the back
		# "reversed" pattern in form of (\d|eno|...)
		rev_pattern = r"(\d|" + "|".join(map(reverse_string, digit_map.keys())) + ")"
		last_digit = reverse_string(re.search(rev_pattern, reverse_string(l)).group(1))

		calibration_value = convert_digit(first_digit) * 10 + convert_digit(last_digit)
		summed_calibration_values += calibration_value
	return summed_calibration_values

# --- Main Program --- #

with open("01_input", encoding="utf-8") as fh:
	given = [l.rstrip() for l in fh.readlines()]

print(f"Part One: {part_one(given)}")
print(f"Part Two: {part_two(given)}")

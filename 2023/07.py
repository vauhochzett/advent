""" Advent of Code 2023: Day 7 """

FILE_TO_READ = "07_input"

# Camel Cards

# Card order based on strength: A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
# Hand types based on strength: 5 of a kind, 4 of a kind, full house (3 of a kind + 2 of a different kind), 3 of a kind, 2 pairs, 1 pair, high card (all distinct)
# Second ordering if same strength: Consider cards in order, which hand has a stronger card first?

# Puzzle input: hand + bid
# Winning: bid * rank; where ranks are inversely sorted by strength (weakest = 1, then incrementing by 1, strongest hand = n)

# First, sort into hand types
# Then, within each hand type, sort based on card strength (one by one, not total number of cards)

import re
from collections import Counter
from enum import Enum
from functools import total_ordering

# --- Shared Classes --- #

class HandType(Enum):
	FIVE_OF_KIND = 7
	FOUR_OF_KIND = 6
	FULL_HOUSE = 5
	THREE_OF_KIND = 4
	TWO_PAIRS = 3
	ONE_PAIR = 2
	HIGH_CARD = 1

	def __gt__(self, other):
		return self.value > other.value

@total_ordering
class Card:
	VALUES = None

	def __init__(self, label: str):
		self.label = label

	@property
	def value(self):
		return Card.VALUES[self.label]
	
	def __gt__(self, other) -> bool:
		if not hasattr(other, "label"):
			return NotImplemented
		return self.value > other.value

	def __eq__(self, other) -> bool:
		if not hasattr(other, "label"):
			return NotImplemented
		return self.value == other.value

	def __hash__(self) -> str:
		return hash(self.label)

	def __repr__(self) -> str:
		return repr(self.label)

	def __str__(self) -> str:
		return self.label

class Play:
	"""A play, made up of a hand (list of cards) and a bid (int)."""
	def __init__(self, hand: str, bid: str):
		self.hand: list[Card] = [Card(c) for c in hand]
		self.bid: int = int(bid)

	def __gt__(self, other) -> bool:
		if not isinstance(other, Play):
			return NotImplemented

		if self.hand_type() != other.hand_type():
			return self.hand_type() > other.hand_type()

		for ours, theirs in zip(self.hand, other.hand):
			if ours == theirs:
				continue
			return ours > theirs

	def __repr__(self) -> str:
		return f"Play({self.hand!r}, {self.bid!r})"

# --- Shared Functions --- #

def parse_line(line: str) -> Play:
	return Play(*line.split(" "))

def given():
	with open(FILE_TO_READ, encoding="utf-8") as given_file:
		for line in given_file:
			yield parse_line(line.rstrip("\n"))

def calculate_winnings() -> int:
	total_winnings: int = 0
	for rank, play in enumerate(sorted(given()), start=1):
		total_winnings += rank * play.bid
	return total_winnings

# --- Part One --- #

VALUES_ONE = {
	c: v
	for (v, c) in enumerate(
		[str(v) for v in range(2, 10)] + ["T", "J", "Q", "K", "A"],
		start=2
	)
}

def hand_type_one(play: Play) -> HandType:
	card_counts = Counter()
	for card in play.hand:
		card_counts[card] += 1
	most_often = sorted(card_counts.items(), key=lambda t: t[1], reverse=True)

	# For five of a kind, we only have one element, so our `match` would not work.
	if len(most_often) == 1:
		return HandType.FIVE_OF_KIND

	match most_often[0][1], most_often[1][1]:
		case (4, _):
			return HandType.FOUR_OF_KIND
		case (3, 2):
			return HandType.FULL_HOUSE
		case (3, _):
			return HandType.THREE_OF_KIND
		case (2, 2):
			return HandType.TWO_PAIRS
		case (2, _):
			return HandType.ONE_PAIR
		case _:
			return HandType.HIGH_CARD

def part_one():
	Card.VALUES = VALUES_ONE
	Play.hand_type = hand_type_one
	return calculate_winnings()

# --- Part Two --- #

VALUES_TWO = {
	c: v
	for (v, c) in enumerate(
		["J"] + [str(v) for v in range(2, 10)] + ["T", "Q", "K", "A"],
		start=1
	)
}

def hand_type_two(play: Play) -> HandType:
	base_type = hand_type_one(play)
	joker = Card("J")

	# Cannot be improved by joker
	if base_type == HandType.FIVE_OF_KIND:
		return base_type

	# Other hands can be improved only by joker
	if not joker in play.hand:
		return base_type

	joker_count = play.hand.count(joker)

	# We know that we have at most four of a kind and at least one joker.
	# We resolve by first matching the joker count and then the concrete hand.
	return {
		4: {
			# Only one case possible, as we exclude five of kind above
			HandType.FOUR_OF_KIND: HandType.FIVE_OF_KIND,
		},
		3: {
			# The two other cards are identical: JJJXX -> XXXXX
			HandType.FULL_HOUSE: HandType.FIVE_OF_KIND,
			# The others differ: JJJXY -> XXXXY
			HandType.THREE_OF_KIND: HandType.FOUR_OF_KIND,
		},
		2: {
			# The other three cards are identical: JJXXX -> XXXXX
			HandType.FULL_HOUSE: HandType.FIVE_OF_KIND,
			# Two of the other three cards are identical: JJXXY -> XXXXY
			HandType.TWO_PAIRS: HandType.FOUR_OF_KIND,
			# All three other cards differ: JJXYZ -> XXXYZ
			HandType.ONE_PAIR: HandType.THREE_OF_KIND,
		},
		1: {
			# The other four cards are identical: JXXXX -> XXXXX
			HandType.FOUR_OF_KIND: HandType.FIVE_OF_KIND,
			# Three of the other four cards are identical: JXXXY -> XXXXY
			HandType.THREE_OF_KIND: HandType.FOUR_OF_KIND,
			# The other four cards are two pairs: JXXYY -> XXXYY
			HandType.TWO_PAIRS: HandType.FULL_HOUSE,
			# Two of the other four cards are identical: JXXYZ -> XXXYZ
			HandType.ONE_PAIR: HandType.THREE_OF_KIND,
			# All four other cards differ: JWXYZ -> WWXYZ
			HandType.HIGH_CARD: HandType.ONE_PAIR,
		}
	}[joker_count][base_type]


def part_two():
	Card.VALUES = VALUES_TWO
	Play.hand_type = hand_type_two
	return calculate_winnings()

# --- Main Program --- #

if __name__ == "__main__":
	print(f"Part One: {part_one()}")
	print(f"Part Two: {part_two()}")

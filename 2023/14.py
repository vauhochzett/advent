""" Advent of Code 2023: Day 14 """

FILE_TO_READ = "14_input"

# Fixed rocks (#), rolling rocks (O), and empty space (.)
# "Roll" all O's north
# Load is the 1-based index of the rows counting from the bottom.


import itertools


class Dish(list):
    def rocks_in(self, col: int) -> tuple[list[int], list[int]]:
        """Return a sorted list of indices of hashes in the given column."""
        hashes = []
        boulders = []
        for row_i, row in enumerate(self):
            if row[col] == "#":
                hashes.append(row_i)
            elif row[col] == "O":
                boulders.append(row_i)
        return (hashes, boulders)

    def tilt_north(self) -> None:
        """Move all boulders as if the platform was tilted north."""
        # Idea: Determine the # before and after and move all O's between them to the top.
        for col in range(len(self[0])):
            hashes, boulders = self.rocks_in(col)
            # As we always place before, we need an imaginary last index
            boundaries = hashes + [len(self)]
            pointer: int = 0
            for boundary_i in boundaries:
                while boulders and boulders[0] < boundary_i:
                    # Consume the boulder
                    boulder_i = boulders.pop(0)
                    self[pointer][col], self[boulder_i][col] = (
                        self[boulder_i][col],
                        self[pointer][col],
                    )
                    pointer += 1
                # We can continue placing after the current boundary
                pointer = boundary_i + 1


def given() -> Dish:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        return Dish([list(l.rstrip("\n")) for l in given_file])


# --- Part One --- #

# What is the sum of the load of all O's after tilting north once?


def part_one():
    dish = given()

    # Move all boulders north
    dish.tilt_north()

    # Calculate the load
    # Idea: Count downwards by row and enumerate in reverse.
    summed_load: int = 0
    for load_index, row in zip(itertools.count(len(dish), -1), dish):
        summed_load += load_index * row.count("O")
    return summed_load


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

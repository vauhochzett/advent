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

    def turned_right(self):  # type: () -> Dish
        """Turn by 90 degrees (to the right). Makes the previous west the new north."""
        # Can't simply multiply the empty list as this would lead to the same list reference.
        transposed_dish = Dish([list() for _ in range(len(self[0]))])
        # We need to iterate by column, moving from bottom to top through the rows
        for col_i, row_i in itertools.product(range(len(self[0])), range(len(self) - 1, -1, -1)):
            transposed_dish[col_i].append(self[row_i][col_i])
        return transposed_dish

    def load(self) -> int:
        """Sum up the load on the north beam."""
        # Idea: Count downwards by row and enumerate in reverse.
        summed_load: int = 0
        for load_index, row in zip(itertools.count(len(self), -1), self):
            summed_load += load_index * row.count("O")
        return summed_load



def given() -> Dish:
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        return Dish([list(l.rstrip("\n")) for l in given_file])


# --- Part One --- #

# What is the sum of the load of all O's after tilting north once?


def part_one():
    dish = given()
    dish.tilt_north()
    return dish.load()


# --- Part Two --- #

# What is the load sum after 1e9 cycles of tilting north, west, south, east?


def part_two():
    dish = given()

    # Cycle
    for i in range(1_000_000_000):
        for _ in range(4):
            dish.tilt_north()
            dish = dish.turned_right()

    # Calculate the load
    return dish.load()


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

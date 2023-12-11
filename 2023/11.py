""" Advent of Code 2023: Day 11 """

FILE_TO_READ = "11_input"

# - galaxies (#) and empty space (.)
# - all rows and columns of only empty space need to be doubled
# - then calculate the shortest path between galaxies

import itertools


def given():
    with open(FILE_TO_READ, encoding="utf-8") as given_file:
        lines_matrix = [list(l.rstrip("\n")) for l in given_file]
    return lines_matrix


def galaxies(space: list[list[str]]) -> list[tuple[int, int]]:
    """Return a list of coordinates (row, col) of "galaxies" (i.e., "#" characters)."""
    galaxy_coordinates = []
    for ri, row in enumerate(space):
        for ci, cell in enumerate(row):
            if cell == "#":
                galaxy_coordinates.append((ri, ci))
    return galaxy_coordinates


# --- Part One --- #


def print_space(image):
    result = []
    for row in image:
        result.append("".join(row))
    print("\n".join(result))


def part_one():
    space: list[list[str]] = given()

    # 1) Expand space (double empty rows and columns)

    # create copy to not change iterated sequence
    new_image = []
    for i, row in enumerate(space):
        new_image.append(row)
        if all(cell == "." for cell in row):
            # copy row as otherwise the reference would point to the same list
            new_image.append(row.copy())
    space = new_image
    # count cols in reverse so that insertion does not change the upcoming indices
    for i in range(len(space[0]) - 1, -1, -1):
        if all(row[i] == "." for row in space):
            for row in space:
                row.insert(i, ".")

    # 2) Find all galaxies ("#")

    galaxy_coordinates = galaxies(space)

    # 3) Calculate shortest path between all pairs

    sum_of_shortest_paths = 0
    for left, right in itertools.combinations(galaxy_coordinates, 2):
        lr, lc = left
        rr, rc = right
        sum_of_shortest_paths += abs(lr - rr) + abs(lc - rc)

    return sum_of_shortest_paths


# --- Part Two --- #


def part_two():
    return "NOT IMPLEMENTED"


# --- Main Program --- #

if __name__ == "__main__":
    print(f"Part One: {part_one()}")
    print(f"Part Two: {part_two()}")

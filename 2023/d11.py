import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

EMPTY = "."
GALAXY = "#"


def read_galaxy(lines):
    galaxy = []
    num_galaxies = 0
    for line in lines:
        row = []
        for char in line.strip():
            if char == GALAXY:
                row.append(num_galaxies)
                num_galaxies += 1
            else:
                row.append(char)
        galaxy.append(row)
    return galaxy, num_galaxies


def expand_galaxy(galaxy: list[list[str]]) -> list[list[str]]:
    new_galaxy = []
    for row in galaxy:
        new_galaxy.append(row)
        if all([char == EMPTY for char in row]):
            new_galaxy.append(row)

    galaxy = new_galaxy
    new_galaxy = [[] for _ in galaxy]
    for idy in range(len(galaxy[0])):
        for idx in range(len(galaxy)):
            new_galaxy[idx].append(galaxy[idx][idy])
        if all([galaxy[idx][idy] == EMPTY for idx in range(len(galaxy))]):
            for idx in range(len(galaxy)):
                new_galaxy[idx].append(galaxy[idx][idy])

    return new_galaxy


def get_empty_rows(galaxy: list[list[str]]) -> list[int]:
    empty_rows = []
    for idx, row in enumerate(galaxy):
        if all([char == EMPTY for char in row]):
            empty_rows.append(idx)
    return empty_rows


def get_empty_cols(galaxy: list[list[str]]) -> list[int]:
    empty_cols = []
    for idy in range(len(galaxy[0])):
        if all([galaxy[idx][idy] == EMPTY for idx in range(len(galaxy))]):
            empty_cols.append(idy)
    return empty_cols


def get_galaxies_positions(galaxy: list[list[str]]) -> dict[int, tuple[int, int]]:
    return {
        galaxy[idx][idy]: (idx, idy)
        for idx in range(len(galaxy))
        for idy in range(len(galaxy[0]))
        if galaxy[idx][idy] != EMPTY
    }


def manhattan_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return sum([abs(point1[0] - point2[0]), abs(point1[1] - point2[1])])


def calculate_points_for_empty(point1, point2, empty_rows, empty_cols):
    extra = 0
    min_x, max_x = (point1[0], point2[0]) if point1[0] < point2[0] else (point2[0], point1[0])
    for row in empty_rows:
        if min_x < row < max_x:
            extra += 1000000 - 1

    min_y, max_y = (point1[1], point2[1]) if point1[1] < point2[1] else (point2[1], point1[1])
    for col in empty_cols:
        if min_y < col < max_y:
            extra += 1000000 - 1

    return extra


def get_galaxy_positions(galaxy):
    return {
        galaxy[idx][idy]: (idx, idy)
        for idx in range(len(galaxy))
        for idy in range(len(galaxy[0]))
        if galaxy[idx][idy] != EMPTY
    }


def generate_pairs_for_galaxies(num_galaxies):
    return [(i, j) for i in range(num_galaxies) for j in range(i, num_galaxies) if i < j]


def solve(lines, part2=False):
    galaxy, num_galaxies = read_galaxy(lines)
    if not part2:
        galaxy = expand_galaxy(galaxy)
        galaxies_positions = get_galaxy_positions(galaxy)
        pairs = generate_pairs_for_galaxies(num_galaxies)
        return sum([manhattan_distance(galaxies_positions[i], galaxies_positions[j]) for i, j in pairs])

    galaxies_positions = get_galaxy_positions(galaxy)
    pairs = generate_pairs_for_galaxies(num_galaxies)
    empty_rows = get_empty_rows(galaxy)
    empty_cols = get_empty_cols(galaxy)

    return sum([
        (manhattan_distance(galaxies_positions[i], galaxies_positions[j])
         + calculate_points_for_empty(galaxies_positions[i], galaxies_positions[j], empty_rows, empty_cols))
        for i, j in pairs
    ])


if __name__ == '__main__':
    print(solve(full))
    print(solve(full, True))

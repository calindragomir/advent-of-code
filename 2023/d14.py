import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

ROUND_ROCK = "O"
CUBE_ROCK = "#"
EMPTY = "."


def rotate_left(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def slide_rocks(row):
    new_list = []
    index = 0
    for idx, c in enumerate(row):
        if c == EMPTY:
            new_list.append(EMPTY)
        if c == ROUND_ROCK:
            new_list.insert(index, ROUND_ROCK)
        if c == CUBE_ROCK:
            new_list.append(CUBE_ROCK)
            index = idx + 1

    return new_list


def calculate_load(slided_row):
    load_parts = []
    max_load = len(slided_row)
    for c in slided_row:
        if c == ROUND_ROCK:
            load_parts.append(max_load)
        max_load -= 1
    return sum(load_parts)


def solve(lines):
    matrix = [[a for a in c] for c in lines]
    transposed = rotate_left(matrix)
    slided = [slide_rocks(r) for r in transposed]
    loads = [calculate_load(r) for r in slided]
    return sum(loads)


###
def tilt_east(rock_map):
    return tuple(CUBE_ROCK.join([''.join(sorted(p)) for p in row.split(CUBE_ROCK)]) for row in rock_map)


def tilt_north(m):
    return rotate_counterclockwise(tilt_east(rotate_clockwise(m)))


def transpose(m):
    return tuple(''.join(i) for i in list(zip(*m)))


def flip(m):
    return m[::-1]


def rotate_clockwise(m):
    return transpose(flip(m))


def rotate_counterclockwise(m):
    return flip(transpose(m))


def spin_platform(rock_map):
    for _ in range(4):
        rock_map = rotate_clockwise(rock_map)
        rock_map = tilt_east(rock_map)
    return rock_map


def north_load(m):
    return sum([row.count(ROUND_ROCK) * i for i, row in enumerate(m[::-1], 1)])


def solve_p2(lines):
    rock_map = tuple(line.strip() for line in lines)
    rm_dict = {}
    for i in range(1, 1000000000):
        rock_map = spin_platform(rock_map)
        if rock_map in rm_dict:
            loop_start = rm_dict[rock_map]
            loop_length = i - loop_start
            i_f = (1000000000 - loop_start) % loop_length + loop_start
            for rock_map, j in rm_dict.items():
                if j == i_f:
                    return north_load(rock_map)
        else:
            rm_dict[rock_map] = i


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve_p2(sample))
    print(solve_p2(full))

import numpy as np

import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

DIRECTIONS = {
    "R": (0, 1),
    "D": (-1, 0),
    "L": (0, -1),
    "U": (1, 0),
}


def solve(lines, part2=False):
    loc, num_pts, pts, xs, ys, b = (0, 0), 0, set(), [], [], None

    if not part2:
        pts.add(loc)
        for line in lines:
            line = line.strip()
            a, b, c = line.split()
            current_direction = DIRECTIONS[a]
            current_length = int(b)
            for i in range(current_length+1):
                pts.add((loc[0] + i * current_direction[0], loc[1] + i * current_direction[1]))

            loc = (loc[0] + current_length * current_direction[0], loc[1] + current_length * current_direction[1])
            xs.append(loc[0])
            ys.append(loc[1])
            b = len(pts)
    else:
        dir_map = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        for line in lines:
            line = line.strip()
            a, b, c = line.split()

            current_direction = dir_map[int(c[-2])]
            current_length = int(c[-7:-2], 16)

            num_pts += current_length
            loc = (loc[0] + current_length * current_direction[0], loc[1] + current_length * current_direction[1])
            xs.append(loc[0])
            ys.append(loc[1])
            b = num_pts

    area = calculate_polygon_area(xs, ys)
    i = round(area + 1 - b // 2)
    return i+b


def calculate_polygon_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(sample, True))
    print(solve(full, True))

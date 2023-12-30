from collections import namedtuple
from itertools import combinations
from sympy import ZZ, Symbol, solve

import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

Data = namedtuple("Data", "id, xpos, xvelo, ypos, yvelo, zpos, zvelo")


def check_intersection(c: (Data, Data), test_area):
    x1 = c[0].xpos
    x2 = c[0].xpos + c[0].xvelo
    x3 = c[1].xpos
    x4 = c[1].xpos + c[1].xvelo
    y1 = c[0].ypos
    y2 = c[0].ypos + c[0].yvelo
    y3 = c[1].ypos
    y4 = c[1].ypos + c[1].yvelo

    den = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    if den != 0:
        px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
        will_intersect_first = (px > x1) == (x2 > x1)
        will_intersect_second = (px > x3) == (x4 > x3)

        return (test_area[0] <= px <= test_area[1] and test_area[0] <= py <= test_area[1]
                and will_intersect_first and will_intersect_second)

    return False


def calculate_intersections(info, test_area):
    combined = combinations(info, 2)
    intersected = 0
    for c in combined:
        if check_intersection(c, test_area):
            intersected += 1
    return intersected


def solve_equation(infos):
    rx, ry, rz = (Symbol(x, domain=ZZ) for x in ("rx", "ry", "rz"))
    rvelx, rvely, rvelz = (Symbol(x, domain=ZZ) for x in ("rvelx", "rvely", "rvelz"))

    equations = []
    for i, info in enumerate(infos):
        (x, y, z), (vx, vy, vz) = (info.xpos, info.ypos, info.zpos), (info.xvelo, info.yvelo, info.zvelo)
        t = Symbol(f"t{i}", positive=True, domain=ZZ)

        eqx = rx + t * rvelx - x - t * vx
        eqy = ry + t * rvely - y - t * vy
        eqz = rz + t * rvelz - z - t * vz

        equations.extend([eqx, eqy, eqz])

    solutions = solve(equations, dict=True, domain=ZZ, check=False)

    return solutions[0][rx] + solutions[0][ry] + solutions[0][rz]


def solver(lines, test_area, part2=False):
    info = []
    identifier = 0
    for line in lines:
        parts = line.split("@")
        locations = [int(loc.strip()) for loc in parts[0].split(",")]
        speeds = [int(speed.strip()) for speed in parts[1].split(",")]
        info.append(Data(identifier, locations[0], speeds[0], locations[1], speeds[1], locations[2], speeds[2]))
        identifier += 1

    if not part2:
        return calculate_intersections(info, test_area)

    result = None
    for i in range(0, len(info), 3):
        result = solve_equation(info[i:i+3])

    return result


if __name__ == '__main__':
    print(solver(sample, (7, 27)))
    print(solver(full, (200000000000000, 400000000000000)))
    print(solver(full, (200000000000000, 400000000000000), True))

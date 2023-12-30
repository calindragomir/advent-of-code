from itertools import cycle
from math import lcm

import utils
import re

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

START = "AAA"
END = "ZZZ"


def solve(lines, part2=False):
    directions = lines[0]
    instructions = build_instructions(lines)

    if not part2:
        return solve_p1(directions, instructions, START, END)

    return solve_p2(directions, instructions)


def solve_p1(directions, instructions, start_point, end_point):
    current_point = start_point
    steps = 0
    for idx, dir in enumerate(cycle(directions)):
        if current_point == end_point:
            break
        current_point = instructions[current_point][0] if dir == "L" else instructions[current_point][1]
        steps += 1
    return steps


def solve_p2(directions, instructions):
    steps = []
    current_points = [point for point in instructions.keys() if point[2] == "A"]
    for point in current_points:
        current_point = point
        curr_steps = 0
        for idx, dir in enumerate(cycle(directions)):
            if current_point[2] == "Z":
                break
            current_point = instructions[current_point][0] if dir == "L" else instructions[current_point][1]
            curr_steps += 1
        steps.append(curr_steps)

    return lcm(*steps)


def build_instructions(lines):
    instructions = {}
    for path in lines[1:]:
        data = re.findall(r'[A-Z]{3}', path)
        instructions[data[0]] = [data[1], data[2]]
    return instructions


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(full, True))

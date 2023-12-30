import numpy as np
from scipy.interpolate import CubicSpline

import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

START = "S"
GARDEN_PLOT = "."
ROCK = "#"
P1_STEPS = 64
P2_STEPS = 26501365


def successors(cell, rocks, limx, limy):
    for pos in (1, -1, 1j, -1j):
        next_pos = cell + pos
        complex_next = complex(next_pos.real % limx, next_pos.imag % limy)
        if complex_next not in rocks:
            yield next_pos


def reachable_blocks(steps, rocks, limx, limy, start):
    log = {start}
    history = []
    for _ in range(steps):
        reachable = set()
        while log:
            cell = log.pop()
            for successor in successors(cell, rocks, limx, limy):
                reachable.add(successor)

        log = reachable
        history.append(len(log))

    return history


def solve(lines, part2=False):
    m = utils.Utilities.get_matrix_from_input(lines, str)
    limy, limx = len(m), len(m[0])
    rocks, start = set(), None
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == ROCK:
                rocks.add(x + y * 1j)
            elif cell == START:
                start = x + y * 1j

    if not part2:
        *_, reachable = reachable_blocks(P1_STEPS, rocks, limx, limy, start)
        return reachable

    period_start = int(start.real)
    period_length = limy
    history = reachable_blocks(period_start + 2 * period_length, rocks, limx, limy, start)
    ys = np.array(history[period_start - 1::period_length])
    xs = np.arange(len(ys))
    spline = CubicSpline(xs, ys)
    target_period = (P2_STEPS - period_start) // period_length
    return int(spline(target_period))


if __name__ == '__main__':
    print(solve(full))
    print(solve(full, True))

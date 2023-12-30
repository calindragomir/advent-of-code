from collections import namedtuple
from functools import reduce

from utils import Utilities

sample = Utilities.get_lines_from_file("sample/d6sample.txt")
p2input = Utilities.get_lines_from_file("d6p2.txt")

TITLE_LINES = {
    0: "Time:",
    1: "Distance:"
}

Pairs = namedtuple("Pairs", "time,distance")


def get_allowed_waiting_times(pair):
    min_dist = pair.distance
    max_time = pair.time
    ok = []
    for wait in range(1, max_time + 1):
        dist_covered = wait * (max_time - wait)
        if dist_covered > min_dist:
            ok.append(wait)
    return ok

def p1(lines):
    times = parser(lines[0], TITLE_LINES[0])
    distances = parser(lines[1], TITLE_LINES[1])
    return solve([Pairs(t, d) for t, d in zip(times, distances)])

def p2(lines):
    time = parserp2(lines[0], TITLE_LINES[0])
    distance = parserp2(lines[1], TITLE_LINES[1])
    return solve([Pairs(time, distance)])

def solve(pairs):
    all_allowed = []
    for pair in pairs:
        all_allowed.append(len(get_allowed_waiting_times(pair)))
    return reduce(lambda x, y: x*y, all_allowed)


def parser(line, title):
    return [int(t.strip()) for t in line.lstrip(title).split(" ") if t.strip() != '']


def parserp2(line, title):
    return int("".join(line.lstrip(title).split(" ")))


if __name__ == '__main__':
    print(p1(sample))
    print(p1(Utilities.get_full_input(__file__)))
    print(p2(p2input))

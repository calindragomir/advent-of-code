import utils
import functools

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

TRANSLATIONS = {
    ".": 0,
    "#": 1,
    "?": 2
}


@functools.cache
def arrangements(config, group):
    if len(group) == 0:
        a = int(sum(c == 1 for c in config) == 0)
        return a
    if sum(group) > len(config):
        return 0
    if config[0] == 0:
        a = arrangements(config[1:], group)
        return a

    no1, no2 = 0, 0
    if config[0] == 2:
        no2 = arrangements(config[1:], group)
    if all(c != 0 for c in config[:group[0]]) and (config[group[0]] if len(config) > group[0] else 0) != 1:
        no1 = arrangements(config[(group[0] + 1):], group[1:])

    return no1 + no2


def solve(lines, part2=False):
    total = 0
    for line in lines:
        config_raw, group_raw = line.strip().split(' ')
        config = [TRANSLATIONS[x] for x in config_raw]
        group = [int(x) for x in group_raw.split(',')]

        if part2:
            config = ((config + [2]) * 5)[:-1]
            group *= 5

        arr = arrangements(tuple(config), tuple(group))
        total += arr
    return total


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(sample, True))
    print(solve(full, True))

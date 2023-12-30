import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)


def coupled(iterable):
    coup = []
    for i, a in enumerate(iterable):
        if i + 1 == len(iterable):
            break
        pair = (a, iterable[i + 1])
        coup.append(pair)
    return coup


def solve(lines):
    all_processed = []
    for l in lines:
        processed = process_line(l)
        if is_all_zeros(processed[-1]):
            last, first = 0, 0
            for p in reversed(processed):
                last = p[-1] + last
                first = p[0] - first
                p.append(last)
                p.insert(0, first)
        else:
            continue
        all_processed.append(processed)

    line_ends_totals = []
    line_fronts_totals = []
    for p in all_processed:
        line_ends_totals.append(p[0][-1])
        line_fronts_totals.append(p[0][0])

    return sum(line_ends_totals), sum(line_fronts_totals)


def is_all_zeros(line):
    s = set(line)
    if len(s) == 1 and s.pop() == 0:
        return True
    else:
        return False


def extend_line_by_number(line, number):
    last = line[-1]
    line.append(last + number)
    return line


def process_line(line):
    numbers = [int(i) for i in line.split()]
    c = coupled(numbers)
    processed = [[int(i) for i in line.split(" ")]]
    updated = [b - a for a, b in c]
    while not are_all_zeros(updated):
        processed.append(updated)
        c = coupled(updated)
        updated = [b - a for a, b in c]
    processed.append(updated)
    return processed


def are_all_zeros(elems):
    for e in elems:
        if e != 0:
            return False
    return True


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))

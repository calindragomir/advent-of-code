import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)


def follow_beam(start, matrix, rows, columns):
    current, visited, energized = [start], set(), set()
    while current:
        next_tile = []
        for (i, j, di, dj) in current:
            """
            di = 1 -> moves right ; di = -1 -> moves left
            dj = 1 -> moves down ; dj = -1 -> moves up
            """
            i += di
            j += dj
            if i < 0 or j < 0 or i >= rows or j >= columns:
                continue
            if (i, j, di, dj) in visited:
                continue
            visited.add((i, j, di, dj))
            energized.add((i, j))
            t = matrix[j][i]
            if t == "." or (t == "|" and di == 0) or (t == "-" and dj == 0):
                next_tile.append((i, j, di, dj))
            elif t == "|" and di != 0:
                next_tile.append((i, j, 0, 1))
                next_tile.append((i, j, 0, -1))
            elif t == "-" and dj != 0:
                next_tile.append((i, j, 1, 0))
                next_tile.append((i, j, -1, 0))
            elif t == "/":
                next_tile.append((i, j, -dj, -di))
            elif t == "\\":
                next_tile.append((i, j, dj, di))
        current = next_tile

    return len(energized)


def solve(lines, part2=False):
    matrix = [[c for c in line] for line in lines]
    rows, columns = (0, 0) if len(matrix) == 0 else (len(matrix), len(matrix[0]))
    if not part2:
        return follow_beam((-1, 0, 1, 0), matrix, rows, columns)
    else:
        m = 0
        for x in range(rows):
            m = max(m, follow_beam((x, -1, 0, 1), matrix, rows, columns))
            m = max(m, follow_beam((x, columns, 0, -1), matrix, rows, columns))
        for y in range(columns):
            m = max(m, follow_beam((-1, 0, 1, 0), matrix, rows, columns))
            m = max(m, follow_beam((rows, 0, -1, 0), matrix, rows, columns))
        return m


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(sample, True))
    print(solve(full, True))

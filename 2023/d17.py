import utils
import heapq

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)


def minimize_heat_loss(g, rows, columns, part2=False):
    to_visit = [(0, 0, 0, -1, -1)]
    distances = {}
    while to_visit:
        dist, i, j, direction, indirection = heapq.heappop(to_visit)
        if (i, j, direction, indirection) in distances:
            continue
        distances[(i, j, direction, indirection)] = dist
        for idx, (dr, dc) in enumerate([[-1, 0], [0, 1], [1, 0], [0, -1]]):
            rr = i + dr
            cc = j + dc
            new_direction = idx
            new_indirection = (1 if new_direction != direction else indirection + 1)

            not_reverse = ((new_direction + 2) % 4 != direction)

            is_valid_part1 = (new_indirection <= 3)
            is_valid_part2 = (new_indirection <= 10 and (new_direction == direction or indirection >= 4 or indirection == -1))
            is_valid = (is_valid_part2 if part2 else is_valid_part1)

            if 0 <= rr < rows and 0 <= cc < columns and not_reverse and is_valid:
                cost = g[rr][cc]
                if (rr, cc, new_direction, new_indirection) in distances:
                    continue
                heapq.heappush(to_visit, (dist + cost, rr, cc, new_direction, new_indirection))

    ans = 1e9
    for (r, c, direction, indirection), v in distances.items():
        if r == rows - 1 and c == columns - 1 and (indirection >= 4 or not part2):
            ans = min(ans, v)

    return ans

def solve(lines, part2=False):
    g = utils.Utilities.get_matrix_from_input(lines, data_type=int)
    rows = len(g)
    columns = len(g[0])
    return minimize_heat_loss(g, rows, columns, part2)


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(sample, True))
    print(solve(full, True))

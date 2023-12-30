import utils
import numpy as np

sample = utils.Utilities.get_lines_from_file_including_space("sample/d13sample.txt")
full = utils.Utilities.get_lines_from_file_including_space("d13.txt")


def indentify_reflection(array, part):
    row_max = array.shape[0]
    for r in range(1, row_max):
        size = min(r, row_max - r)
        sub = array[r - size:r + size]
        sub_a = np.flipud(sub[:len(sub)//2])
        sub_b = sub[len(sub)//2:]

        if part == 1:
            if np.array_equal(sub_a, sub_b):
                return r
        else:
            if np.sum(sub_a == sub_b) == np.prod(sub_a.shape) - 1:
                return r

    return None


def get_board_info(board, part=1):
    b = np.array(board)
    index = indentify_reflection(b.T, part)

    if index is None:
        index = indentify_reflection(b, part) * 100

    return index


def solve(lines):
    boards = []
    for idx, line in enumerate(lines):
        if idx == 0 or line == "":
            boards.append([])
        if line == "":
            continue

        boards[-1].append(list(line))

    sums_p1 = []
    sums_p2 = []
    for board in boards:
        sums_p1.append(get_board_info(board, 1))
        sums_p2.append(get_board_info(board, 2))

    return sum(sums_p1), sum(sums_p2)


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))

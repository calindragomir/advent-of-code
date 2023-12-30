import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

START = "S"
CORNERS = {"J", "L", "F", "7"}


def solve(lines, part2=False):
    start = find_start(lines)
    loop = find_loop(lines, start)
    if not part2:
        return solve_p1(loop)
    area = polygon_area(loop)
    return solve_p2(area, len(loop))


def solve_p1(loop):
    return len(loop) // 2 + len(loop) % 2


def solve_p2(area, loop_size):
    return int(area - 0.5 * loop_size + 1)


def find_start(matrix):
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            if element == START:
                return i, j
    return None


def find_start_direction(matrix, start):
    valid_directions = {
        (1, 0): {"|", "J", "L"},
        (0, -1): {"F", "L", "-"},
        (-1, 0): {"|", "7", "F"},
        (0, 1): {"J", "7", "-"},
    }
    for (offset_row, offset_col), valid_pipes in valid_directions.items():
        new_row, new_col = start[0] + offset_row, start[1] + offset_col
        if check_location(new_row, new_col, valid_pipes, matrix):
            return offset_row, offset_col
    return None


def check_location(new_row, new_col, valid_pipes, matrix):
    return (0 <= new_row < len(matrix)
            and 0 <= new_col < len(matrix[0])
            and matrix[new_row][new_col] in valid_pipes)


def calculate_next_direction(row_offset: int, col_offset: int, pipe: str) -> tuple[int, int]:
    directions = {"L": 1, "7": 1, "J": -1, "F": -1}
    return col_offset * directions[pipe], row_offset * directions[pipe]


def find_loop(matrix, start):
    dir_row, dir_col = find_start_direction(matrix, start)
    current = start
    loop = []
    while current != start or not loop:
        loop.append(current)
        row, col = current
        current = (row + dir_row, col + dir_col)
        pipe = matrix[current[0]][current[1]]
        if pipe in CORNERS:
            dir_row, dir_col = calculate_next_direction(dir_row, dir_col, pipe)
    return loop


def polygon_area(coordinates):
    x, y = zip(*coordinates)
    return 0.5 * abs(sum(x[i] * y[i - 1] - x[i - 1] * y[i] for i in range(len(coordinates))))


if __name__ == "__main__":
    print(solve(sample))
    print(solve(full))
    print(solve(full, True))

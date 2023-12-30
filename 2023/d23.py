import sys
from collections import deque

import utils

sample = utils.Utilities.get_sample_file(__file__)
full = utils.Utilities.get_full_input(__file__)

sys.setrecursionlimit(3000000)

PATH = ".."
FOREST = "#"


def solve(lines, part2=False):
    grid = []
    for line in lines:
        line = line.strip()
        if line == "": continue
        grid.append(line)

    if not part2:
        return do_part1(grid)
    else:
        return do_part2(grid)


def do_part1(grid):
    dst = {((0, 1), (-1, 1)): 0, ((1, 1), (0, 1)): 1}
    bfs_q = deque()
    bfs_q.append(((1, 1), (0, 1), 1))
    answer = 0

    while len(bfs_q) > 0:
        cur_pt, prev_pt, cdst = bfs_q.popleft()
        if dst[(cur_pt, prev_pt)] != cdst:
            continue
        if cur_pt[0] == len(grid) - 1:
            answer = max(answer, cdst)
            continue
        cx, cy = cur_pt
        nxts = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        if grid[cx][cy] == "<":
            nxts = [(0, -1)]
        if grid[cx][cy] == ">":
            nxts = [(0, 1)]
        if grid[cx][cy] == "v":
            nxts = [(1, 0)]
        if grid[cx][cy] == "^":
            nxts = [(-1, 0)]
        for dx, dy in nxts:
            nx, ny = cx + dx, cy + dy
            if nx < 0:
                continue
            if ny < 0:
                continue
            if nx >= len(grid):
                continue
            if ny >= len(grid[nx]):
                continue
            if grid[nx][ny] == FOREST:
                continue
            if (nx, ny) == prev_pt:
                continue
            if grid[nx][ny] != PATH:
                px, py = None, None
                if grid[nx][ny] == "<":
                    px, py = (0, -1)
                if grid[nx][ny] == ">":
                    px, py = (0, 1)
                if grid[nx][ny] == "v":
                    px, py = (1, 0)
                if grid[nx][ny] == "^":
                    px, py = (-1, 0)
                if (nx + px, ny + py) == cur_pt:
                    continue
            if ((nx, ny), cur_pt) not in dst or dst[((nx, ny), cur_pt)] < dst[(cur_pt, prev_pt)] + 1:
                dst[((nx, ny), cur_pt)] = dst[(cur_pt, prev_pt)] + 1
                bfs_q.append(((nx, ny), cur_pt, dst[((nx, ny), cur_pt)]))

    return answer


ans = 0
vis = set()


def do_part2(grid):
    global ans
    dfs((0, 1), grid)
    return ans


def dfs(cur_pos, grid):
    global ans
    if cur_pos in vis:
        return
    if cur_pos[0] == len(grid)-1:
        ans = max(ans, len(vis))
        return

    vis.add(cur_pos)

    cx, cy = cur_pos
    for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        nx, ny = cx + dx, cy + dy
        if nx < 0:
            continue
        if ny < 0:
            continue
        if nx >= len(grid):
            continue
        if ny >= len(grid[nx]):
            continue
        if grid[nx][ny] == FOREST:
            continue
        if (nx, ny) in vis:
            continue
        dfs((nx, ny), grid)

    vis.remove(cur_pos)


if __name__ == '__main__':
    print(solve(sample))
    print(solve(full))
    print(solve(sample, True))
    print(solve(full, True))

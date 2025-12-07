from utils import run_solver, cache_by_id, dprint

TEST_INPUT = r'''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............'''
TEST_OUTPUT1 = 21
TEST_OUTPUT2 = 40

@run_solver("Part 1", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT1)])
def part1(d: list[str]) -> int:
    H = len(d)
    W = len(d[0])
    mid = W // 2
    cols = [0] * W
    cols[mid] = 1
    t = 0
    for r in range(1, H // 2):
        ncols = [0] * W
        row = d[2 * r]
        for c in range(mid - r + 1, mid + r):
            if cols[c]:
                if row[c] == '^':
                    t += 1
                    ncols[c - 1] = 1
                    ncols[c + 1] = 1
                else:
                    ncols[c] = 1
        cols = ncols
    return t


@run_solver("Part 2", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT2)])
def part2(d: list[str]) -> int:
    H = len(d)
    W = len(d[0])
    mid = W // 2
    cols = [0] * W
    cols[mid] = 1
    for r in range(1, H // 2):
        ncols = [0] * W
        row = d[2 * r]
        for c in range(mid - r + 1, mid + r):
            cnt = cols[c]
            if row[c] == '^':
                ncols[c - 1] += cnt
                ncols[c + 1] += cnt
            else:
                ncols[c] += cnt
        cols = ncols
    return sum(cols)

if __name__ == '__main__':
    part1()
    part2()
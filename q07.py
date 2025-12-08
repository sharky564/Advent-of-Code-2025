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
    TRANS_TABLE = {46: '0', 94: '1'}
    active = 1 << (len(d[0]) // 2)
    t = 0
    for r in range(2, len(d), 2):
        hits = active & int(d[r].translate(TRANS_TABLE), 2)
        t += hits.bit_count()
        active = (active & ~hits) | (hits >> 1) | (hits << 1)
    return t


@run_solver("Part 2", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT2)])
def part2(d: list[str]) -> int:
    W = len(d[0])
    mid = W // 2
    cols = [0] * W
    cols[mid] = 1
    for r in range(1, len(d) // 2):
        row = d[2 * r]
        for c in range(mid - r + 1, mid + r, 2):
            if row[c] == '^':
                cnt = cols[c]
                cols[c - 1] += cnt
                cols[c] = 0
                cols[c + 1] += cnt
    return sum(cols)


if __name__ == '__main__':
    part1()
    part2()
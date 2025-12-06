from utils import run_solver, cache_by_id, dprint

TEST_INPUT = r'''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''
TEST_OUTPUT1 = 3
TEST_OUTPUT2 = 6

@cache_by_id
def process_data(d: list[str]):
    return (int(l[1:]) * (1 if l[0] == 'R' else -1) for l in d)

@run_solver("Part 1", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT1)])
def part1(d: list[str]) -> int:
    data = process_data(d)
    v = 50
    N = 100
    t = 0
    for s in data:
        v += s
        t += v % N == 0
    return t
    

@run_solver("Part 2", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT2)])
def part2(d: list[str]) -> int:
    data = process_data(d)
    v = 50
    N = 100
    t = 0
    for s in data:
        p = v
        v += s
        if s < 0:
            t += -v // N - -p // N
        else:
            t += v // N - p // N
    return t


if __name__ == '__main__':
    part1()
    part2()
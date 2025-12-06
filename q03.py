from utils import run_solver, dprint

TEST_INPUT = r'''987654321111111
811111111111119
234234234234278
818181911112111'''
TEST_OUTPUT1 = 357
TEST_OUTPUT2 = 3121910778619

def find(s, k):
    n = 0
    r = []
    l = len(s)
    for i in range(l + 1 - k, l + 1):
        for c in '9876543210':
            if (j := s.find(c, n, i)) != -1:
                r.append(c)
                n = j + 1
                break
    return int(''.join(r))


@run_solver("Part 1", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT1)])
def part1(d: list[str]) -> int:
    return sum(map(lambda s: find(s, 2), d))


@run_solver("Part 2", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT2)])
def part2(d: list[str]) -> int:
    return sum(map(lambda s: find(s, 12), d))


if __name__ == '__main__':
    part1()
    part2()
from utils import run_solver

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


@run_solver("Part 1", submit_result=False)
def part1(d: list[str]) -> int:
    return sum(map(lambda s: find(s, 2), d))


@run_solver("Part 2", submit_result=False)
def part2(d: list[str]) -> int:
    return sum(map(lambda s: find(s, 12), d))


if __name__ == '__main__':
    part1()
    part2()
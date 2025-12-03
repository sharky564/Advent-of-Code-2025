from utils import run_solver

def process_data(d: list[str]):
    return [list(map(int, line)) for line in d]


def find_largest_subsequence(b, l):
    v = 0
    while l > 0:
        l -= 1
        if l > 0:
            s = max(b[:-l])
        else:
            s = max(b)
        b = b[b.index(s) + 1:]
        v = 10 * v + s
    return v


@run_solver("Part 1", submit_result=False)
def part1(d: list[str]) -> int:
    data = process_data(d)
    t = 0
    for b in data:
        t += find_largest_subsequence(b, 2)
    return t

@run_solver("Part 2", submit_result=False)
def part2(d: list[str]) -> int:
    data = process_data(d)
    t = 0
    for b in data:
        x = find_largest_subsequence(b, 12)
        t += x
    return t

if __name__ == '__main__':
    part1()
    part2()

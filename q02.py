from utils import run_solver
from math import ceil

def process_data(d: list[str]):
    return [l.split('-') for l in d[0].split(',')]


@run_solver("Part 1")
def part1(d: list[str]) -> int:
    data = process_data(d)
    t = 0
    for s, e in data:
        for n in range(len(s), len(e) + 1):
            if n % 2 == 0:
                l = n // 2
                m = 10**l + 1
                a = max(ceil(int(s) / m), 10**(l - 1))
                b = min(int(e) // m + 1, 10**l)
                t += m * (b - a) * (b + a - 1) // 2
    return t
    

@run_solver("Part 2")
def part2(d: list[str]) -> int:
    data = process_data(d)
    i = set()
    for s, e in data:
        for n in range(min(2, len(s)), len(e) + 1):
            for l in range(1, n // 2 + 1):
                if n % l == 0:
                    m = (10**n - 1) // (10**l - 1)
                    a = max(ceil(int(s) / m), 10**(l - 1))
                    b = min(int(e) // m + 1, 10**l)
                    i.update(range(a * m, b * m, m))
    return sum(i)

if __name__ == '__main__':
    part1()
    part2()
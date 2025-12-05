# from utils import run_solver
# import bisect

# _CACHE = {}

# def process_data(d: list[str]):
#     d_id = id(d)
#     if d_id in _CACHE:
#         return _CACHE[d_id]
#     r = []
#     s = []
#     for l in d:
#         if '-' in l:
#             i = l.find('-')
#             r.append([int(l[:i]), int(l[i+1:]) + 1])
#         elif l:
#             s.append(int(l))
            
#     r.sort()
#     m = [r[0]]
#     e = r[0][1]
    
#     for x, y in r[1:]:
#         if e < x:
#             m[-1][1] = e
#             m.append([x, y])
#             e = y
#         elif y > e:
#             e = y
    
#     m[-1][1] = e

#     result = (m, s)
#     _CACHE[d_id] = result
#     return result

# @run_solver("Part 1", submit_result=False)
# def part1(d: list[str]) -> int:
#     rg, s = process_data(d)
#     sp = [r[0] for r in rg]
#     c = 0
#     for v in s:
#         i = bisect.bisect_right(sp, v) - 1
#         if i >= 0:
#             if v < rg[i][1]:
#                 c += 1
#     return c

# @run_solver("Part 2", submit_result=False)
# def part2(d: list[str]) -> int:
#     rg, _ = process_data(d)
#     return sum(y - x for x, y in rg)

# if __name__ == '__main__':
#     part1()
#     part2()

from utils import run_solver
import bisect

_CACHE = {}

def process_data(d: list[str]):
    d_id = id(d)
    if d_id in _CACHE:
        return _CACHE[d_id]
    try:
        i = d.index('') 
    except ValueError:
        i = len(d)

    r = []
    for i in range(i):
        s, _, e = d[i].partition('-')
        r.append((int(s), int(e) + 1))

    r.sort()

    s = []
    e = []
    
    cs, ce = r[0]
    
    for ns, ne in r[1:]:
        if ns > ce:
            s.append(cs)
            e.append(ce)
            cs, ce = ns, ne
        elif ne > ce:
            ce = ne
            
    s.append(cs)
    e.append(ce)
    n = [int(l) for l in d[i+1:] if l]

    result = (tuple(s), tuple(e), n)
    _CACHE[d_id] = result
    return result

@run_solver("Part 1", submit_result=False)
def part1(d: list[str]) -> int:
    s, e, n = process_data(d)
    bi = bisect.bisect_right
    c = 0
    
    for v in n:
        i = bi(s, v)
        if i > 0 and v < e[i-1]:
            c += 1
    return c

@run_solver("Part 2", submit_result=False)
def part2(d: list[str]) -> int:
    s, e, _ = process_data(d)
    return sum(e - s for s, e in zip(s, e))

if __name__ == '__main__':
    part1()
    part2()
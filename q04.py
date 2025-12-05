from utils import run_solver

_CACHE = {}

def process_data(d: list[str]):
    d_id = id(d)
    if d_id in _CACHE:
        return _CACHE[d_id]
    R = len(d)
    C = len(d[0])
    W = C + 2
    g = bytearray((R + 2) * W)
    
    r = []
    i = W + 1
    
    for x in range(R):
        row = d[x]
        for y in range(C):
            if row[y] == '@':
                g[i] = 1
                r.append(i)
            i += 1
        i += 2
    
    result = (g, r, W)
    _CACHE[d_id] = result
    return result

@run_solver("Part 1", submit_result=False)
def part1(d: list[str]) -> int:
    g, r, w = process_data(d)
    o1, o2, o3, o4, o5, o6, o7, o8 = -w - 1, -w, -w + 1, -1, 1, w - 1, w, w + 1
    c = 0
    for i in r:
        if g[i + o1] + g[i + o2] + g[i + o3] + g[i + o4] + g[i + o5] + g[i + o6] + g[i + o7] + g[i + o8] <= 3:
            c += 1
    return c

@run_solver("Part 2", submit_result=False)
def part2(d: list[str]) -> int:
    g, r, w = process_data(d)
    
    o1, o2, o3, o4, o5, o6, o7, o8 = -w - 1, -w, -w + 1, -1, 1, w - 1, w, w + 1
    n = bytearray(len(g))
    q = []
    
    for i in r:
        c = g[i + o1] + g[i + o2] + g[i + o3] + g[i + o4] + g[i + o5] + g[i + o6] + g[i + o7] + g[i + o8]
        n[i] = c
        if c <= 3:
            q.append(i)
            
    r = 0
    while q:
        c = q.pop()            
        g[c] = 0
        r += 1

        k = c + o1
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)
            
        k = c + o2
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)

        k = c + o3
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)

        k = c + o4
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)

        k = c + o5
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)

        k = c + o6
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)

        k = c + o7
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)

        k = c + o8
        if g[k]:
            n[k] -= 1
            if n[k] == 3:
                q.append(k)

    return r

if __name__ == '__main__':
    part1()
    part2()

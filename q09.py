from utils import run_solver, cache_by_id, dprint
import itertools

TEST_INPUT = r'''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3'''
TEST_OUTPUT1 = 50
TEST_OUTPUT2 = 24


@cache_by_id
def process_data(d: list[str]):
    return [list(map(int, line.split(','))) for line in d]

@run_solver("Part 1", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT1)], profile=True)
def part1(d: list[str]) -> int:
    data = process_data(d)
    max_found = 0
    for p1, p2 in itertools.combinations(data, 2):
        area = (abs(p1[1] - p2[1]) + 1) * (abs(p1[0] - p2[0]) + 1)
        if area > max_found:
            max_found = area
    return max_found


@run_solver("Part 2", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT2)], profile=True)
def part2(d: list[str]) -> int:
    points = process_data(d)
    n = len(points)
    xs = sorted(set(p[0] for p in points))
    ys = sorted(set(p[1] for p in points))
    x_map = {x: i for i, x in enumerate(xs)}
    y_map = {y: i for i, y in enumerate(ys)}
    
    W, H = len(xs) - 1, len(ys) - 1
    
    v_edges = []
    for i in range(n):
        p1 = points[i]
        p2 = points[i - 1]
        if p1[0] == p2[0]:
            xi = x_map[p1[0]]
            y_start = y_map[p1[1]]
            y_end = y_map[p2[1]]
            if y_start > y_end:
                y_start, y_end = y_end, y_start
            v_edges.append((xi, y_start, y_end))
    v_edges.sort()
    active_y = [0] * H
    current_pref_row = [0] * (H + 1)
    pref = [current_pref_row]
    
    edge_ptr = 0
    num_edges = len(v_edges)
    for xi in range(W):
        while edge_ptr < num_edges and v_edges[edge_ptr][0] == xi:
            _, y_s, y_e = v_edges[edge_ptr]
            for yi in range(y_s, y_e):
                active_y[yi] ^= 1
            edge_ptr += 1
        col_acc = list(itertools.accumulate(active_y, initial=0))
        new_pref_row = [p + c for p, c in zip(current_pref_row, col_acc)]
        
        pref.append(new_pref_row)
        current_pref_row = new_pref_row

    max_found = 0
    points.sort() 
    
    for i in range(n - 1):
        p1 = points[i]
        xi1, yi1 = x_map[p1[0]], y_map[p1[1]]
        
        for j in range(i + 1, n):
            p2 = points[j]
            area = (abs(p1[1] - p2[1]) + 1) * (abs(p1[0] - p2[0]) + 1)
            if area <= max_found:
                continue

            xi2, yi2 = x_map[p2[0]], y_map[p2[1]]
            x_start = xi1 if xi1 < xi2 else xi2
            x_end   = xi2 if xi1 < xi2 else xi1
            y_start = yi1 if yi1 < yi2 else yi2
            y_end   = yi2 if yi1 < yi2 else yi1
            
            actual_sum = pref[x_end][y_end] - pref[x_start][y_end] - pref[x_end][y_start] + pref[x_start][y_start]
            expected_sum = (x_end - x_start) * (y_end - y_start)
            if actual_sum == expected_sum:
                max_found = area
                    
    return max_found

if __name__ == '__main__':
    part1()
    part2()
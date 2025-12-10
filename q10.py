from utils import run_solver, cache_by_id, dprint
import math

TEST_INPUT = r'''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'''
TEST_OUTPUT1 = 7
TEST_OUTPUT2 = 33

@run_solver("Part 1", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT1)])
def part1(d: list[str]) -> int:
    total = 0
    trans = str.maketrans({'.': '0', '#': '1'})
    
    for line in d:
        parts = line.split()
        target = int(parts[0][1:-1][::-1].translate(trans), 2)
        if target == 0:
            continue
            
        buttons = []
        for p in parts[1:-1]:
            mask = 0
            for x in p[1:-1].split(','):
                mask |= (1 << int(x))
            buttons.append(mask)
            
        n = len(buttons)
        mid = n // 2
        
        left_map = {0: 0}
        for b in buttons[:mid]:
            for m, p in list(left_map.items()):
                nm = m ^ b
                np = p + 1
                if nm not in left_map or np < left_map[nm]:
                    left_map[nm] = np
                    
        right_map = {0: 0}
        for b in buttons[mid:]:
            for m, p in list(right_map.items()):
                nm = m ^ b
                np = p + 1
                if nm not in right_map or np < right_map[nm]:
                    right_map[nm] = np
        
        min_presses = float('inf')
        for mask, pop in right_map.items():
            needed = target ^ mask
            if needed in left_map:
                cost = pop + left_map[needed]
                if cost < min_presses:
                    min_presses = cost
                    
        if min_presses != float('inf'):
            total += min_presses
            
    return total

def solve_linear_equation(button_idx: list[tuple[int, ...]], target: list[int]):
    num_lights = len(target)
    num_buttons = len(button_idx)

    var_upper_bounds = []
    for affected in button_idx:
        var_upper_bounds.append(min(target[i] for i in affected))
    matrix = [[0] * (num_buttons + 1) for _ in range(num_lights)]
    for c, indices in enumerate(button_idx):
        for r in indices:
            matrix[r][c] = 1
    for r in range(num_lights):
        matrix[r][num_buttons] = target[r]

    pivot_row = 0
    pivots = []
    pivot_cols = set()
    for c in range(num_buttons):
        if pivot_row >= num_lights:
            break
            
        curr = pivot_row
        while curr < num_lights and matrix[curr][c] == 0:
            curr += 1
        
        if curr == num_lights:
            continue
            
        matrix[pivot_row], matrix[curr] = matrix[curr], matrix[pivot_row]
        if matrix[pivot_row][c] < 0:
            matrix[pivot_row] = [-x for x in matrix[pivot_row]]
        
        pivot_val = matrix[pivot_row][c]
        for r in range(num_lights):
            if r != pivot_row and matrix[r][c] != 0:
                factor = matrix[r][c]
                mr = matrix[r]
                mp = matrix[pivot_row]
                new_row = [0] * (num_buttons + 1)
                
                row_gcd = 0
                for k in range(num_buttons + 1):
                    val = mr[k] * pivot_val - mp[k] * factor
                    new_row[k] = val
                    if val != 0:
                        if row_gcd == 0:
                            row_gcd = abs(val)
                        else:
                            row_gcd = math.gcd(row_gcd, val)
                if row_gcd > 1:
                    for k in range(num_buttons + 1):
                        new_row[k] //= row_gcd
                matrix[r] = new_row

        pivots.append((pivot_row, c))
        pivot_cols.add(c)
        pivot_row += 1

    for r in range(pivot_row, num_lights):
        if matrix[r][num_buttons] != 0:
            return float('inf')

    free_vars = [c for c in range(num_buttons) if c not in pivot_cols]
    F = len(free_vars)
    pivot_constraints = []
    free_var_slopes = {f: 1.0 for f in free_vars}
    
    for r, p_col in pivots:
        P = matrix[r][p_col]
        RHS = matrix[r][num_buttons]
        coeffs = []
        for f in free_vars:
            C_f = matrix[r][f]
            if C_f != 0:
                coeffs.append((C_f, f))
                free_var_slopes[f] -= C_f / P
        pivot_constraints.append((p_col, P, RHS, coeffs))
    free_vars.sort(key=lambda x: abs(free_var_slopes[x]), reverse=True)

    min_total = float('inf')
    def dfs(idx, current_assign, current_free_sum):
        nonlocal min_total, F, free_vars, pivot_constraints, var_upper_bounds
        if current_free_sum >= min_total:
            return

        if idx == F:
            current_total = current_free_sum
            for p_col, P, RHS, coeffs in pivot_constraints:
                val = RHS
                for coeff, f_col in coeffs:
                    val -= coeff * current_assign[f_col]
                x_p, rem = divmod(val, P)
                if not (rem == 0 and 0 <= x_p <= var_upper_bounds[p_col]):
                    return
                current_total += x_p
            
            if current_total < min_total:
                min_total = current_total
            return

        f_col = free_vars[idx]
        low = 0
        high = var_upper_bounds[f_col]
        for p_col, P, RHS, coeffs in pivot_constraints:
            rem = RHS
            curr_coeff = 0
            min_future = 0
            max_future = 0
            
            for coeff, fc in coeffs:
                if fc in current_assign:
                    rem -= coeff * current_assign[fc]
                elif fc == f_col:
                    curr_coeff = coeff
                elif coeff > 0:
                    max_future += coeff * var_upper_bounds[fc]
                else:
                    min_future += coeff * var_upper_bounds[fc]
            
            p_bound = var_upper_bounds[p_col]            
            numer_upper = rem - min_future
            numer_lower = rem - max_future - P * p_bound
            if curr_coeff == 0:
                if numer_upper < 0 or numer_lower > 0:
                    return
                else:
                    continue
            elif curr_coeff > 0:
                upper = numer_upper // curr_coeff
                lower = numer_lower // curr_coeff
            else:
                upper = -(numer_lower // -curr_coeff)
                lower = -(numer_upper // -curr_coeff)

            if high > upper:
                high = upper
            if low < lower:
                low = lower

        if low > high:
            return

        slope = free_var_slopes[f_col]
        r_range = range(low, high + 1)
        if slope < 0:
            r_range = range(high, low - 1, -1)
            
        for val in r_range:
            current_assign[f_col] = val
            dfs(idx + 1, current_assign, current_free_sum + val)
            del current_assign[f_col]

    dfs(0, {}, 0)
    return int(min_total) if min_total != float('inf') else float('inf')


@run_solver("Part 2", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT2)])
def part2(d: list[str]) -> int:
    total = 0
    for line in d:
        *button_list, joltage = line.split()[1:]
        buttons = []
        for b in button_list:
            buttons.append(tuple(map(int, b[1:-1].split(','))))
        joltage = list(map(int, joltage[1:-1].split(',')))
        res = solve_linear_equation(buttons, joltage)
        total += res
    return total

if __name__ == '__main__':
    part1()
    part2()
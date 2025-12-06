from utils import run_solver, dprint

TEST_INPUT = r'''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +   '''
TEST_OUTPUT1 = 4277556
TEST_OUTPUT2 = 3263827


@run_solver("Part 1", submit_result=False, benchmark=True, tests=[(TEST_INPUT, TEST_OUTPUT1)])
def part1(d: list[str]) -> int:
    matrix = [line.split() for line in d[:-1]]
    ops = d[-1].split()
    total = 0
    for c in range(len(ops)):
        val = int(matrix[0][c])
        op = ops[c]
        if op == '*':
            for r in range(1, len(matrix)):
                val *= int(matrix[r][c])
        else:
            for r in range(1, len(matrix)):
                val += int(matrix[r][c])
        total += val
    return total


@run_solver("Part 2", submit_result=False, strip_lines=False, tests=[(TEST_INPUT, TEST_OUTPUT2)])
def part2(d: list[str]) -> int:
    rows = d[:-1]
    ops = d[-1]
    
    total = 0
    val = 0
    mul = False
    for x in range(len(ops)):
        op = ops[x]
        num = 0
        has_digit = False
        
        for r in rows:
            if x < len(r):
                c = r[x]
                if c != ' ':
                    num = num * 10 + (ord(c) - 48)
                    has_digit = True
        
        if op == '*':
            val = num
            mul = True
        elif op == '+':
            val = num
            mul = False
        else:
            if has_digit:
                if mul:
                    val *= num
                else:
                    val += num
            else:
                total += val
                val = 0

    total += val
    return total

if __name__ == '__main__':
    part1()
    part2()


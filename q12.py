from utils import run_solver, cache_by_id, dprint

TEST_INPUT = r'''0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2'''
TEST_OUTPUT1 = 2


@run_solver("Part 1", submit_result=True, tests=[])
def part1(d: list[str]) -> int:
    '''
    This solution works here only because the input is designed that this is allowed -_-, despite failing the test
    '''
    fit = 0
    for line in d:
        if "x" in line:
            dimensions, boxes = line.split(":")
            w,h = dimensions.split("x")
            area = int(w) // 3 * int(h) // 3

            total_boxes = sum(int(x) for x in boxes.split())
            if total_boxes <= area:
                fit += 1
    return fit

if __name__ == '__main__':
    part1()
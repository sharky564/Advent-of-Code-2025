from utils import run_solver, cache_by_id
from collections import defaultdict

TEST_INPUT1 = r'''aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out'''

TEST_INPUT2 = r'''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out'''

TEST_OUTPUT1 = 5
TEST_OUTPUT2 = 2

@cache_by_id
def process_data(d: list[str]):
    vals = defaultdict(list)
    parsed = dict(map(lambda line: line.split(': '), d))
    for k, v in parsed.items():
        vals[k] = sorted(v.split())
    return vals

def num_paths(grid, start, end, avoid):
    memo = {}
    def count_dfs(current_node):
        if current_node == end:
            return 1
        
        if current_node in memo:
            return memo[current_node]
        
        total_paths = 0
        for neighbor in grid.get(current_node, []):
            if neighbor not in avoid:
                total_paths += count_dfs(neighbor)
        
        memo[current_node] = total_paths
        return total_paths

    return count_dfs(start)

@run_solver("Part 1", submit_result=False, tests=[(TEST_INPUT1, TEST_OUTPUT1)])
def part1(d: list[str]) -> int:
    data = process_data(d)
    total = num_paths(data, 'you', 'out', [])
    return total

@run_solver("Part 2", submit_result=True, tests=[(TEST_INPUT2, TEST_OUTPUT2)])
def part2(d: list[str]) -> int:
    data = process_data(d)
    
    total11 = num_paths(data, 'svr', 'fft', {'dac', 'out'})
    total12 = num_paths(data, 'fft', 'dac', {'out'})
    total13 = num_paths(data, 'dac', 'out', {})
    
    total21 = num_paths(data, 'svr', 'dac', {'fft', 'out'})
    total22 = num_paths(data, 'dac', 'fft', {'out'})
    total23 = num_paths(data, 'fft', 'out', {})

    return (total11 * total12 * total13) + (total21 * total22 * total23)

if __name__ == '__main__':
    part1()
    part2()
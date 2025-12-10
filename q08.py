from utils import run_solver, cache_by_id, dprint
import heapq

TEST_INPUT = r'''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689'''

TEST_OUTPUT1 = 40
TEST_OUTPUT2 = 25272

@cache_by_id
def process_data(d: list[str]):
    return [tuple(map(int, line.split(','))) for line in d]

class UnionFind:
    __slots__ = ['parent', 'size', 'components']

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, i):
        root = i
        while root != self.parent[root]:
            root = self.parent[root]
        curr = i
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt
        return root

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            self.components -= 1
            return True
        return False

def gen(data):
    n = len(data)
    for i in range(n - 1):
        x1, y1, z1 = data[i]
        for j in range(i + 1, n):
            x2, y2, z2 = data[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist_sq = dx*dx + dy*dy + dz*dz
            yield (dist_sq, i, j)

def get_heaped_edges(limit, data):
    if limit == -1:
        candidates = list(gen(data))
        heapq.heapify(candidates)
        return candidates
    else:
        return heapq.nsmallest(limit, gen(data))


@run_solver("Part 1", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT1)], profile=True)
def part1(d: list[str]) -> int:
    data = process_data(d)
    n = len(data)
    limit = 10 if n == 20 else 1000
    
    dsu = UnionFind(n)
    for _, u, v in get_heaped_edges(limit, data):
        dsu.union(u, v)
    component_sizes = {}
    for i in range(n):
        root = dsu.find(i)
        component_sizes[root] = dsu.size[root]
        
    sizes = heapq.nlargest(3, component_sizes.values())
    return sizes[0] * sizes[1] * sizes[2]

@run_solver("Part 2", submit_result=False, tests=[(TEST_INPUT, TEST_OUTPUT2)], profile=True)
def part2(d: list[str]) -> int:
    data = process_data(d)
    n = len(data)
    dsu = UnionFind(n)
    edges = get_heaped_edges(-1, data)
    while True:
        _, u, v = heapq.heappop(edges)
        if dsu.union(u, v):
            if dsu.components == 1:
                return data[u][0] * data[v][0]

if __name__ == '__main__':
    part1()
    part2()
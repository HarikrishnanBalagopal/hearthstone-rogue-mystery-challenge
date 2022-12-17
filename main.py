from collections import deque


class Graph:
    def __init__(self, root):
        self.vs = {}
        self.vs[hash(root)] = {}

    def v_exists(self, v):
        return hash(v) in self.vs

    def add_v(self, src, edge, v):
        self.vs[hash(v)] = {}
        self.vs[hash(src)][edge] = hash(v)

    def add_edge(self, src, edge, v):
        self.vs[hash(src)][edge] = hash(v)


def hash(v):
    return (
        v[6] * 10**6
        + v[5] * 10**5
        + v[4] * 10**4
        + v[3] * 10**3
        + v[2] * 10**2
        + v[1] * 10**1
        + v[0] * 10**0
    )


def add(v1, v2):
    return [(x + y) % 10 for x, y in zip(v1, v2)]


def sub(v1, v2):
    return [(x - y) % 10 for x, y in zip(v1, v2)]


def create_graph(edges, goal, source):
    source_hash = hash(source)
    graph = Graph(goal)
    q = deque()
    q.append(goal)
    while len(q) > 0:
        curr = q.popleft()
        for i, edge in enumerate(edges):
            new_v = sub(curr, edge)
            if graph.v_exists(new_v):
                graph.add_edge(curr, i, new_v)
                continue
            graph.add_v(curr, i, new_v)
            print(new_v)
            print(f"{hash(new_v):07}")
            if hash(new_v) == source_hash:
                print("reached the source!!!!")
                return graph
            q.append(new_v)
    raise "failed to reach the source"


def dfs(graph, goal, source):
    path = [(-1, goal)]
    visited = set()
    path, ok = dfs_helper(graph, source, visited, goal, path)
    if not ok:
        raise "failed to find the path"
    return path


def dfs_helper(graph, source, visited, curr, path):
    if curr == source:
        return path, True
    visited.add(curr)
    for e, v in graph.vs[curr].items():
        if v in visited:
            continue
        new_path, ok = dfs_helper(graph, source, visited, v, path + [(e, v)])
        if ok:
            return new_path, True
    return path, False


def sanity(path, goal, source, edges):
    path_es = [e for e, _ in path]
    # print(path_es)
    path_es.reverse()
    path_es = path_es[:-1]
    print("the hits to make are", [i + 1 for i in path_es])

    print("the code after each hit is shown below")
    curr = source
    print(curr)
    for e_idx in path_es:
        e = edges[e_idx]
        # print('->', e)
        curr = add(curr, e)
        print(curr)
    if hash(curr) == hash(goal):
        print("the path is correct!")
    else:
        raise "the path is incorrect!"


def main():
    goal = [4, 4, 4, 4, 4, 4, 4]
    # goal = [7, 4, 5, 8, 2, 2, 5]
    source = [5, 1, 0, 2, 0, 5, 2]
    edges = [
        [1, 2, 1, -2, 2, 0, -3],
        [-2, 1, -2, -2, 3, -2, -2],
        [0, -2, 1, 1, 2, -2, -2],
        [0, 0, 1, 1, -2, 3, -3],
        [-3, 0, -1, 2, 1, -2, 3],
        [2, 3, 2, -3, 0, 1, 1],
        [-2, -2, -1, -3, 0, 3, 1],
    ]
    print(f"trying to reach the source {hash(source)} from the goal {hash(goal)}")
    graph = create_graph(edges, goal, source)
    print("done creating the graph")
    # print(graph.vs)
    print(f"reached the source {hash(source)} from the goal {hash(goal)}")
    print("-" * 100)
    path = dfs(graph, hash(goal), hash(source))
    # print("path", path)
    sanity(path, goal, source, edges)
    print("#" * 100)


main()

import time
import sys
import tracemalloc
from collections import deque


#  -------- GRAPH REPRESENTAION --------

# Graph a: numeric vertices 0–11 with undirected edges
GRAPH_A_EDGES = [
    (0, 2), (0, 3), (0, 7), (0, 8),
    (1, 2), (1, 3), (1, 4),
    (3, 5),
    (4, 6),
    (5, 7),
    (6, 9), (6, 11),
    (8, 10),
    (9, 11),
]
GRAPH_A_NODES = list(range(12)) 

# Graph b: alphabetic vertices A–O with undirected edges 
GRAPH_B_EDGES = [
    ('A', 'B'), ('A', 'C'),
    ('B', 'D'), ('B', 'G'),
    ('C', 'D'),
    ('D', 'E'), ('D', 'J'),
    ('E', 'F'), ('E', 'K'),
    ('F', 'G'), ('F', 'H'), ('F', 'K'), ('F', 'M'),
    ('G', 'H'), ('G', 'K'), ('G', 'L'), ('G', 'N'),
    ('H', 'I'), ('H', 'J'),
    ('I', 'J'),
    ('K', 'L'),
    ('M', 'O'),
    ('N', 'O'),
]
GRAPH_B_NODES = list('ABCDEFGHIJKLMNO')



#  -------- BUILD REPRESENTATIONS --------

def build_adjacency_list(nodes, edges):
    adj = {n: [] for n in nodes}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj

def build_adjacency_matrix(nodes, edges):
    idx = {n: i for i, n in enumerate(nodes)}
    n = len(nodes)
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[idx[u]][idx[v]] = 1
        matrix[idx[v]][idx[u]] = 1
    return idx, matrix

# -------- BFS (adjacency list) --------

def bfs_list(adj, start, goal):
    visited = {start}
    queue = deque([[start]])
    nodes_visited = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_visited += 1

        if node == goal:
            return path, nodes_visited

        for neighbour in adj[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])

    return None, nodes_visited

# -------- BFS (adjacency matrix) --------

def bfs_matrix(nodes, idx, matrix, start, goal):
    visited = {start}
    queue = deque([[start]])
    nodes_visited = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_visited += 1

        if node == goal:
            return path, nodes_visited

        row = idx[node]
        for col, connected in enumerate(matrix[row]):
            if connected:
                neighbour = nodes[col]
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(path + [neighbour])

    return None, nodes_visited

#  -------- DFS (adjacency list) --------

def dfs_list(adj, start, goal):
    visited = set()
    stack = [[start]]
    nodes_visited = 0

    while stack:
        path = stack.pop()
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)
        nodes_visited += 1

        if node == goal:
            return path, nodes_visited

        for neighbour in reversed(adj[node]):
            if neighbour not in visited:
                stack.append(path + [neighbour])

    return None, nodes_visited

# -------- DFS (adjacency matrix) --------

def dfs_matrix(nodes, idx, matrix, start, goal):
    visited = set()
    stack = [[start]]
    nodes_visited = 0

    while stack:
        path = stack.pop()
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)
        nodes_visited += 1

        if node == goal:
            return path, nodes_visited

        row = idx[node]
        for col in reversed(range(len(matrix[row]))):
            if matrix[row][col]:
                neighbour = nodes[col]
                if neighbour not in visited:
                    stack.append(path + [neighbour])

    return None, nodes_visited

#  -------- TIMING & MEMORY ANALYSIS --------

def benchmark(func, *args, runs=5):
    times = []
    mems = []
    path = None
    visited = None

    for _ in range(runs):
        tracemalloc.start()
        t0 = time.perf_counter()

        path, visited = func(*args)

        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append((t1 - t0) * 1000)
        mems.append(peak)

    avg_time = sum(times) / runs
    avg_mem = sum(mems)  / runs
    return path, visited, avg_time, avg_mem

# -------- PRINTING HELPERS --------

def print_adjacency_list(adj, label):
    print(f"\n")
    print(f"Adjacency List  -  {label}")
    
    for node in sorted(adj.keys(), key=str):
        neighbours = ", ".join(str(n) for n in adj[node])
        print(f"  {str(node):>3} : [{neighbours}]")


def print_adjacency_matrix(nodes, matrix, label):
    print(f"\n")
    print(f"Adjacency Matrix  -  {label}")
    header = "     " + "  ".join(f"{str(n):>2}" for n in nodes)
    print(header)
    print("     " + "─" * (len(nodes) * 4))
    for i, node in enumerate(nodes):
        row_str = "  ".join(str(matrix[i][j]) for j in range(len(nodes)))
        print(f"  {str(node):>2} | {row_str}")


def print_result(algo, rep, path, nodes_visited, avg_time, avg_mem):
    path_str = " -> ".join(str(n) for n in path) if path else "No path found"
    print(f"\n[{algo} | {rep}]")
    print(f"Path: {path_str}")
    print(f"Nodes visited: {nodes_visited}")
    print(f"Avg time (5 runs): {avg_time:.6f} ms")
    print(f"Avg memory: {avg_mem / 1024:.4f} KB")

#  -------- MAIN --------

def run_graph(label, nodes, edges, start, goal):
    print(f"\n")
    print(f"GRAPH {label}   |   Start: {start}   ->   Goal: {goal}")

    # Build both representations
    adj = build_adjacency_list(nodes, edges)
    idx, matrix = build_adjacency_matrix(nodes, edges)

    # Print representations
    print_adjacency_list(adj, f"Graph {label}")
    print_adjacency_matrix(nodes, matrix, f"Graph {label}")

    # -- BFS --
    print(f"\n")
    print("BFS RESULTS")

    path, nv, t, m = benchmark(bfs_list, adj, start, goal)
    print_result("BFS", "Adjacency List  ", path, nv, t, m)

    path, nv, t, m = benchmark(bfs_matrix, nodes, idx, matrix, start, goal)
    print_result("BFS", "Adjacency Matrix", path, nv, t, m)

    # -- DFS --
    print(f"\n")
    print("DFS RESULTS")

    path, nv, t, m = benchmark(dfs_list, adj, start, goal)
    print_result("DFS", "Adjacency List  ", path, nv, t, m)

    path, nv, t, m = benchmark(dfs_matrix, nodes, idx, matrix, start, goal)
    print_result("DFS", "Adjacency Matrix", path, nv, t, m)


def main():
    print("-" * 55)
    print("BFS vs DFS - Graph Traversal Assignment")
    print("-" * 55)

    # Graph a
    run_graph("(a)", GRAPH_A_NODES, GRAPH_A_EDGES, start=0, goal=7)

    # Graph b
    run_graph("(b)", GRAPH_B_NODES, GRAPH_B_EDGES, start='A', goal='O')

    # Analysis Summary
    print(f"\n")
    print("ANALYSIS & COMPARISON SUMMARY IN README.md")

if __name__ == "__main__":
    main()
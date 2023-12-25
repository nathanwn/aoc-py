import sys

from aoclib.graph.graph import UndiGraph


def find_bridges(g: UndiGraph) -> list[tuple[int, int]]:
    timer = -1
    visited = [False for _ in range(g.n)]
    time_in = [-1 for _ in range(g.n)]
    low = [-1 for _ in range(g.n)]
    # low[u] = min(
    #     time_in[u],
    #     time_in[p] for all p where u -> p is a back edge
    #     low[v] for all v where u -> v is a tree edge
    # )
    # An edge (u, v) in the DFS tree is a bridge iff time_in[u] < low[v]
    # Intuition: the edge (u, v) is a bridge if it is the only way to reach v
    # from the root of the dfs tree.

    bridges = []

    def dfs(u: int, p: int = -1):
        nonlocal timer
        timer += 1
        visited[u] = True
        time_in[u] = timer
        low[u] = time_in[u]

        for v in g.adj[u]:
            if v == p:
                continue
            if visited[v]:  # back edge
                low[u] = min(low[u], time_in[v])
            else:  # tree edge
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if time_in[u] < low[v]:
                    bridges.append((u, v))

    sys.setrecursionlimit(int(1e9))
    for u in range(g.n):
        if not visited[u]:
            dfs(u)

    return bridges

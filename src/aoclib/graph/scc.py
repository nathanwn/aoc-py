import sys
from collections.abc import Sequence

from aoclib.graph.graph import DiGraph


def reverse(g: DiGraph) -> DiGraph:
    gt = DiGraph(g.n)

    for u in range(g.n):
        for v in g.adj[u]:
            gt.add_edge(v, u)

    return gt


class SCC:
    def __init__(self, g: DiGraph) -> None:
        self.g = g
        self.gt = reverse(g)

    def topo_sort(self) -> Sequence[int]:
        mark = [0 for _ in range(self.g.n)]
        order = []

        def dfs(u: int) -> None:
            mark[u] = 1
            for v in self.g.adj[u]:
                if mark[v] == 0:
                    dfs(v)
            mark[u] = 2
            order.append(u)

        for u in range(self.g.n):
            if mark[u] == 0:
                dfs(u)

        order.reverse()
        return order

    def scc(self) -> Sequence[int]:
        sys.setrecursionlimit(int(1e9))
        mark = [0 for _ in range(self.g.n)]
        leaders = [_ for _ in range(self.g.n)]

        def dfs(u: int, leader: int) -> None:
            mark[u] = 1
            leaders[u] = leader
            for v in self.gt.adj[u]:
                if mark[v] == 0:
                    dfs(v, leader)
            mark[u] = 2

        topo_order = self.topo_sort()
        assert len(topo_order) == self.g.n
        assert len(topo_order) == self.gt.n
        for u in topo_order:
            if mark[u] == 0:
                dfs(u, u)

        return leaders

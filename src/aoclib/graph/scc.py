import sys
from collections.abc import Sequence

from aoclib.graph.graph import DiGraph


class SCC:
    def __init__(self, g: DiGraph) -> None:
        self.g = g
        self.gt = g.reverse()

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

        topo_order = self.g.topo_sort()
        assert len(topo_order) == self.g.n
        assert len(topo_order) == self.gt.n
        for u in topo_order:
            if mark[u] == 0:
                dfs(u, u)

        return leaders

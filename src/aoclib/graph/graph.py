from __future__ import annotations

from collections.abc import Sequence


class DiGraph:
    def __init__(self, n: int) -> None:
        self.n = n
        self.adj: list[list[int]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)

    def topo_sort(self) -> Sequence[int]:
        mark = [0 for _ in range(self.n)]
        order = []

        def dfs(u: int) -> None:
            mark[u] = 1
            for v in self.adj[u]:
                if mark[v] == 0:
                    dfs(v)
            mark[u] = 2
            order.append(u)

        for u in range(self.n):
            if mark[u] == 0:
                dfs(u)

        order.reverse()
        return order

    def reverse(self) -> DiGraph:
        gt = DiGraph(self.n)

        for u in range(self.n):
            for v in self.adj[u]:
                gt.add_edge(v, u)

        return gt

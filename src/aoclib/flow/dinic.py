from collections import deque
from dataclasses import dataclass


@dataclass
class FlowEdge:
    u: int
    v: int
    c: float
    f: float


class Dinic:
    def __init__(
        self,
        n: int,
        s: int,
        t: int,
        inf: float = 1e9,
        eps: float = 1e-9,
    ) -> None:
        self.n = n
        self.s = s
        self.t = t
        self.inf = inf
        self.eps = eps
        self.adj: list[list[int]] = [[] for _ in range(n)]  # stores indices of edges
        self.level = [0 for _ in range(n)]  # shortest distance from source
        self.ptr = [0 for _ in range(n)]  # the next edge that can be used
        self.edges: list[FlowEdge] = []

    def add_edge(self, u: int, v: int, c: float, rc: float = 0) -> None:
        eid = len(self.edges)
        self.adj[u].append(eid)
        self.adj[v].append(eid + 1)
        self.edges.append(FlowEdge(u, v, c, 0))
        self.edges.append(FlowEdge(v, u, rc, 0))

    def bfs(self) -> bool:
        self.level = [-1 for _ in range(self.n)]
        self.level[self.s] = 0
        q: deque[int] = deque([self.s])

        while len(q) > 0:
            u = q.popleft()
            for eid in self.adj[u]:
                e = self.edges[eid]
                if e.c - e.f <= self.eps or self.level[e.v] != -1:
                    continue
                self.level[e.v] = self.level[u] + 1
                q.append(e.v)

        return self.level[self.t] != -1

    def dfs(self, u: int, flow: float) -> float:
        if u == self.t:
            return flow

        for j in range(self.ptr[u], len(self.adj[u])):
            eid = self.adj[u][j]
            e = self.edges[eid]
            if e.c - e.f > 0 and self.level[e.v] == self.level[u] + 1:
                df = self.dfs(e.v, min(e.c - e.f, flow))
                if df > 0:
                    self.edges[eid].f += df
                    self.edges[eid ^ 1].f -= df
                    return df

        return 0

    def max_flow(self) -> float:
        f: float = 0

        while self.bfs():
            self.ptr = [0 for _ in range(self.n)]
            total_df: float = 0
            while True:
                df = self.dfs(self.s, self.inf)
                if df <= self.eps:
                    break
                total_df += df
            if total_df <= self.eps:
                break
            f += total_df

        return f

    def get_min_cut(self) -> list[int]:
        self.bfs()
        return [u for u in range(self.n) if self.level[u] != -1]

    def get_min_cut_capacity(self) -> float:
        cut = self.get_min_cut()
        min_cut_cap: float = 0
        for u in cut:
            for eid in self.adj[u]:
                e = self.edges[eid]
                if self.level[e.v] == -1:
                    min_cut_cap += e.c
        return min_cut_cap

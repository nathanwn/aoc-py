class DSU:
    def __init__(self, n: int):
        self.n = n
        self.leader = [i for i in range(n)]
        self.depth = [0 for _ in range(n)]

    def find(self, u: int) -> int:
        while self.leader[u] != u:
            u = self.leader[u]
        return u

    def merge(self, u: int, v: int) -> bool:
        u = self.find(u)
        v = self.find(v)
        if u == v:
            return False
        if self.depth[u] < self.depth[v]:
            self.leader[u] = v
        else:
            self.leader[v] = u
            if self.depth[u] == self.depth[v]:
                self.depth[u] += 1
        return True

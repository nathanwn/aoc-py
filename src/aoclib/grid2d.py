from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import NamedTuple


class Di4(Enum):
    U = "U"
    D = "D"
    L = "L"
    R = "R"


class Pos(NamedTuple):
    r: int
    c: int

    def inside(self, g: Sequence[Sequence[str]]) -> bool:
        return 0 <= self.r < len(g) and 0 <= self.c < len(g[0])

    def go(self, d: Di4) -> Pos:
        if d == Di4.U:
            return Pos(self.r - 1, self.c)
        if d == Di4.D:
            return Pos(self.r + 1, self.c)
        if d == Di4.L:
            return Pos(self.r, self.c - 1)
        if d == Di4.R:
            return Pos(self.r, self.c + 1)
        assert False


class State(NamedTuple):
    pos: Pos
    dir: Di4

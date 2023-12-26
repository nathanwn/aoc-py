from __future__ import annotations

from collections.abc import Sequence
from enum import IntEnum
from typing import NamedTuple


class Di4(IntEnum):
    U = 0
    D = 1
    L = 2
    R = 3


def turn_left(d: Di4) -> Di4:
    if d == Di4.U:
        return Di4.L
    elif d == Di4.L:
        return Di4.D
    elif d == Di4.D:
        return Di4.R
    else:
        return Di4.U


def turn_right(d: Di4) -> Di4:
    if d == Di4.U:
        return Di4.R
    elif d == Di4.R:
        return Di4.D
    elif d == Di4.D:
        return Di4.L
    else:
        return Di4.U


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

    def manhattan(self, other: Pos) -> int:
        return abs(self.r - other.r) + abs(self.c - other.c)


class State(NamedTuple):
    pos: Pos
    dir: Di4

    def __repr__(self) -> str:
        return f"State(pos={tuple(self.pos)},dir={Di4(self.dir).name})"


def parse_grid(input: str) -> list[list[str]]:
    return [[c for c in line] for line in input.splitlines()]


def format_grid(g: list[list[str]]):
    return "\n".join(["".join([c for c in line]) for line in g])

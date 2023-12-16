from __future__ import annotations

import sys
import argparse
from enum import Enum
from typing import NamedTuple
from queue import Queue
from collections import defaultdict


class Direction(Enum):
    U = "U"
    D = "D"
    L = "L"
    R = "R"


class Position(NamedTuple):
    r: int
    c: int

    def inside(self, g: list[str]) -> bool:
        return 0 <= self.r < len(g) and 0 <= self.c < len(g[0])

    def go(self, d: Direction) -> Position:
        if d == Direction.U:
            return Position(self.r - 1, self.c)
        if d == Direction.D:
            return Position(self.r + 1, self.c)
        if d == Direction.L:
            return Position(self.r, self.c - 1)
        if d == Direction.R:
            return Position(self.r, self.c + 1)
        assert False


class State(NamedTuple):
    dir: Direction
    pos: Position


Visited = list[list[dict[Direction, bool]]]


def compute(g: list[str], s: State) -> int:
    visited: Visited = [[defaultdict(lambda: False) for j in range(len(g[0]))] for i in range(len(g))]
    q: Queue[State] = Queue()
    q.put(s)

    while not q.empty():
        u = q.get()
        p = u.pos
        d = u.dir
        if (not p.inside(g)) or visited[p.r][p.c][d]:
            continue

        visited[p.r][p.c][d] = True
        cell = g[p.r][p.c]
        if cell == ".":
            q.put(State(dir=d, pos=p.go(d)))
        elif cell == "/":
            m = {
                Direction.U: Direction.R,
                Direction.L: Direction.D,
                Direction.R: Direction.U,
                Direction.D: Direction.L,
            }
            d = m[d]
            q.put(State(dir=d, pos=p.go(d)))
        elif cell == "\\":
            m = {
                Direction.U: Direction.L,
                Direction.L: Direction.U,
                Direction.R: Direction.D,
                Direction.D: Direction.R,
            }
            d = m[d]
            q.put(State(dir=d, pos=p.go(d)))
        elif cell == "|":
            if d not in [Direction.U, Direction.D]:
                q.put(State(dir=Direction.U, pos=Position(p.r - 1, p.c)))
                q.put(State(dir=Direction.D, pos=Position(p.r + 1, p.c)))
            else:
                q.put(State(dir=d, pos=p.go(d)))
        elif cell == "-":
            if d not in [Direction.L, Direction.R]:
                q.put(State(dir=Direction.L, pos=Position(p.r, p.c - 1)))
                q.put(State(dir=Direction.R, pos=Position(p.r, p.c + 1)))
            else:
                q.put(State(dir=d, pos=p.go(d)))
        else:
            assert False

    energized = [['#' if True in visited[i][j].values() else '.' for j in range(len(g[0]))] for i in range(len(g))]

    ans = 0
    for row in energized:
        for cell in row:
            if cell == "#":
                ans += 1

    return ans


def part1(input: str) -> int:
    g = input.splitlines()
    s = State(dir=Direction.R, pos=Position(0, 0))
    ans = compute(g, s)
    return ans


def part2(input: str) -> int:
    g = input.splitlines()
    ans = 0

    for c in range(len(g[0])):
        r = 0
        p = Position(r, c)
        s = State(dir=Direction.D, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    for c in range(len(g[0])):
        r = len(g) - 1
        p = Position(r, c)
        s = State(dir=Direction.U, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    for r in range(len(g)):
        c = 0
        p = Position(r, c)
        s = State(dir=Direction.R, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    for r in range(len(g)):
        c = len(g[0]) - 1
        p = Position(r, c)
        s = State(dir=Direction.L, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    return ans


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2"])
    parser.add_argument("input_file")

    args = parser.parse_args()

    with open(args.input_file, mode="r", encoding="utf-8") as f:
        input = f.read().strip()

    if args.part == "1":
        print(f"Part 1: {part1(input)}")
    else:
        print(f"Part 2: {part2(input)}")


if __name__ == "__main__":
    main()

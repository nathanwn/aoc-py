from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict
from collections.abc import Callable
from enum import Enum
from queue import Queue
from typing import NamedTuple

import pytest

from aoclib.grid2d import Di4, Pos, State
from aoclib.util import read_file

Visited = list[list[dict[Di4, bool]]]


def compute(g: list[str], s: State) -> int:
    visited: Visited = [
        [defaultdict(bool) for j in range(len(g[0]))] for i in range(len(g))
    ]
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
                Di4.U: Di4.R,
                Di4.L: Di4.D,
                Di4.R: Di4.U,
                Di4.D: Di4.L,
            }
            d = m[d]
            q.put(State(dir=d, pos=p.go(d)))
        elif cell == "\\":
            m = {
                Di4.U: Di4.L,
                Di4.L: Di4.U,
                Di4.R: Di4.D,
                Di4.D: Di4.R,
            }
            d = m[d]
            q.put(State(dir=d, pos=p.go(d)))
        elif cell == "|":
            if d not in [Di4.U, Di4.D]:
                q.put(State(dir=Di4.U, pos=Pos(p.r - 1, p.c)))
                q.put(State(dir=Di4.D, pos=Pos(p.r + 1, p.c)))
            else:
                q.put(State(dir=d, pos=p.go(d)))
        elif cell == "-":
            if d not in [Di4.L, Di4.R]:
                q.put(State(dir=Di4.L, pos=Pos(p.r, p.c - 1)))
                q.put(State(dir=Di4.R, pos=Pos(p.r, p.c + 1)))
            else:
                q.put(State(dir=d, pos=p.go(d)))
        else:
            assert False

    energized = [
        ["#" if True in visited[i][j].values() else "." for j in range(len(g[0]))]
        for i in range(len(g))
    ]

    ans = 0
    for row in energized:
        for cell in row:
            if cell == "#":
                ans += 1

    return ans


def part1(input: str) -> int:
    g = input.splitlines()
    s = State(dir=Di4.R, pos=Pos(0, 0))
    ans = compute(g, s)
    return ans


def part2(input: str) -> int:
    g = input.splitlines()
    ans = 0

    for c in range(len(g[0])):
        r = 0
        p = Pos(r, c)
        s = State(dir=Di4.D, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    for c in range(len(g[0])):
        r = len(g) - 1
        p = Pos(r, c)
        s = State(dir=Di4.U, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    for r in range(len(g)):
        c = 0
        p = Pos(r, c)
        s = State(dir=Di4.R, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    for r in range(len(g)):
        c = len(g[0]) - 1
        p = Pos(r, c)
        s = State(dir=Di4.L, pos=p)
        res = compute(g, s)
        print(f"{r=} {c=} {res=}", file=sys.stderr)
        ans = max(ans, res)

    return ans


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2"])
    parser.add_argument("input_file")

    args = parser.parse_args()

    with open(args.input_file, encoding="utf-8") as f:
        input = f.read().strip()

    if args.part == "1":
        print(f"Part 1: {part1(input)}")
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "input.txt", 8551),
        (part2, "input.txt", 8754),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    main()

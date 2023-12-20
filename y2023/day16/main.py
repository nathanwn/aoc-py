from __future__ import annotations

import argparse
import os
import sys
from collections import deque
from collections.abc import Callable

import pytest

from aoclib.grid2d import Di4, Pos, State
from aoclib.util import read_file

Visited = list[list[list[bool]]]


def get_next_states(u: State, ch: str) -> list[State]:
    next_states = []
    p = u.pos
    d = u.dir

    if ch == ".":
        next_states.append(State(dir=d, pos=p.go(d)))
    elif ch == "/":
        m = {
            Di4.U: Di4.R,
            Di4.L: Di4.D,
            Di4.R: Di4.U,
            Di4.D: Di4.L,
        }
        d = m[d]
        next_states.append(State(dir=d, pos=p.go(d)))
    elif ch == "\\":
        m = {
            Di4.U: Di4.L,
            Di4.L: Di4.U,
            Di4.R: Di4.D,
            Di4.D: Di4.R,
        }
        d = m[d]
        next_states.append(State(dir=d, pos=p.go(d)))
    elif ch == "|":
        if d not in [Di4.U, Di4.D]:
            next_states.append(State(dir=Di4.U, pos=Pos(p.r - 1, p.c)))
            next_states.append(State(dir=Di4.D, pos=Pos(p.r + 1, p.c)))
        else:
            next_states.append(State(dir=d, pos=p.go(d)))
    elif ch == "-":
        if d not in [Di4.L, Di4.R]:
            next_states.append(State(dir=Di4.L, pos=Pos(p.r, p.c - 1)))
            next_states.append(State(dir=Di4.R, pos=Pos(p.r, p.c + 1)))
        else:
            next_states.append(State(dir=d, pos=p.go(d)))
    else:
        assert False

    return next_states


def compute(g: list[str], s: State) -> int:
    visited: Visited = [
        [[False for d in range(len(Di4))] for j in range(len(g[0]))]
        for i in range(len(g))
    ]
    q: deque[State] = deque()
    q.append(s)
    visited[s.pos.r][s.pos.c][s.dir] = True

    while len(q) > 0:
        u = q.popleft()
        ch = g[u.pos.r][u.pos.c]
        next_states = get_next_states(u, ch)

        for v in next_states:
            if (not v.pos.inside(g)) or visited[v.pos.r][v.pos.c][v.dir]:
                continue
            q.append(v)
            visited[v.pos.r][v.pos.c][v.dir] = True

    energized = [
        [
            "#" if any(visited[i][j][d] for d in range(len(Di4))) else "."
            for j in range(len(g[0]))
        ]
        for i in range(len(g))
    ]

    ans = 0
    for row in energized:
        for ch in row:
            if ch == "#":
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

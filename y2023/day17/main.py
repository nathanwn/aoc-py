from __future__ import annotations

import argparse
import heapq
import os
from collections import defaultdict
from collections.abc import Callable
from typing import NamedTuple

import pytest

from aoclib.grid2d import Di4, Pos, parse_grid, turn_left, turn_right
from aoclib.util import read_file

INF = int(1e9)


class State(NamedTuple):
    pos: Pos
    dir: Di4
    same_dir: int


class Entry(NamedTuple):
    state: State
    cost: int

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Entry):
            return self.cost < other.cost
        raise TypeError()


def solve(input: str, min_same_dir: int, max_same_dir: int) -> int:
    g = parse_grid(input)
    n = len(g)
    m = len(g[0])

    s = Pos(0, 0)
    t = Pos(n - 1, m - 1)

    cost: dict[State, int] = defaultdict(lambda: INF)
    start_states = [State(pos=s, dir=d, same_dir=0) for d in [Di4.R, Di4.D]]
    q: list[Entry] = []
    for ss in start_states:
        cost[ss] = 0
        entry = Entry(state=ss, cost=0)
        heapq.heappush(q, entry)

    t_state = None

    while len(q) > 0:
        u = heapq.heappop(q)
        u_pos, u_dir, u_same_dir = u.state

        if t == u_pos and u_same_dir >= min_same_dir:
            t_state = u.state
            break

        if cost[u.state] < u.cost:
            continue

        dirs = [u_dir]
        if u.state.same_dir >= min_same_dir:
            dirs.append(turn_left(u_dir))
            dirs.append(turn_right(u_dir))

        for dir in dirs:
            if dir == u_dir:
                if u.state.same_dir == max_same_dir:
                    continue
                v_same_dir = u_same_dir + 1
            else:
                v_same_dir = 1
            v_pos = u_pos.go(dir)
            v_state = State(pos=v_pos, dir=dir, same_dir=v_same_dir)
            if not v_pos.inside(g):
                continue
            w = int(g[v_pos.r][v_pos.c])
            if cost[u.state] + w < cost[v_state]:
                cost[v_state] = cost[u.state] + w
                v = Entry(
                    state=v_state,
                    cost=cost[v_state],
                )
                heapq.heappush(q, v)

    assert t_state is not None
    return cost[t_state]


def part1(input: str) -> int:
    return solve(input, 0, 3)


def part2(input: str) -> int:
    return solve(input, 4, 10)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2", "d"])
    parser.add_argument("input_file")

    try:
        args = parser.parse_args()
    except SystemExit:
        return 1

    input = read_file(args.input_file)

    if args.part == "1":
        print(f"Part 1: {part1(input)}")
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "sample.txt", 102),
        (part2, "sample.txt", 94),
        (part2, "sample2.txt", 71),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

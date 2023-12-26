from __future__ import annotations

import argparse
import os
import pprint
from collections import defaultdict, deque
from collections.abc import Callable

import pytest

from aoclib.grid2d import Di4, Pos, State
from aoclib.util import read_file


def find_start(g: list[list[str]]) -> Pos:
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == "S":
                return Pos(r, c)
    assert False


def get_cycle(g: list[list[str]]) -> list[State]:
    start = find_start(g)

    visited = [[False for c in range(len(g[0]))] for r in range(len(g))]
    visited[start.r][start.c] = True
    neighbors: list[State] = []

    dir_map = {
        Di4.U: {"|": Di4.U, "7": Di4.L, "F": Di4.R},
        Di4.D: {"|": Di4.D, "J": Di4.L, "L": Di4.R},
        Di4.L: {"-": Di4.L, "L": Di4.U, "F": Di4.D},
        Di4.R: {"-": Di4.R, "J": Di4.U, "7": Di4.D},
    }

    for d in Di4:
        nxt = start.go(d)
        if nxt.inside(g) and g[nxt.r][nxt.c] in dir_map[d].keys():
            neighbors.append(State(pos=start.go(d), dir=d))

    assert len(neighbors) == 2
    node = neighbors[0]
    cycle = [node]
    while node.pos != start:
        p = node.pos
        ch = g[p.r][p.c]
        d = dir_map[node.dir][ch]
        node = State(pos=p.go(d), dir=d)
        cycle.append(node)

    return cycle


def part1(input: str) -> int:
    g = [[c for c in line] for line in input.splitlines()]
    cycle = get_cycle(g)
    pprint.pprint(cycle)
    return len(cycle) // 2


def part2(input: str) -> int:
    g = [[c for c in line] for line in input.splitlines()]
    g2 = [["." for c in range(len(g[0]) * 3)] for r in range(len(g) * 3)]

    shape_map = defaultdict(list)
    shape_map["|"] = [(0, 1), (1, 1), (2, 1)]
    shape_map["-"] = [(1, 0), (1, 1), (1, 2)]
    shape_map["7"] = [(1, 0), (1, 1), (2, 1)]
    shape_map["F"] = [(1, 2), (1, 1), (2, 1)]
    shape_map["J"] = [(0, 1), (1, 1), (1, 0)]
    shape_map["L"] = [(0, 1), (1, 1), (1, 2)]
    shape_map["S"] = [
        *[(0, 0), (0, 1), (0, 2)],
        *[(1, 0), (1, 1), (1, 2)],
        *[(2, 0), (2, 1), (2, 2)],
    ]

    for r in range(len(g)):
        for c in range(len(g[0])):
            for rr, cc in shape_map[g[r][c]]:
                g2[3 * r + rr][3 * c + cc] = "x"

    visited = [[False for c in range(len(g2[0]))] for r in range(len(g2))]
    start = find_start(g)
    visited[start.r * 3][start.c * 3] = True
    q: deque[Pos] = deque()

    for r in range(len(g2)):
        q.append(Pos(r, 0))
        q.append(Pos(r, len(g2[0]) - 1))
        visited[r][0] = True
        visited[r][len(g2[0]) - 1] = True
    for c in range(len(g2[0])):
        q.append(Pos(0, c))
        q.append(Pos(len(g2) - 1, c))
        visited[0][c] = True
        visited[len(g2) - 1][c] = True

    while len(q) > 0:
        u = q.popleft()

        for d in Di4:
            v = u.go(d)
            if v.inside(g2) and g2[v.r][v.c] == "." and not visited[v.r][v.c]:
                q.append(v)
                visited[v.r][v.c] = True

    ans = 0
    for r in range(len(g)):
        for c in range(len(g[0])):
            passed = False
            for rr in range(3):
                for cc in range(3):
                    if visited[r * 3 + rr][c * 3 + cc]:
                        passed = True
            if not passed:
                g[r][c] = "Y"
                ans += 1

    return ans


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2"])
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
        (part1, "sample1.txt", 4),
        (part1, "sample2.txt", 8),
        (part1, "input.txt", 6815),
        (part2, "sample3.txt", 4),
        (part2, "sample4.txt", 8),
        (part2, "sample5.txt", 10),
        (part2, "input.txt", 269),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    raise SystemExit(main())

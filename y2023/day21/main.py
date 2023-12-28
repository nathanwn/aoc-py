from __future__ import annotations

import argparse
import os
from collections.abc import Callable, Sequence

import pytest

from aoclib.grid2d import Di4, Pos, parse_grid
from aoclib.util import read_file


def find_start(g: Sequence[Sequence[str]]) -> Pos:
    n = len(g)
    m = len(g[0])
    for i in range(n):
        for j in range(m):
            if g[i][j] == "S":
                return Pos(i, j)
    assert False


def solve_1(g: Sequence[Sequence[str]], steps=64) -> int:
    n = len(g)
    m = len(g[0])
    dp = [[[0 for k in range(steps + 1)] for j in range(m)] for i in range(n)]

    s = find_start(g)
    dp[s.r][s.c][0] = 1

    for k in range(1, steps + 1):
        for r in range(n):
            for c in range(m):
                u = Pos(r, c)
                if dp[u.r][u.c][k - 1] == 0:
                    continue
                for d in Di4:
                    v = u.go(d)
                    if not v.inside(g) or g[v.r][v.c] == "#":
                        continue
                    dp[v.r][v.c][k] |= dp[u.r][u.c][k - 1]

    ans = 0

    for r in range(n):
        for c in range(m):
            ans += dp[r][c][steps]

    return ans


def part1(input: str) -> int:
    g = parse_grid(input)
    return solve_1(g)


def part2(input: str) -> int:
    return 0


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


@pytest.mark.skip  # remove me
@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "sample.txt", -1),
        (part2, "sample.txt", -1),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

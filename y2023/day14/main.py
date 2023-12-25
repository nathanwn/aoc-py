from __future__ import annotations

import argparse
import os
from collections.abc import Callable

import pytest

from aoclib.util import read_file


def tilt_north(g: list[list[str]]) -> None:
    n = len(g)
    m = len(g[0])
    for i in range(n):
        for j in range(m):
            c = g[i][j]
            if c == "O":
                for k in range(i - 1, -1, -1):
                    if g[k][j] != ".":
                        break
                    g[k + 1][j], g[k][j] = g[k][j], g[k + 1][j]


def tilt_south(g: list[list[str]]) -> None:
    n = len(g)
    m = len(g[0])
    for i in range(n - 1, -1, -1):
        for j in range(m):
            c = g[i][j]
            if c == "O":
                for k in range(i + 1, n):
                    if g[k][j] != ".":
                        break
                    g[k - 1][j], g[k][j] = g[k][j], g[k - 1][j]


def tilt_west(g: list[list[str]]) -> None:
    n = len(g)
    m = len(g[0])
    for j in range(m):
        for i in range(n):
            c = g[i][j]
            if c == "O":
                for k in range(j - 1, -1, -1):
                    if g[i][k] != ".":
                        break
                    g[i][k + 1], g[i][k] = g[i][k], g[i][k + 1]


def tilt_east(g: list[list[str]]) -> None:
    n = len(g)
    m = len(g[0])
    for j in range(m - 1, -1, -1):
        for i in range(n):
            c = g[i][j]
            if c == "O":
                for k in range(j + 1, m):
                    if g[i][k] != ".":
                        break
                    g[i][k - 1], g[i][k] = g[i][k], g[i][k - 1]


def txt(g: list[list[str]]) -> str:
    return "\n".join(["".join([c for c in line]) for line in g])


def calc(g: list[list[str]]) -> int:
    n = len(g)
    m = len(g[0])
    ans = 0
    for i in range(n):
        for j in range(m):
            c = g[i][j]
            if c == "O":
                ans += n - i
    return ans


def parse(input: str) -> list[list[str]]:
    return list(map(lambda line: [c for c in line], input.splitlines()))


def part1(input: str) -> int:
    g = parse(input)
    return calc(g)


def rotate(g: list[list[str]]) -> None:
    tilt_north(g)
    tilt_west(g)
    tilt_south(g)
    tilt_east(g)


def part2(input: str) -> int:
    N = 1000000000
    g = parse(input)
    cache: dict[str, int] = {}  # key: txt(g); val: index when g first encountered
    for i in range(N):
        rotate(g)
        s = txt(g)
        if s in cache:
            cycle = i - cache[s]
            k = (N - 1 - i) % cycle
            for _ in range(k):
                rotate(g)
            return calc(g)
        cache[s] = i
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2"])
    parser.add_argument("input_file")

    args = parser.parse_args()
    input = read_file(args.input_file)

    if args.part == "1":
        print(f"Part 1: {part1(input)}")
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "sample.txt", 104),
        (part1, "input.txt", 101106),
        (part2, "sample.txt", 64),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

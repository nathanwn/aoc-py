from __future__ import annotations

import argparse
import os
import pprint
import sys
from collections.abc import Callable, Sequence

import pytest

from aoclib.util import read_file

Grid = list[list[str]]


def column_eq(g: Grid, l: int, r: int) -> bool:
    n = len(g)
    return all(g[i][l] == g[i][r] for i in range(n))


def row_eq(g: Grid, a: int, b: int) -> bool:
    m = len(g[0])
    return all(g[a][j] == g[b][j] for j in range(m))


def check_horizontal_reflection(g: Grid, avoid: int) -> int | None:
    n = len(g)

    def check(k: int) -> bool:
        for i in range(k + 1):
            a = k - i
            b = k + i + 1
            if b >= n:
                return True
            if not row_eq(g, a, b):
                return False
        return True

    for k in range(0, n - 1):
        assert avoid is not None
        if k + 1 != avoid and check(k):
            return k + 1
    return None


def check_vertical_reflection(g: Grid, avoid: int) -> int | None:
    m = len(g[0])

    def check(k: int) -> bool:
        for i in range(k + 1):
            l = k - i
            r = k + i + 1
            if r >= m:
                return True
            if not column_eq(g, l, r):
                return False
        return True

    for k in range(0, m - 1):
        if k + 1 != avoid and check(k):
            return k + 1
    return None


def check_after_mutation(
    g: Grid,
    checker: Callable[..., int | None],
    avoid: int | None,
) -> int | None:
    n = len(g)
    m = len(g[0])
    avoid = avoid or -1
    for i in range(n):
        for j in range(m):
            if g[i][j] == ".":
                g[i][j] = "#"
            else:
                g[i][j] = "."
            v = checker(g, avoid=avoid)
            # revert
            if g[i][j] == ".":
                g[i][j] = "#"
            else:
                g[i][j] = "."

            if v is not None and v != avoid:
                return v
    return None


def parse(input: str) -> list[Grid]:
    return list(
        map(
            lambda p: [[c for c in line] for line in p],
            map(
                lambda _: _.splitlines(),
                input.split("\n\n"),
            ),
        )
    )


def check_reflections(g: Grid) -> tuple[int | None, int | None]:
    v = check_vertical_reflection(g, -1)
    h = check_horizontal_reflection(g, -1)
    return v, h


def part1(input: str) -> int:
    gs = parse(input)
    ans = 0
    for i, g in enumerate(gs):
        v, h = check_reflections(g)
        if v is not None:
            ans += v
        if h is not None:
            ans += h * 100

    return ans


def part2(input: str) -> int:
    gs = parse(input)
    ans = 0
    for i, g in enumerate(gs):
        v, h = check_reflections(g)
        vv = check_after_mutation(g, check_vertical_reflection, v)
        hh = check_after_mutation(g, check_horizontal_reflection, h)
        if vv is not None and vv != v:
            ans += vv
        if hh is not None and hh != h:
            ans += hh * 100

    return ans


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
    elif args.part == "d":
        print(part2(input))
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "sample.txt", 405),
        (part1, "input.txt", 37561),
        (part2, "sample.txt", 400),
        (part2, "input.txt", 31108),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

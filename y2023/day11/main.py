from __future__ import annotations

import argparse
import os
import pprint
from collections.abc import Callable
from functools import partial

import pytest

from aoclib.grid2d import Pos
from aoclib.util import read_file


def solve(input: str, expand: int) -> int:
    g = list(map(lambda line: [c for c in line], input.splitlines()))
    pprint.pprint(g)
    R = len(g)
    C = len(g[0])

    # prefix sum arrays
    # empty_rows[r + 1] - empty_rows[l]: number of empty rows in the range[l, r]
    empty_rows = [0]
    empty_cols = [0]

    for r in range(R):
        row_empty = True
        for c in range(C):
            if g[r][c] == "#":
                row_empty = False
                break
        val = empty_rows[-1]
        if row_empty:
            val += 1
        empty_rows.append(val)
    for c in range(R):
        col_empty = True
        for r in range(C):
            if g[r][c] == "#":
                col_empty = False
                break
        val = empty_cols[-1]
        if col_empty:
            val += 1
        empty_cols.append(val)

    nodes: list[Pos] = []

    for r in range(R):
        for c in range(C):
            if g[r][c] == "#":
                nodes.append(Pos(r, c))

    N = len(nodes)
    ans = 0

    for i in range(N):
        for j in range(i + 1, N):
            res = nodes[i].manhattan(nodes[j])
            minr = min(nodes[i].r, nodes[j].r)
            maxr = max(nodes[i].r, nodes[j].r)
            minc = min(nodes[i].c, nodes[j].c)
            maxc = max(nodes[i].c, nodes[j].c)
            res += (empty_rows[maxr + 1] - empty_rows[minr]) * (expand - 1)
            res += (empty_cols[maxc + 1] - empty_cols[minc]) * (expand - 1)
            print(f"s={i+1} t={j+1} {res=}")
            ans += res

    return ans


def part1(input: str) -> int:
    return solve(input, expand=2)


def part2(input: str) -> int:
    return solve(input, expand=1000000)


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
        (part1, "sample.txt", 374),
        (partial(solve, expand=10), "sample.txt", 1030),
        (partial(solve, expand=100), "sample.txt", 8410),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Callable
from functools import reduce
import pprint


def parse(input: str) -> list[list[int]]:
    arrs = []
    for line in input.splitlines():
        ai = list(map(int, line.split()))
        arrs.append(ai)
    return arrs


def solve(a: list[int]) -> int:
    cur = a[:]
    d = [cur]

    while not all_zero(cur):
        cur = []
        for i in range(len(d[-1]) - 1):
            cur.append(d[-1][i + 1] - d[-1][i])
        d.append(cur)

    d[-1].append(0)

    for i in range(len(d) - 2, -1, -1):
        d[i].append(d[i][-1] + d[i + 1][-1])

    return d[0][-1]


def all_zero(a: list[int]) -> int:
    return all(x == 0 for x in a)


def part1(input: str) -> int:
    arrs = parse(input)
    return sum([solve(a) for a in arrs])


def part2(input: str) -> int:
    arrs = parse(input)
    for a in arrs:
        a.reverse()
    return sum([solve(a) for a in arrs])


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

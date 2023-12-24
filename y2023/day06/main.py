from __future__ import annotations

import argparse
import math
import os
from collections.abc import Callable
from typing import NamedTuple

import pytest

from aoclib.util import read_file


class Record(NamedTuple):
    t: int
    d: int


def parse_input_1(input: str) -> list[Record]:
    lines = input.split("\n")
    vals = []
    for line in lines:
        _, _, nums_input = line.rpartition(":")
        nums_input = nums_input.strip()
        vals.append(list(map(int, nums_input.split())))
    assert len(vals[0]) == len(vals[1])
    return [Record(vals[0][i], vals[1][i]) for i in range(len(vals[0]))]


def parse_input_2(input: str) -> Record:
    lines = input.split("\n")
    vals = []
    for line in lines:
        _, _, num_input = line.rpartition(":")
        num_input = num_input.strip()
        num = int("".join(num_input.split()))
        vals.append(num)
    return Record(vals[0], vals[1])


def solve_1(r: Record) -> int:
    ans = 0
    for v in range(1, r.t):
        d = v * (r.t - v)
        if d > r.d:
            ans += 1
    return ans


def solve_2(r: Record) -> int:
    def f_distance(v) -> int:
        return v * (r.t - v)

    def find_best_speed(r: Record) -> int:
        low = 1
        high = r.t

        while low < high:
            m = (low + high) // 2
            if f_distance(m) > f_distance(m + 1):
                high = m
            else:
                low = m + 1

        return low

    def find_lowest_speed(low: int, high: int) -> int:
        ans = -1
        while low <= high:
            mid = low + (high - low) // 2
            if f_distance(mid) > r.d:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        assert ans != -1
        return ans

    def find_highest_speed(low: int, high: int) -> int:
        ans = -1
        while low <= high:
            mid = low + (high - low) // 2
            if f_distance(mid) > r.d:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        assert ans != -1
        return ans

    v_best = find_best_speed(r)
    v_low = find_lowest_speed(1, v_best)
    v_high = find_highest_speed(v_best, r.t - 1)
    return v_high - v_low + 1


def part1(input: str) -> int:
    records = parse_input_1(input)
    sols = [solve_1(r) for r in records]
    sols2 = [solve_2(r) for r in records]
    assert sols == sols2
    return math.prod(sols)


def part2(input: str) -> int:
    r = parse_input_2(input)
    return solve_2(r)


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
        (part1, "sample.txt", 288),
        (part1, "input.txt", 140220),
        (part2, "sample.txt", 71503),
        (part2, "input.txt", 39570185),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

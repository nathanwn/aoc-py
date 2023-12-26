from __future__ import annotations

import argparse
import os
from collections.abc import Callable

import pytest

from aoclib.util import read_file


def part1(input: str) -> int:
    return 0


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

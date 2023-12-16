import argparse
import os
from collections import defaultdict
from collections.abc import Callable
from typing import NamedTuple

import pytest

from aoclib.util import read_file


class Num(NamedTuple):
    row: int
    col_start: int
    col_end: int
    val: int


class Symbol(NamedTuple):
    row: int
    col: int
    char: str


def new_num(grid: list[str], row: int, col_start: int, col_end: int) -> Num:
    return Num(
        row,
        col_start,
        col_end,
        val=int(grid[row][col_start : col_end + 1]),
    )


def new_symbol(grid: list[str], row: int, col: int) -> Symbol:
    return Symbol(row, col, grid[row][col])


def adjacent_symbols(num: Num, grid: list[str]) -> list[Symbol]:
    height = len(grid)
    width = len(grid[0])
    symbols = []

    # left
    if num.col_start - 1 >= 0 and grid[num.row][num.col_start - 1] != ".":
        symbols.append(new_symbol(grid, num.row, num.col_start - 1))
    # right
    if num.col_end + 1 < width and grid[num.row][num.col_end + 1] != ".":
        symbols.append(new_symbol(grid, num.row, num.col_end + 1))
    # top
    if num.row > 0:
        for col in range(max(0, num.col_start - 1), min(num.col_end + 2, width)):
            if grid[num.row - 1][col] != ".":
                symbols.append(new_symbol(grid, num.row - 1, col))
    # bottom
    if num.row < height - 1:
        for col in range(max(0, num.col_start - 1), min(num.col_end + 2, width)):
            if grid[num.row + 1][col] != ".":
                symbols.append(new_symbol(grid, num.row + 1, col))

    return symbols


def extract_nums(grid: list[str]) -> list[Num]:
    nums: list[Num] = []

    for row in range(len(grid)):
        col_start = -1
        for col in range(len(grid[row])):
            c = grid[row][col]
            if not c.isdigit():
                if col_start != -1:
                    nums.append(new_num(grid, row, col_start, col - 1))
                    col_start = -1
            elif col_start == -1:
                col_start = col
        if col_start != -1:
            nums.append(new_num(grid, row, col_start, len(grid[row]) - 1))

    return nums


def part1(input: str) -> int:
    grid = input.splitlines()
    nums = extract_nums(grid)
    ans = 0
    for num in nums:
        if len(adjacent_symbols(num, grid)) > 0:
            ans += num.val
    return ans


def part2(input: str):
    grid = input.splitlines()
    nums = extract_nums(grid)
    gear_adjacents: dict[Symbol, list[Num]] = defaultdict(list)

    for num in nums:
        symbols = adjacent_symbols(num, grid)
        for symbol in symbols:
            if symbol.char != "*":
                continue
            gear_adjacents[symbol].append(num)

    ans = 0
    for _, adjacents in gear_adjacents.items():
        if len(adjacents) == 2:
            ans += adjacents[0].val * adjacents[1].val

    return ans


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
        (part1, "sample.txt", 4361),
        (part1, "input.txt", 526404),
        (part2, "sample.txt", 467835),
        (part2, "input.txt", 84399773),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    raise SystemExit(main())

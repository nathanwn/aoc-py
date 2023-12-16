import argparse
import os
from collections.abc import Callable

import pytest

from aoclib.util import read_file


def score(win: list[int], have: list[int]) -> int:
    s = 0
    for x in have:
        if x in win:
            s += 1
    return s


def parse_line(line: str) -> tuple[list[int], list[int]]:
    _, _, nums = line.partition(":")
    win_nums, _, have_nums = nums.partition("|")
    win = list(map(lambda _: int(_), win_nums.strip().split()))
    have = list(map(lambda _: int(_), have_nums.strip().split()))
    return win, have


def part1(input: str) -> int:
    ans = 0
    for line in input.splitlines():
        win, have = parse_line(line)
        s = score(win, have)
        ans += 0 if s == 0 else (1 << (s - 1))
    return ans


def part2(input: str):
    lines = input.splitlines()
    cnt = [1 for _ in range(len(lines))]
    for i, line in enumerate(lines):
        win, have = parse_line(line)
        s = score(win, have)
        for j in range(i + 1, min(i + s + 1, len(lines))):
            cnt[j] += cnt[i]
    return sum(cnt)


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
        (part1, "sample.txt", 13),
        (part1, "input.txt", 25004),
        (part2, "sample.txt", 30),
        (part2, "input.txt", 14427616),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    raise SystemExit(main())

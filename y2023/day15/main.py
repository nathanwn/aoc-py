from __future__ import annotations

import argparse
import os
from collections.abc import Callable
from typing import NamedTuple

import pytest

from aoclib.util import read_file


def encode(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


class Len(NamedTuple):
    label: str
    focal_len: int


class PushStep(NamedTuple):
    len: Len


class PopStep(NamedTuple):
    label: str


Step = PushStep | PopStep


def part1(input: str) -> int:
    steps = input.split(",")
    return sum([encode(step) for step in steps])


def is_push_step(step_s: str) -> bool:
    return "=" in step_s


def parse_step(step_s: str) -> Step:
    if "=" in step_s:
        parts = step_s.split("=")
        return PushStep(len=Len(label=parts[0], focal_len=int(parts[1])))
    else:
        return PopStep(label=step_s[:-1])


def parse_steps(input: str) -> list[Step]:
    words = input.split(",")
    steps = [parse_step(word) for word in words]
    return steps


def part2(input: str) -> int:
    steps = parse_steps(input)
    m: list[list[Len]] = [[] for _ in range(256)]

    def find_label_in_bucket(h: int, label: str) -> int:
        for i in range(len(m[h])):
            if label == m[h][i].label:
                return i
        return -1

    for step in steps:
        if isinstance(step, PushStep):
            h = encode(step.len.label)
            i = find_label_in_bucket(h, step.len.label)
            if i != -1:
                m[h][i] = step.len
            else:
                m[h].append(step.len)
        else:
            h = encode(step.label)
            i = find_label_in_bucket(h, step.label)
            if i != -1:
                m[h].pop(i)

    ans = 0

    for h in range(len(m)):
        for i in range(len(m[h])):
            ans += (h + 1) * (i + 1) * m[h][i].focal_len

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
        (part1, "sample.txt", 1320),
        (part1, "input.txt", 501680),
        (part2, "sample.txt", 145),
        (part2, "input.txt", 241094),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

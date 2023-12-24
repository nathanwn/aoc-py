from __future__ import annotations

import argparse
import math
import os
from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce

import pytest

from aoclib.util import read_file


@dataclass
class RingBuffer:
    buf: str
    i: int = 0

    def get(self) -> str:
        i = self.i
        self.i += 1
        if self.i == len(self.buf):
            self.i = 0
        return self.buf[i]


def parse_edge_input(edge_input: str) -> tuple[dict[str, str], dict[str, str]]:
    lc = {}
    rc = {}

    for line in edge_input.splitlines():
        node, _, children = line.partition(" = ")
        children = children[1:-1]
        left, _, right = children.partition(", ")
        lc[node] = left
        rc[node] = right

    return lc, rc


def get_num_steps(
    lc: dict,
    rc: dict,
    seq: str,
    source: str,
    is_sink: Callable[[str], bool],
) -> int:
    buf = RingBuffer(seq)
    node = source
    ans = 0
    while not is_sink(node):
        ans += 1
        step = buf.get()
        if step == "L":
            node = lc[node]
        else:
            node = rc[node]
    return ans


def part1(input: str) -> int:
    seq, _, edge_input = input.partition("\n\n")
    lc, rc = parse_edge_input(edge_input)
    return get_num_steps(lc, rc, seq, source="AAA", is_sink=lambda _: _ == "ZZZ")


def part2(input: str) -> int:
    seq, _, edge_input = input.partition("\n\n")
    lc, rc = parse_edge_input(edge_input)
    nodes = list(lc.keys())
    sources = [node for node in nodes if node.endswith("A")]
    steps = [
        get_num_steps(
            lc,
            rc,
            seq,
            source=source,
            is_sink=lambda _: _.endswith("Z"),
        )
        for source in sources
    ]
    return reduce(math.lcm, steps, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2"])
    parser.add_argument("input_file")

    args = parser.parse_args()

    with open(args.input_file, encoding="utf-8") as f:
        input = f.read().strip()

    if args.part == "1":
        print(f"Part 1: {part1(input)}")
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "input.txt", 15517),
        (part2, "input.txt", 14935034899483),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

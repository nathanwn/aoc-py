from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Callable
from functools import reduce


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


def gcd(a: int, b: int) -> int:
    if a < b:
        a, b = b, a
    while b > 0:
        r = a % b
        a = b
        b = r
    return a


def lcd(a: int, b: int) -> int:
    return a // gcd(a, b) * b


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
    return reduce(lcd, steps, 1)


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

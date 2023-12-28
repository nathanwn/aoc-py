from __future__ import annotations

import argparse
import math
import os
from collections import Counter, defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import NamedTuple

import pytest

from aoclib.util import read_file


@dataclass
class Node:
    name: str
    adj: list[str]

    def receive(self, parent: str, pulse: int) -> int | None:
        return None


@dataclass
class Broadcaster(Node):
    def receive(self, parent: str, pulse: int) -> int | None:
        return pulse


@dataclass
class FlipFlop(Node):
    state: int = 0

    def receive(self, parent: str, pulse: int) -> int | None:
        if pulse == 1:
            return None
        self.state = 1 - self.state
        return self.state


@dataclass
class Conjunction(Node):
    mem: dict[str, int] = field(default_factory=dict)

    def receive(self, parent: str, pulse: int) -> int | None:
        self.mem[parent] = pulse
        return int(not all(self.mem.values()))


def parse_node(line: str) -> Node:
    u, vs = map(str.strip, line.split("->"))
    adj = list(map(str.strip, vs.split(",")))
    if u[0] == "%":
        return FlipFlop(name=u[1:], adj=adj)
    if u[0] == "&":
        return Conjunction(name=u[1:], adj=adj)
    if u == "broadcaster":
        return Broadcaster(name=u, adj=adj)
    return Node(name=u, adj=adj)


class Pulse(NamedTuple):
    p: str
    u: str
    pulse: int


def part1(input: str) -> int:
    nodes = {node.name: node for node in map(parse_node, input.splitlines())}
    for u in nodes:
        for v in nodes[u].adj:
            if v not in nodes:
                continue
            vnode = nodes[v]
            if isinstance(vnode, Conjunction):
                vnode.mem[u] = 0

    s = nodes["broadcaster"]
    c: Counter[int] = Counter()

    for i in range(1000):
        print(f"======={i}========")
        q: deque[Pulse] = deque([Pulse("button", s.name, 0)])
        while len(q) > 0:
            p, u, u_pulse = q.popleft()
            c[u_pulse] += 1
            LH = ["low", "high"]
            print(f"{p} -{LH[u_pulse]}-> {u}")

            if u not in nodes:
                continue

            v_pulse = nodes[u].receive(p, u_pulse)

            if v_pulse is None:
                continue

            for v in nodes[u].adj:
                q.append(Pulse(u, v, v_pulse))

    return math.prod(c.values())


def part2(input: str) -> int:
    nodes = {node.name: node for node in map(parse_node, input.splitlines())}
    parents: dict[str, list[str]] = defaultdict(list)
    for u in nodes:
        for v in nodes[u].adj:
            parents[v].append(u)
            if v not in nodes:
                continue
            vnode = nodes[v]
            if isinstance(vnode, Conjunction):
                vnode.mem[u] = 0
    s = nodes["broadcaster"]

    # This solution relies on looking at the pattern in the input
    # (which I'm not a very big fan of, but it is what it is.)

    # The output node "rx" has a single "special conjunction" as its parent
    assert len(parents["rx"]) == 1
    special_conjunction: str = parents["rx"][0]
    # The input signals feeding into the special conjunction
    feeds = set(parents[special_conjunction])
    first_seen = {}

    for i in range(1, int(1e18)):
        # print(f"{i=}")
        q: deque[Pulse] = deque([Pulse("button", s.name, 0)])

        while len(q) > 0:
            p, u, u_pulse = q.popleft()

            if u_pulse == 0:
                if u in feeds and u not in first_seen:
                    first_seen[u] = i
                if set(first_seen.keys()) == feeds:
                    print(list(first_seen.values()))
                    return math.lcm(*first_seen.values())

            if u not in nodes:
                continue

            v_pulse = nodes[u].receive(p, u_pulse)

            if v_pulse is None:
                continue

            for v in nodes[u].adj:
                q.append(Pulse(u, v, v_pulse))

    return -1


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
        (part1, "input.txt", 743090292),
        (part2, "input.txt", 241528184647003),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

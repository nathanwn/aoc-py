from __future__ import annotations

import argparse
import itertools
import math
import os
from collections import Counter
from collections.abc import Callable, Sequence

import pytest

from aoclib.flow.dinic import Dinic
from aoclib.graph.bridge import find_bridges
from aoclib.graph.graph import UndiGraph
from aoclib.structures.dsu import DSU
from aoclib.util import read_file


def parse_line(line: str) -> tuple[str, Sequence[str]]:
    parts = list(map(lambda _: _.strip(), line.split(": ")))
    u = parts[0]
    vs = list(map(lambda _: _.strip(), parts[1].split(" ")))
    return u, vs


def part1(input: str) -> int:
    # Running this with pypy3 took about 30 mins
    nodes: dict[str, int] = {}
    node_label: list[str] = []
    n = 0

    edges = []

    for line in input.splitlines():
        su, svs = parse_line(line)
        if su not in nodes:
            nodes[su] = n
            n += 1
            node_label.append(su)
        u = nodes[su]

        for sv in svs:
            if sv not in nodes:
                nodes[sv] = n
                n += 1
                node_label.append(sv)
            v = nodes[sv]
            if u < v:
                edges.append((u, v))
            else:
                edges.append((v, u))

    g = UndiGraph(n)

    for u, v in edges:
        g.add_edge(u, v)

    for s in range(n):
        for t in range(n):
            if s == t:
                continue

            dinic = Dinic(n=n, s=s, t=t)

            for u in range(g.n):
                for v in g.adj[u]:
                    dinic.add_edge(u, v, 1)

            max_flow = dinic.max_flow()
            if max_flow == 3:
                k = len(dinic.get_min_cut())
                ans = k * (n - k)
                return ans

    assert False


def part1_slow(input: str) -> int:
    # Running this with pypy3 took about 30 mins
    nodes: dict[str, int] = {}
    node_label: list[str] = []
    n = 0

    edges = []

    for line in input.splitlines():
        su, svs = parse_line(line)
        if su not in nodes:
            nodes[su] = n
            n += 1
            node_label.append(su)
        u = nodes[su]

        for sv in svs:
            if sv not in nodes:
                nodes[sv] = n
                n += 1
                node_label.append(sv)
            v = nodes[sv]
            if u < v:
                edges.append((u, v))
            else:
                edges.append((v, u))

    g = UndiGraph(n)

    for u, v in edges:
        g.add_edge(u, v)

    pairs = list(itertools.combinations(range(len(edges)), 2))

    disabled_triple = []

    for i, j in pairs:
        disabled_pair = [edges[i], edges[j]]
        # remove
        for u, v in disabled_pair:
            g.adj[u].remove(v)
            g.adj[v].remove(u)

        bridges = find_bridges(g)
        if len(bridges) == 1:
            disabled_triple = [*disabled_pair]
            u, v = bridges[0]
            if u > v:
                v, u = u, v
            disabled_triple.append((u, v))
            break

        # add back
        for u, v in disabled_pair:
            g.adj[u].append(v)
            g.adj[v].append(u)

    assert len(disabled_triple) == 3
    print(disabled_triple)

    dsu = DSU(n)
    components: Counter = Counter()
    for u in range(g.n):
        for v in g.adj[u]:
            if u < v and (u, v) not in disabled_triple:
                dsu.merge(u, v)
    for u in range(g.n):
        components[dsu.find(u)] += 1

    ans = math.prod(components.values())

    return ans


def part2(input: str) -> int:
    return 0


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
        (part1, "sample.txt", 54),
        (part1, "input.txt", 551196),
        # (part2, "sample.txt", -1),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

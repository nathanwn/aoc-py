from __future__ import annotations

import argparse
import os
from collections.abc import Callable
from typing import NamedTuple

import pytest

from aoclib.int_range import IntRange
from aoclib.util import read_file


def get_gap_range(this: IntRange, that: IntRange) -> IntRange | None:
    new_len = that.low - this.high - 1
    if new_len <= 0:
        return None
    return IntRange.from_len(this.high + 1, new_len)


class MapOp(NamedTuple):
    dest_start: int
    src_range: IntRange

    def contains(self, seed: int) -> bool:
        return self.src_range.contains(seed)

    def map_val(self, val: int) -> int:
        return val - self.src_range.low + self.dest_start

    def map_range(self, int_range: IntRange) -> IntRange:
        return IntRange.from_len(self.map_val(int_range.low), int_range.len)


def parse_seeds(seed_line: str) -> list[int]:
    _, _, seeds_part = seed_line.rpartition(":")
    seeds = list(map(int, seeds_part.split()))
    return seeds


def parse_seed_ranges(seed_line: str) -> list[IntRange]:
    _, _, seeds_part = seed_line.rpartition(":")
    vals = list(map(int, seeds_part.split()))
    res = []
    for i in range(0, len(vals), 2):
        res.append(IntRange.from_len(vals[i], vals[i + 1]))
    return res


def parse_map_layers(parts: list[str]) -> list[list[MapOp]]:
    layers = []
    for i in range(1, len(parts)):
        part = parts[i]
        _, _, range_input = part.rpartition(":")
        range_input = range_input.strip()
        range_lines = range_input.splitlines()
        layer = []
        for range_line in range_lines:
            line_parts = list(map(int, range_line.split()))
            layer.append(
                MapOp(line_parts[0], IntRange.from_len(line_parts[1], line_parts[2]))
            )
        layer.sort(key=lambda map_op: map_op.src_range.low)
        layers.append(layer)

    return layers


def map_result(val: int, layers: list[list[MapOp]]) -> int:
    for layer in layers:
        for map_range in layer:
            if map_range.contains(val):
                val = map_range.map_val(val)
                break
    return val


def apply_layer_to_range(val_range: IntRange, layer: list[MapOp]) -> list[IntRange]:
    res = []

    first = None
    last = None

    for i in range(len(layer)):
        op = layer[i]
        if val_range.join(layer[i].src_range) is not None:
            first = i
            break

    for i in range(len(layer) - 1, -1, -1):
        op = layer[i]
        if val_range.join(layer[i].src_range) is not None:
            last = i
            break

    if first is None and last is None:
        return [val_range]

    assert first is not None and last is not None

    overlap_ranges: list[IntRange] = []

    for i in range(first, last + 1):
        op = layer[i]
        overlap_range = val_range.join(op.src_range)
        if overlap_range is None:
            continue
        overlap_ranges.append(overlap_range)
        res_range = op.map_range(overlap_range)
        res.append(res_range)

    for j in range(len(overlap_ranges) - 1):
        gap = get_gap_range(overlap_ranges[j], overlap_ranges[j + 1])
        if gap is None:
            continue
        res.append(gap)

    if val_range.low < overlap_ranges[0].low:
        res.append(
            IntRange.from_len(
                low=val_range.low, len=overlap_ranges[0].low - val_range.low
            )
        )
    if overlap_ranges[-1].high < val_range.high:
        res.append(
            IntRange.from_len(
                low=overlap_ranges[-1].high + 1,
                len=val_range.high - overlap_ranges[-1].high,
            )
        )

    return res


def map_range(val_range: IntRange, layers: list[list[MapOp]]) -> list[IntRange]:
    vranges = [val_range]
    for layer in layers:
        new_vranges = []
        for vrange in vranges:
            new_vranges.extend(apply_layer_to_range(vrange, layer))
        vranges = new_vranges
    vranges.sort(key=lambda int_range: int_range.low)
    return vranges


def part1(input: str) -> int:
    parts = input.split("\n\n")
    seeds = parse_seeds(parts[0])
    layers = parse_map_layers(parts)
    ans = int(1e9)
    for seed in seeds:
        result = map_result(seed, layers)
        ans = min(ans, result)

    return ans


def part2(input: str) -> int:
    parts = input.split("\n\n")
    seed_ranges = parse_seed_ranges(parts[0])
    layers = parse_map_layers(parts)
    result_ranges = []
    for seed_range in seed_ranges:
        result_ranges.extend(map_range(seed_range, layers))
    result_ranges.sort(key=lambda int_range: int_range.low)
    return result_ranges[0].low


def part2_stupid(input: str) -> int:
    parts = input.split("\n\n")
    seed_ranges = parse_seed_ranges(parts[0])
    layers = parse_map_layers(parts)
    ans = int(1e9)

    for seed_range in seed_ranges:
        for seed in range(seed_range.low, seed_range.high + 1):
            result = map_result(seed, layers)
            ans = min(ans, result)

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
        part2_ans = part2(input)
        # part2_stupid_ans = part2_stupid(input)
        print(f"Part 2: {part2_ans}")
        # print(f"Part 2 (stupid): {part2_stupid_ans}")
        # assert part2_ans == part2_stupid_ans


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "sample.txt", 35),
        (part1, "input.txt", 389056265),
        (part2, "sample.txt", 46),
        (part2, "input.txt", 137516820),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    raise SystemExit(main())

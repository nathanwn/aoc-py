from __future__ import annotations

import argparse
import os
import re
from collections.abc import Callable
from functools import lru_cache

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from aoclib.util import read_file


def parse_line(line: str) -> tuple[str, tuple[int, ...]]:
    parts = line.split(" ")
    a = list(map(int, parts[1].split(",")))
    return parts[0], tuple(a)


def get_result(ss: list[str]) -> tuple[int, ...]:
    s = "".join(ss)
    parts = re.split(r"\.+", s)
    lens = tuple(filter(lambda _: _ != 0, [len(part) for part in parts]))
    return lens


@lru_cache(maxsize=None)
def solve(s: str, a: tuple[int, ...]) -> int:
    if len(s) == 0:
        if len(a) > 0:
            return 0
        else:
            return 1

    if s[0] == ".":
        non_dot = len(s)
        for i in range(1, len(s)):
            if s[i] != ".":
                non_dot = i
                break
        return solve(s[non_dot:], a)

    elif s[0] == "#":
        if len(a) == 0:
            return 0  # exhausted
        else:  # len(a) > 0
            if len(s) < a[0]:
                return 0
            # len(s) >= a[0]
            for i in range(a[0]):
                if s[i] == ".":
                    return 0
            if len(s) == a[0]:
                return solve(s[a[0] :], a[1:])
            # len(s) > a[0]
            if s[a[0]] == "#":
                return 0
            return solve(s[a[0] + 1 :], a[1:])
    else:  # s[0] == "?"
        assert s[0] == "?"

        ans = solve(s[1:], a)

        if len(a) == 0:
            return ans

        if a[0] > len(s):
            return ans
        else:
            for i in range(a[0]):
                if s[i] == ".":
                    # a[0] cannot start at s[0]
                    return ans

            if a[0] == len(s):
                return ans + solve(s[a[0] :], a[1:])
            else:
                if s[a[0]] == "#":
                    return ans
                return ans + solve(s[a[0] + 1 :], a[1:])


def solve_stupid(s: str, a: tuple[int, ...]) -> int:
    q = []
    for i, c in enumerate(s):
        if c == "?":
            q.append(i)

    res = 0
    for mask in range(1 << (len(q))):
        ss = [_ for _ in s]
        for i in range(len(q)):
            if mask & (1 << i) > 0:
                ss[q[i]] = "#"
            else:
                ss[q[i]] = "."
        rr = get_result(ss)
        if rr == a:
            res += 1

    return res


def part1(input: str) -> int:
    lines = input.splitlines()

    ans = 0
    for line in lines:
        s, a = parse_line(line)
        res = solve(s, a)
        ans += res
    return ans


def part2(input: str) -> int:
    lines = input.splitlines()

    ans = 0
    for line in lines:
        si, ai = parse_line(line)
        s = "?".join([si for _ in range(5)])
        a = ai * 5
        res = solve(s, a)
        ans += res

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
        (part1, "sample.txt", 21),
        (part1, "input.txt", 6827),
        (part2, "sample.txt", 525152),
        (part2, "input.txt", 1537505634471),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


def gen_test_case() -> st.SearchStrategy:
    chars = st.one_of(list(map(st.just, [".", "?", "#"])))
    s = st.lists(chars, min_size=5, max_size=12)
    a = st.lists(st.integers(min_value=1, max_value=3), min_size=1, max_size=4)
    return st.tuples(s, a)


@given(gen_test_case())
def test_solver(test_case: tuple[list[str], list[int]]):
    s, a = test_case
    cnt_quesion = s.count("?")
    cnt_hash = s.count("#")
    assume(sum(a) <= cnt_quesion + cnt_hash)
    ss = "".join(s)
    assert solve_stupid(ss, tuple(a)) == solve(ss, tuple(a))


if __name__ == "__main__":
    SystemExit(main())

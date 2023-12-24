from __future__ import annotations

import argparse
import os
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import NamedTuple

import pytest

from aoclib.util import read_file


@total_ordering
class HandType(Enum):
    FIVE = 6
    FOUR = 5
    FULL_HOUSE = 4
    THREE = 3
    TWO_PAIRS = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        raise NotImplemented


@dataclass
class BaseHand:
    s: str

    @property
    def hand_type(self) -> HandType:
        raise NotImplemented

    @property
    def hand_score(self) -> list[int]:
        raise NotImplemented

    def __lt__(self, other) -> bool:
        if self.hand_type == other.hand_type:
            return self.hand_score < other.hand_score
        return self.hand_type < other.hand_type


@dataclass
class Hand(BaseHand):
    @property
    def hand_type(self) -> HandType:
        counts: dict[str, int] = defaultdict(int)
        for c in self.s:
            counts[c] += 1
        count_vals = sorted(list(counts.values()), key=lambda _: -_)
        if count_vals == [5]:
            return HandType.FIVE
        if count_vals == [4, 1]:
            return HandType.FOUR
        if count_vals == [3, 2]:
            return HandType.FULL_HOUSE
        if count_vals == [3, 1, 1]:
            return HandType.THREE
        if count_vals == [2, 2, 1]:
            return HandType.TWO_PAIRS
        if count_vals == [2, 1, 1, 1]:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    @property
    def hand_score(self) -> list[int]:
        CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        return [CARDS.index(c) for c in self.s]


@dataclass
class JokerHand(BaseHand):
    @property
    def hand_type(self) -> HandType:
        counts: dict[str, int] = defaultdict(int)
        for c in self.s:
            counts[c] += 1

        count_rest = []

        for k in counts:
            if k != "J":
                count_rest.append(counts[k])

        count_rest = sorted(list(count_rest), key=lambda _: -_)

        count_jokers = 5 - sum(count_rest)

        if count_jokers == 0:
            return Hand(self.s).hand_type
        elif count_jokers == 1:
            if count_rest == [4]:
                return HandType.FIVE
            if count_rest == [3, 1]:
                return HandType.FOUR
            if count_rest == [2, 2]:
                return HandType.FULL_HOUSE
            if count_rest == [2, 1, 1]:
                return HandType.THREE
            if count_rest == [2, 1, 1]:
                return HandType.TWO_PAIRS
            return HandType.ONE_PAIR
        elif count_jokers == 2:
            if count_rest == [3]:
                return HandType.FIVE
            if count_rest == [2, 1]:
                return HandType.FOUR
            return HandType.THREE
        elif count_jokers == 3:
            if count_rest == [2]:
                return HandType.FIVE
            return HandType.FOUR
        return HandType.FIVE

    @property
    def hand_score(self) -> list[int]:
        CARDS = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
        return [CARDS.index(c) for c in self.s]


class Game(NamedTuple):
    hand: BaseHand
    bid: int


def parse_input(input: str, hand_cls: Callable[[str], BaseHand]) -> list[Game]:
    games = []
    for line in input.splitlines():
        parts = line.split()
        games.append(Game(hand=hand_cls(parts[0]), bid=int(parts[1])))
    return games


def solve(input: str, hand_cls: Callable[[str], BaseHand]) -> int:
    games = parse_input(input, hand_cls)
    games.sort(key=lambda game: game.hand)
    ans = sum([((i + 1) * games[i].bid) for i in range(len(games))])
    return ans


def part1(input: str) -> int:
    return solve(input, Hand)


def part2(input: str) -> int:
    return solve(input, JokerHand)


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
        (part1, "sample.txt", 6440),
        (part1, "input.txt", 248836197),
        (part2, "sample.txt", 5905),
        (part2, "input.txt", 251195607),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

from __future__ import annotations

import argparse
import operator
import os
import typing
from collections import deque
from collections.abc import Callable
from typing import NamedTuple

import pytest

from aoclib.int_range import IntRange
from aoclib.util import read_file

Part = dict[str, int]


class Cond(NamedTuple):
    att: str
    op: str
    rhs: int

    def __str__(self) -> str:
        return f"{self.att}{self.op}{self.rhs}"


class Rule(NamedTuple):
    cond: Cond | None
    dest: str

    @property
    def eval(self) -> Callable[[Part], bool]:
        if self.cond is None:
            return lambda _: True
        att, op_s, rhs = self.cond
        op = {
            "<": operator.lt,
            ">": operator.gt,
        }[op_s]
        return lambda part: op(part[att], int(rhs))


class Workflow(NamedTuple):
    name: str
    rules: list[Rule]


RangesState = dict[str, IntRange]


class State(NamedTuple):
    ranges_state: RangesState
    workflow: str
    rule_id: int


def parse_rule(rule_input: str) -> Rule:
    if ":" in rule_input:
        cond_s, dest = rule_input.split(":")
        for op_s in ["<", ">"]:
            lhs, _, rhs = cond_s.partition(op_s)
            if op_s != "" and rhs != "":
                return Rule(
                    cond=Cond(att=lhs, op=op_s, rhs=int(rhs)),
                    dest=dest,
                )
        assert False

    return Rule(
        cond=None,
        dest=rule_input,
    )


def parse_workflow_input(workflow_input: str) -> Workflow:
    name, rem = workflow_input.split("{")  # }
    rem = rem[:-1]
    rules = list(map(parse_rule, rem.split(",")))
    return Workflow(name=name, rules=rules)


def parse_part(part_input: str) -> Part:
    s = part_input[1:-1]
    att_strs = s.split(",")
    res = {}
    for att_str in att_strs:
        att, _, rhs = att_str.partition("=")
        res[att] = int(rhs)
    return typing.cast(Part, res)


def part1(input: str) -> int:
    workflows_input, parts_input = input.split("\n\n")
    workflows: list[Workflow] = list(
        map(parse_workflow_input, workflows_input.splitlines())
    )
    ws = {w.name: w for w in workflows}
    parts = list(map(parse_part, parts_input.splitlines()))

    ans = 0

    for part in parts:
        cur = "in"
        while cur not in ["R", "A"]:
            w = ws[cur]
            for rule in w.rules:
                if rule.eval(part):
                    cur = rule.dest
                    break
        if cur == "A":
            ans += sum(part.values())

    return ans


def eval_ranges(
    r: IntRange,
    cond: Cond,
) -> tuple[IntRange, IntRange]:
    if cond.op == ">":
        if r.low <= cond.rhs + 1 <= r.high:
            take = IntRange(low=cond.rhs + 1, high=r.high)
            leave = IntRange(low=r.low, high=cond.rhs)
            return take, leave
        elif cond.rhs + 1 > r.high:
            take = IntRange.from_len(low=0, len=0)
            leave = r
            return take, leave
    else:  # "<"
        if r.low <= cond.rhs - 1 <= r.high:
            take = IntRange(low=r.low, high=cond.rhs - 1)
            leave = IntRange(low=cond.rhs, high=r.high)
            return take, leave
        elif cond.rhs - 1 < r.low:
            take = IntRange.from_len(low=0, len=0)
            leave = r
            return take, leave

    return r, IntRange.from_len(low=0, len=0)


def part2(input: str) -> int:
    workflows_input, _ = input.split("\n\n")
    workflows: list[Workflow] = list(
        map(parse_workflow_input, workflows_input.splitlines())
    )
    ws = {w.name: w for w in workflows}

    s = State(
        ranges_state={c: IntRange(low=1, high=4000) for c in "xmas"},
        workflow="in",
        rule_id=0,
    )
    q: deque[State] = deque([s])

    # Note that in the end, all ranges states are disjoint.
    # Therefore, we do not need to care about overlapping results.
    final_ranges_state: list[RangesState] = []

    while len(q) > 0:
        u = q.popleft()

        if u.workflow == "R":
            continue
        if u.workflow == "A":
            final_ranges_state.append(u.ranges_state)
            continue

        workflow = ws[u.workflow]
        rule = workflow.rules[u.rule_id]

        cond = rule.cond

        if cond is None:
            v = State(
                ranges_state=dict(u.ranges_state),
                workflow=rule.dest,
                rule_id=0,
            )
            q.append(v)
        else:
            take_state = {}
            leave_state = {}

            for c in "xmas":
                if cond.att == c:
                    take, leave = eval_ranges(u.ranges_state[c], cond)
                    take_state[c] = take
                    leave_state[c] = leave
                else:
                    take_state[c] = u.ranges_state[c]
                    leave_state[c] = u.ranges_state[c]

            v_take = State(
                ranges_state=take_state,
                workflow=rule.dest,
                rule_id=0,
            )
            v_leave = State(
                ranges_state=leave_state,
                workflow=workflow.name,
                rule_id=u.rule_id + 1,
            )

            q.append(v_take)
            q.append(v_leave)

    ans = 0

    for ranges_state in final_ranges_state:
        cur = 1
        for c in "xmas":
            if c not in ranges_state:
                cur = 0
                break
            else:
                cur *= ranges_state[c].len
        ans += cur

    return ans


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2", "d"])
    parser.add_argument("input_file")

    try:
        args = parser.parse_args()
    except SystemExit:
        return 1

    input = read_file(args.input_file)

    if args.part == "1":
        print(f"Part 1: {part1(input)}")
    elif args.part == "d":
        print(f"{part2(input)}")
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "sample.txt", 19114),
        (part1, "input.txt", 449531),
        (part2, "sample.txt", 167409079868000),
        (part2, "input.txt", 122756210763577),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

from __future__ import annotations

import argparse
import os
from collections.abc import Callable
from functools import partial

import pytest
import z3

from aoclib.geometry.line import Line, RLine
from aoclib.geometry.point import Point, RPoint
from aoclib.geometry.rational import Rational
from aoclib.util import read_file

Coor3D = tuple[int, int, int]


def parse_triple(s: str) -> Coor3D:
    ints = list(map(int, s.split(",")))
    return ints[0], ints[1], ints[2]


def parse_line(line: str) -> tuple[Coor3D, Coor3D]:
    parts = line.split("@")
    return parse_triple(parts[0]), parse_triple(parts[1])


def part1(
    input: str,
    minc: int = 2 * 10**14,
    maxc: int = 4 * 10**14,
) -> int:
    min_x = min_y = minc
    max_x = max_y = maxc

    us = []
    vs = []
    for line in input.splitlines():
        ui, vi = parse_line(line)
        us.append(Point(ui[0], ui[1]))
        vs.append(Point(vi[0], vi[1]))

    lines: list[Line[int]] = []

    for i in range(len(us)):
        lines.append(Line.from_direction_and_point(v=vs[i], p=us[i]))

    ans = 0

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            li = lines[i]
            lj = lines[j]
            t = li.intersect(lj)
            if t is None:
                # print(f"{li} does not intersect with {lj}")
                pass
            else:
                # print(f"{li} intersects with {lj} at {t}")
                if min_x <= t.x <= max_x and min_y <= t.y <= max_y:
                    uit = t - us[i]
                    ujt = t - us[j]
                    # given two parallel vectors (i.e. cross product should be ~0)
                    # dot product > 0 means
                    # the two parallel vectors have the same direction
                    if uit.dot(vs[i]) > 0 and ujt.dot(vs[j]) > 0:
                        ans += 1

    return ans


def part1_rational(
    input: str,
    minc: int = 2 * 10**14,
    maxc: int = 4 * 10**14,
) -> int:
    min_x = min_y = minc
    max_x = max_y = maxc

    us = []
    vs = []
    for line in input.splitlines():
        ui, vi = parse_line(line)
        us.append(RPoint(x=Rational.from_int(ui[0]), y=Rational.from_int(ui[1])))
        vs.append(RPoint(x=Rational.from_int(vi[0]), y=Rational.from_int(vi[1])))

    lines: list[RLine] = []

    for i in range(len(us)):
        lines.append(RLine.from_direction_and_point(v=vs[i], p=us[i]))

    ans = 0

    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            li = lines[i]
            lj = lines[j]
            t = li.intersect(lj)
            if t is None:
                # print(f"{li} does not intersect with {lj}")
                pass
            else:
                # print(f"{li} intersects with {lj} at {t}")
                if min_x <= t.x <= max_x and min_y <= t.y <= max_y:
                    uit = t - us[i]
                    ujt = t - us[j]
                    # given two parallel vectors (i.e. cross product should be ~0)
                    assert uit.cross(vs[i]) == 0
                    assert ujt.cross(vs[j]) == 0
                    # dot product > 0 means
                    # the two parallel vectors have the same direction
                    if uit.dot(vs[i]) > 0 and ujt.dot(vs[j]) > 0:
                        ans += 1

    return ans


def part2(input: str) -> int:
    z3.set_option(verbose=10)
    us = []
    vs = []
    for line in input.splitlines():
        ui, vi = parse_line(line)
        us.append(ui)
        vs.append(vi)

    n = len(us)

    # We start at u' with velocity v'.
    # We need to satisfy:
    # u' + v'.ti = ui + vi.ti for all i
    solver = z3.Solver()

    # Note: For whatever reason, using z3.Int did not really work (super slow).
    # z3.Real did the trick.
    x_p = z3.Real("x_p")
    vx_p = z3.Real("vx_p")
    y_p = z3.Real("y_p")
    vy_p = z3.Real("vy_p")
    z_p = z3.Real("z_p")
    vz_p = z3.Real("vz_p")
    t = [z3.Real(f"t_{i}") for i in range(n)]

    for i in range(n):
        x_i = us[i][0]
        vx_i = vs[i][0]
        y_i = us[i][1]
        vy_i = vs[i][1]
        z_i = us[i][2]
        vz_i = vs[i][2]

        solver.add(x_p - x_i + (vx_p - vx_i) * t[i] == 0)
        solver.add(y_p - y_i + (vy_p - vy_i) * t[i] == 0)
        solver.add(z_p - z_i + (vz_p - vz_i) * t[i] == 0)
        solver.add(t[i] >= 0)

    assert solver.check() == z3.CheckSatResult(z3.Z3_L_TRUE)
    model = solver.model()
    q = [x_p, y_p, z_p]
    return sum([model[_].as_long() for _ in q])  # type: ignore


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("part", choices=["1", "2"])
    parser.add_argument("input_file")

    args = parser.parse_args()
    input = read_file(args.input_file)

    if args.part == "1":
        print(f"Part 1: {part1_rational(input)}")
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (partial(part1, minc=7, maxc=27), "sample.txt", 2),
        (partial(part1_rational, minc=7, maxc=27), "sample.txt", 2),
        (part1, "input.txt", 16779),
        (part1_rational, "input.txt", 16779),
        (part2, "sample.txt", 47),
        (part2, "input.txt", 871983857253169),
    ],
)
def test(
    solver: Callable[[str], int],
    file: str,
    ans: int,
) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

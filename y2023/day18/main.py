from __future__ import annotations

import argparse
import os
from collections import deque
from collections.abc import Callable, Sequence
from functools import partial
from typing import NamedTuple

import pytest

from aoclib.geometry.point import Point
from aoclib.grid2d import Di4, Pos
from aoclib.util import read_file


class Step(NamedTuple):
    di: Di4
    len: int

    @property
    def v(self):
        return {
            Di4.R: Point(self.len, 0),
            Di4.D: Point(0, -self.len),
            Di4.L: Point(-self.len, 0),
            Di4.U: Point(0, self.len),
        }[self.di]


def get_grid_size(steps: Sequence[Step]) -> tuple[int, int, int, int]:
    min_r = 0
    min_c = 0
    max_r = 0
    max_c = 0

    r = 0
    c = 0

    for step in steps:
        if step.di == Di4.U:
            r -= step.len
        elif step.di == Di4.D:
            r += step.len
        elif step.di == Di4.L:
            c -= step.len
        else:
            c += step.len
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)

    return min_r, min_c, max_r, max_c


def solve(
    input: str,
    parse_step_fn: Callable[[str], Step],
    solve_fn: Callable[[Sequence[Step]], int],
) -> int:
    steps = [parse_step_fn(line) for line in input.splitlines()]
    return solve_fn(steps)


def part1_parse_step(line: str) -> Step:
    parts = line.split(" ")
    di = {
        "U": Di4.U,
        "D": Di4.D,
        "L": Di4.L,
        "R": Di4.R,
    }[parts[0]]
    k = int(parts[1])
    return Step(di, k)


def part1_solve(steps: Sequence[Step]) -> int:
    min_r, min_c, max_r, max_c = get_grid_size(steps)

    n = max_r - min_r + 3
    m = max_c - min_c + 3

    assert min_r <= 0 and min_c <= 0
    origin = Pos(abs(min_r) + 1, abs(min_c) + 1)
    cur = Pos(origin.r, origin.c)

    g = [["." for c in range(m)] for r in range(n)]
    g[cur.r][cur.c] = "#"
    for step in steps:
        d = step.di
        for _ in range(step.len):
            cur = cur.go(d)
            g[cur.r][cur.c] = "#"

    # Get origin
    maybe_starts = []
    start_step_dirs: list[tuple[int, int]] = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    for step_dir in start_step_dirs:
        ss = Pos(origin.r + step_dir[0], origin.c + step_dir[1])
        if g[ss.r][ss.c] == ".":
            maybe_starts.append(ss)

    # Flood-fill
    for ch in ["x", "o"]:
        s = next(ss for ss in maybe_starts if g[ss.r][ss.c] == ".")
        q: deque[Pos] = deque([s])
        g[s.r][s.c] = ch

        while len(q) > 0:
            u = q.popleft()
            for d in Di4:
                v = u.go(d)
                if v.inside(g) and g[v.r][v.c] == ".":
                    g[v.r][v.c] = ch
                    q.append(v)

    if g[0][0] == "x":
        ch_in, ch_out = "o", "x"
    else:
        ch_in, ch_out = "x", "o"

    for r in range(n):
        for c in range(m):
            if g[r][c] == ch_in:
                g[r][c] = "#"
            elif g[r][c] == ch_out:
                g[r][c] = "."

    ans = 0

    for r in range(n):
        for c in range(m):
            if g[r][c] == "#":
                ans += 1

    return ans


def part1(input: str) -> int:
    return solve(input, part1_parse_step, part1_solve)


def part2_parse_step(line: str) -> Step:
    parts = line.split(" ")
    s = parts[2][2:-1]
    assert len(s) == 6
    dist = int(s[:-1], 16)
    di_map = {
        "0": Di4.R,
        "1": Di4.D,
        "2": Di4.L,
        "3": Di4.U,
    }
    di = di_map[s[-1]]
    return Step(len=dist, di=di)


def part2_solve(steps: Sequence[Step]) -> int:
    # Create a polygon where each vertex is the center of each boundary grid cell,
    # then calculate its area.
    # We also need to add the area in boundary grid cells not bounded
    # by the polygon.
    # This remaning area includes:
    # - Area in the corner grid cells.
    # - Area not in the corner grid cells. Let's call these cells the "side cells"
    # Area in the corner grid cells can be calculated as the sum of:
    #   1 (area of the whole grid) * ex_angle[i] (in radian) / 360 (degree)
    #   where ex_angle[i] is the exterior angle at the polygon vertex
    #   in corner cell i.
    # Remember that: The sum of interior angles of a polygon is
    #   180 (degree) * (n - 2)
    # where n is the number of angles/sides.
    # The area outside of the polygon can be calculated by the exterior angles.
    #   n - (180 * (n - 2) / 360)
    # = n - ((n - 2) / 2)

    origin = Point(0, 0)
    polygon = [origin]
    sides = 0

    for step in steps:
        p = polygon[-1] + step.v
        polygon.append(p)
        sides += step.len - 1
    assert polygon[0] == polygon[-1]
    polygon.pop()  # We always go back to the origin at the end.

    # Standard way to calculate area of a polygon.
    # Test problem: https://cses.fi/problemset/task/2191.
    area = 0
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        area += p1.cross(p2)
    polygon_area = abs(area) // 2

    corners = len(steps)
    corner_area = corners - ((corners - 2) // 2)

    side_area = sides // 2

    ans = polygon_area + corner_area + side_area
    return ans


def part2(input: str) -> int:
    return solve(input, part2_parse_step, part2_solve)


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
        print(f"Part 1 sol: {solve(input, part1_parse_step, part1_solve)}")
        print(f"Part 2 sol: {solve(input, part1_parse_step, part2_solve)}")
    else:
        print(f"Part 2: {part2(input)}")


@pytest.mark.parametrize(
    ("solver", "file", "ans"),
    [
        (part1, "sample.txt", 62),
        (part1, "input.txt", 36807),
        # Solve part 1 with part 2's logic.
        (
            partial(solve, parse_step_fn=part1_parse_step, solve_fn=part2_solve),
            "sample.txt",
            62,
        ),
        (
            partial(solve, parse_step_fn=part1_parse_step, solve_fn=part2_solve),
            "input.txt",
            36807,
        ),
        (part2, "sample.txt", 952408144115),
        (part2, "input.txt", 48797603984357),
    ],
)
def test(solver: Callable[[str], int], file: str, ans: int) -> None:
    filepath = os.path.join(os.path.dirname(__file__), file)
    assert solver(read_file(filepath)) == ans


if __name__ == "__main__":
    SystemExit(main())

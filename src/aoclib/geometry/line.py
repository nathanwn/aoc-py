from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Generic, TypeVar

from aoclib.geometry.point import Point

T = TypeVar("T", int, float, Fraction)


@dataclass
class Line(Generic[T]):
    """
    Attributes
    ----------
    v : Point
        The direction vector.
    c : Point
        The offset.
    """

    v: Point
    c: T

    @classmethod
    def from_two_points(cls, q: Point, p: Point) -> Line:
        return cls.from_direction_and_point(v=q - p, p=p)

    @classmethod
    def from_direction_and_point(cls, v: Point, p: Point) -> Line:
        c = v.cross(p)
        return Line(v=v, c=c)

    def intersect(self, other: Line) -> Point | None:
        d = self.v.cross(other.v)
        if d == 0:
            return None
        return (other.v * self.c - self.v * other.c) / d

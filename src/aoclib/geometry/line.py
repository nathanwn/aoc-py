from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from aoclib.geometry.point import Point, RPoint
from aoclib.geometry.rational import Rational

T = TypeVar("T", int, float)


@dataclass
class Line(Generic[T]):
    """
    Attributes
    ----------
    v : Point[T]
        The direction vector.
    c : Point[T]
        The offset.
    """

    v: Point[T]
    c: T

    @classmethod
    def from_two_points(cls, q: Point[T], p: Point[T]) -> Line[T]:
        return cls.from_direction_and_point(v=q - p, p=p)

    @classmethod
    def from_direction_and_point(cls, v: Point[T], p: Point[T]) -> Line[T]:
        c = v.cross(p)
        return Line(v=v, c=c)

    def intersect(self, other: Line[T]) -> Point[float] | None:
        d = self.v.cross(other.v)
        if d == 0:
            return None
        return (other.v * self.c - self.v * other.c) / d


@dataclass
class RLine:
    v: RPoint
    c: Rational

    @classmethod
    def from_two_points(cls, q: RPoint, p: RPoint) -> RLine:
        return cls.from_direction_and_point(v=q - p, p=p)

    @classmethod
    def from_direction_and_point(cls, v: RPoint, p: RPoint) -> RLine:
        c = v.cross(p)
        return RLine(v=v, c=c)

    def intersect(self, other: RLine) -> RPoint | None:
        d = self.v.cross(other.v)
        if d == 0:
            return None
        return (other.v * self.c - self.v * other.c) / d

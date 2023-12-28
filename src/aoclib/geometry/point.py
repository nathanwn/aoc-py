from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Generic, TypeVar

from aoclib.geometry.rational import Rational

T = TypeVar("T", int, float, Fraction)


@dataclass
class Point(Generic[T]):
    x: T
    y: T

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, k) -> Point:
        return Point(self.x * k, self.y * k)

    def __truediv__(self, k) -> Point:
        return Point(self.x / k, self.y / k)

    def dot(self, other: Point) -> T:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Point) -> T:
        return self.x * other.y - self.y * other.x

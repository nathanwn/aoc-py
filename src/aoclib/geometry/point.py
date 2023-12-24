from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from aoclib.geometry.rational import Rational

T = TypeVar("T", int, float)


@dataclass
class Point(Generic[T]):
    x: T
    y: T

    def __add__(self, other: Point[T]) -> Point[T]:
        return Point(self.x - other.x, self.y - other.y)

    def __sub__(self, other: Point[T]) -> Point[T]:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, k: int | float) -> Point:
        return Point(self.x * k, self.y * k)

    def __truediv__(self, k: int | float) -> Point:
        return Point(self.x / k, self.y / k)

    def dot(self, other: Point[T]) -> T:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Point[T]) -> T:
        return self.x * other.y - self.y * other.x


@dataclass
class RPoint:
    x: Rational
    y: Rational

    def __add__(self, other: RPoint) -> RPoint:
        return RPoint(self.x - other.x, self.y - other.y)

    def __sub__(self, other: RPoint) -> RPoint:
        return RPoint(self.x - other.x, self.y - other.y)

    def __mul__(self, k: Rational) -> RPoint:
        return RPoint(self.x * k, self.y * k)

    def __truediv__(self, k: Rational) -> RPoint:
        return RPoint(self.x / k, self.y / k)

    def dot(self, other: RPoint) -> Rational:
        return self.x * other.x + self.y * other.y

    def cross(self, other: RPoint) -> Rational:
        return self.x * other.y - self.y * other.x

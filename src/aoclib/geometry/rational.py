from __future__ import annotations

from dataclasses import dataclass
from math import gcd, lcm


@dataclass
class Rational:
    num: int
    den: int

    def normalize(self) -> Rational:
        g = gcd(self.num, self.den)
        self.num //= g
        self.den //= g
        return self

    @classmethod
    def from_int(cls, v: int) -> Rational:
        return Rational(num=v, den=1)

    def __add__(self, other: object) -> Rational:
        if isinstance(other, int):
            return self + Rational(num=other, den=1)
        elif isinstance(other, Rational):
            den = lcm(self.den, other.den)
            num = den // self.den * self.num + den // other.den * other.num
            return Rational(num=num, den=den).normalize()
        else:
            raise TypeError(f"Cannot add a Rational with a {other.__class__}")

    def __sub__(self, other: object) -> Rational:
        if isinstance(other, int):
            return self - Rational(num=other, den=1)
        elif isinstance(other, Rational):
            den = lcm(self.den, other.den)
            num = den // self.den * self.num - den // other.den * other.num
            return Rational(num=num, den=den).normalize()
        else:
            raise TypeError(f"Cannot subtract a Rational with a {other.__class__}")

    def __mul__(self, other: object) -> Rational:
        if isinstance(other, int):
            return self * Rational(num=other, den=1)
        elif isinstance(other, Rational):
            return Rational(
                num=self.num * other.num, den=self.den * other.den
            ).normalize()
        else:
            raise TypeError(f"Cannot multiply a Rational with a {other.__class__}")

    def __truediv__(self, other: object) -> Rational:
        if isinstance(other, int):
            return self * Rational(num=1, den=other)
        elif isinstance(other, Rational):
            return self * other.inverse()
        else:
            raise TypeError(f"Cannot divide a Rational with a {other.__class__}")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self == Rational(num=other, den=1)
        elif isinstance(other, Rational):
            x = self.normalize()
            y = other.normalize()
            return x.num == y.num and x.den == y.den
        else:
            raise TypeError(f"Cannot compare a Rational with a {other.__class__}")

    def __lt__(self, other: object) -> bool:
        if isinstance(other, int):
            return self < Rational(num=other, den=1)
        elif isinstance(other, Rational):
            den = lcm(self.den, other.den)
            self_num = den // self.den * self.num
            other_num = den // other.den * other.num
            return self_num < other_num
        else:
            raise TypeError(f"Cannot compare a Rational with a {other.__class__}")

    def __le__(self, other: object) -> bool:
        return self < other or self == other

    def __gt__(self, other: object) -> bool:
        if isinstance(other, int):
            return self > Rational(num=other, den=1)
        elif isinstance(other, Rational):
            return other < self
        else:
            raise TypeError(f"Cannot compare a Rational with a {other.__class__}")

    def __ge__(self, other: object) -> bool:
        return self > other or self == other

    def inverse(self) -> Rational:
        return Rational(num=self.den, den=self.num)

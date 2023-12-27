from __future__ import annotations

from typing import NamedTuple


class IntRange(NamedTuple):
    low: int
    high: int

    @classmethod
    def from_len(cls, low: int, len: int) -> IntRange:
        return cls(low=low, high=low + len - 1)

    @property
    def len(self) -> int:
        return self.high - self.low + 1

    def contains(self, val: int) -> bool:
        return self.low <= val <= self.high

    def join(self, them: IntRange) -> IntRange | None:
        if them.high < self.low or self.high < them.low:
            return None
        new_low = max(self.low, them.low)
        new_high = min(self.high, them.high)
        return IntRange(new_low, new_high)

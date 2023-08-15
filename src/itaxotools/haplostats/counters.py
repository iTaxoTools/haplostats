from __future__ import annotations

from collections import Counter
from itertools import combinations


class TagCounters:
    """Count members for many tags"""

    def __init__(self):
        self._counters: dict[str, Counter[int]] = {}

    def add(self, tag: str, member: int) -> None:
        if tag not in self._counters:
            self._counters[tag] = Counter()
        self._counters[tag][member] += 1

    def update(self, tag: str, members: iter[int]) -> None:
        if tag not in self._counters:
            self._counters[tag] = Counter()
        self._counters[tag].update(members)

    def all(self) -> iter[tuple[str, Counter]]:
        for tag in self._counters:
            yield tag, self._counters[tag]

    def all_pairs(self) -> iter[tuple[str, str, Counter]]:
        tags = self._counters.keys()
        for x, y in combinations(tags, 2):
            counter = self._counters[x] & self._counters[y]
            yield x, y, counter

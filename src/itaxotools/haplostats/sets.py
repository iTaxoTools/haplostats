from __future__ import annotations

from collections import Counter
from itertools import combinations


class TaggedDisjointSets:
    """Disjoint-set data structure (Union-Find) with tag counters"""

    def __init__(self, n: int = 0):
        self._parents: list[int] = list(range(n))
        self._ranks: list[int] = [0] * n

        self._counters: list[Counter[str]] = [Counter() for _ in range(n)]

    def _extend(self, x: int) -> None:
        diff = x - len(self._parents)
        if diff < 0:
            return

        self._parents.extend(range(len(self._parents), x + 1))
        self._ranks.extend([0] * (diff + 1))
        self._counters.extend((Counter() for _ in range(diff + 1)))

    def _find(self, x: int) -> None:
        if self._parents[x] != x:
            self._parents[x] = self._find(self._parents[x])
        return self._parents[x]

    def _union(self, x: int, y: int) -> None:
        if x == y:
            return

        x = self._find(x)
        y = self._find(y)

        if x == y:
            return

        if self._ranks[x] < self._ranks[y]:
            x, y = y, x

        self._parents[y] = x

        if self._ranks[x] == self._ranks[y]:
            self._ranks[x] += 1

    def add(self, tag: str, members: iter[int]):
        members = list(members)
        if not len(members):
            raise ValueError("Tag must contain at least one member")

        target = members[0]

        for m in members:
            self._extend(m)
            self._counters[m][tag] += 1
            self._union(m, target)

    def get_set_members(self) -> list[list[int]]:
        sets: dict[int, list[int]] = {}
        for i in range(len(self._parents)):
            root = self._find(i)
            if root not in sets:
                sets[root] = []
            sets[root].append(i)
        return list(sets.values())

    def get_tags_for_members(self, members: iter[int]) -> Counter[str]:
        counter = Counter()
        for member in members:
            counter.update(self._counters[member])
        return counter

    def get_tags_per_set(self) -> dict[int, Counter[str]]:
        return {
            set: self.get_tags_for_members(members)
            for set, members in enumerate(self.get_set_members())
        }

    def get_sets_per_tag(self, tags_per_set=None) -> dict[str, Counter[int]]:
        tags_per_set = tags_per_set or self.get_tags_per_set()
        tag_counters: dict[str, Counter[int]] = {}
        for set, tags in tags_per_set.items():
            for tag, count in tags.items():
                if tag not in tag_counters:
                    tag_counters[tag] = Counter()
                tag_counters[tag][set] = count
        return tag_counters

    def get_sets_per_tag_pair(
        self, sets_per_tag=None, set_members=None
    ) -> iter[tuple[str, str, Counter[int]]]:
        sets_per_tag = sets_per_tag or self.get_sets_per_tag()
        set_members = set_members or self.get_set_members()
        for x, y in combinations(sets_per_tag.keys(), 2):
            counter = sets_per_tag[x] & sets_per_tag[y]
            for set in counter:
                common_members = 0
                for member in set_members[set]:
                    member_tags = self._counters[member]
                    if x in member_tags and y in member_tags:
                        common_members += 1
                counter[set] = common_members
            yield x, y, counter

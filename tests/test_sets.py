from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from itaxotools.haplostats.sets import TaggedDisjointSets

Input = list[tuple[str, list[int]]]
TagsPerSet = dict[int, Counter[str]]
SetsPerTag = dict[str, Counter[int]]


@dataclass
class SetTest:
    n: int
    input: Input
    tags_per_set: TagsPerSet
    sets_per_tag: SetsPerTag

    def validate(self):
        tdsets = TaggedDisjointSets(self.n)
        for tag, members in self.input:
            tdsets.add(tag, members)
        tags_per_set = tdsets.get_tags_per_set()
        sets_per_tag = tdsets.get_sets_per_tag()

        assert tags_per_set == self.tags_per_set
        assert sets_per_tag == self.sets_per_tag


def test_empty():
    SetTest(
        n = 4,
        input = [],
        tags_per_set = {
            0: Counter(),
            1: Counter(),
            2: Counter(),
            3: Counter(),
        },
        sets_per_tag = {},
    ).validate()


def test_disjoint():
    SetTest(
        n = 4,
        input = [
            ('A', [0, 1]),
            ('B', [2, 3]),
        ],
        tags_per_set = {
            0: Counter({'A': 2}),
            1: Counter({'B': 2}),
        },
        sets_per_tag = {
            'A': Counter({0: 2}),
            'B': Counter({1: 2}),
        },
    ).validate()


def test_overlap():
    SetTest(
        n = 4,
        input = [
            ('A', [0, 1, 2, 3]),
            ('B', [0, 1, 2, 3]),
        ],
        tags_per_set = {
            0: Counter({'A': 4, 'B': 4}),
        },
        sets_per_tag = {
            'A': Counter({0: 4}),
            'B': Counter({0: 4}),
        },
    ).validate()


def test_repeated():
    SetTest(
        n = 4,
        input = [
            ('A', [0]),
            ('A', [0]),
            ('A', [0]),
            ('A', [0]),
            ('B', [1, 2, 3]),
        ],
        tags_per_set = {
            0: Counter({'A': 4}),
            1: Counter({'B': 3}),
        },
        sets_per_tag = {
            'A': Counter({0: 4}),
            'B': Counter({1: 3}),
        },
    ).validate()


def test_chained():
    SetTest(
        n = 4,
        input = [
            ('A', [0, 1]),
            ('B', [1, 2]),
            ('C', [2, 3]),
        ],
        tags_per_set = {
            0: Counter({'A': 2, 'B': 2, 'C': 2}),
        },
        sets_per_tag = {
            'A': Counter({0: 2}),
            'B': Counter({0: 2}),
            'C': Counter({0: 2}),
        },
    ).validate()


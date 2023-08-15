from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from itaxotools.haplostats.counters import TagCounters

Input = list[tuple[str, list[int]]]
TagList = list[tuple[str, Counter[int]]]
PairList = list[tuple[str, str, Counter[int]]]


@dataclass
class CounterTest:
    input: Input
    tag_list: TagList
    pair_list: PairList

    def validate(self):
        counters = TagCounters()
        for tag, members in self.input:
            if len(members) == 1:
                counters.add(tag, members[0])
            else:
                counters.update(tag, members)
        tag_list = list(counters.all())
        pair_list = list(counters.all_pairs())

        assert tag_list == self.tag_list
        assert pair_list == self.pair_list


def test_empty():
    CounterTest(
        input = [],
        tag_list = [],
        pair_list = [],
    ).validate()


def test_add_single():
    CounterTest(
        input = [
            ('A', [0]),
        ],
        tag_list = [
            ('A', Counter({0: 1})),
        ],
        pair_list = [],
    ).validate()


def test_add_many():
    CounterTest(
        input = [
            ('A', [0]),
            ('B', [1]),
            ('C', [2]),
        ],
        tag_list = [
            ('A', Counter({0: 1})),
            ('B', Counter({1: 1})),
            ('C', Counter({2: 1})),
        ],
        pair_list = [
            ('A', 'B', Counter()),
            ('A', 'C', Counter()),
            ('B', 'C', Counter()),
        ],
    ).validate()


def test_update_single():
    CounterTest(
        input = [
            ('A', [0, 1, 2]),
        ],
        tag_list = [
            ('A', Counter({0: 1, 1: 1, 2: 1})),
        ],
        pair_list = [],
    ).validate()


def test_update_single_repeated():
    CounterTest(
        input = [
            ('A', [0, 0, 1]),
        ],
        tag_list = [
            ('A', Counter({0: 2, 1: 1})),
        ],
        pair_list = [],
    ).validate()


def test_update_many_couples():
    CounterTest(
        input = [
            ('A', [0, 1]),
            ('B', [1, 2]),
            ('C', [3, 4]),
        ],
        tag_list = [
            ('A', Counter({0: 1, 1: 1})),
            ('B', Counter({1: 1, 2: 1})),
            ('C', Counter({3: 1, 4: 1})),
        ],
        pair_list = [
            ('A', 'B', Counter({1: 1})),
            ('A', 'C', Counter()),
            ('B', 'C', Counter()),
        ],
    ).validate()

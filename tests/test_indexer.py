from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from itaxotools.haplostats.indexer import StringIndexer

Input = list[tuple[str, int]]
ReturnList = list[int]
IndexList = list[tuple[int, str]]


@dataclass
class IndexerTest:
    input: Input
    index_list: IndexList
    length: int

    def validate(self):
        indexer = StringIndexer()
        for string, id in self.input:
            v = indexer.add(string)
            assert v == id
        index_list = list(indexer.all())

        assert index_list == self.index_list
        assert len(indexer) == self.length


def test_empty():
    IndexerTest(
        input = [],
        index_list = [],
        length = 0,
    ).validate()


def test_single():
    IndexerTest(
        input = [
            ('A', 0),
        ],
        index_list = [
            (0, 'A'),
        ],
        length = 1,
    ).validate()


def test_two():
    IndexerTest(
        input = [
            ('A', 0),
            ('B', 1),
        ],
        index_list = [
            (0, 'A'),
            (1, 'B'),
        ],
        length = 2,
    ).validate()


def test_repeated():
    IndexerTest(
        input = [
            ('A', 0),
            ('A', 0),
            ('A', 0),
            ('B', 1),
            ('A', 0),
        ],
        index_list = [
            (0, 'A'),
            (1, 'B'),
        ],
        length = 2,
    ).validate()

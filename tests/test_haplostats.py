from __future__ import annotations

import pytest

from itaxotools.haplostats import HaploStats


def test_empty():
    stats = HaploStats()
    assert stats.format_haplotype_id(0) == "Hap01"
    assert stats.format_set_id(0) == "FFR01"
    assert stats.get_haplotypes() == {}
    assert stats.get_haplotypes_per_subset() == {}
    assert stats.get_haplotypes_shared_between_subsets() == []
    assert stats.get_fields_for_recombination() == {}
    assert stats.get_subsets_per_field_for_recombination() == {}
    assert stats.get_fields_for_recombination_per_subset() == {}
    assert stats.get_fields_for_recombination_shared_between_subsets() == []
    assert stats.get_dataset_sizes() == dict(
        haplotypes=0,
        subsets=0,
        FFRs=0,
    )


@pytest.fixture
def stats_example():
    stats = HaploStats()
    stats.set_subset_labels(
        subset_a="species_a",
        subset_b="species_b",
        subsets="species",
    )
    stats.add("verrucosa", ["AAAAAAAAA", "AAAAAAAAC"])
    stats.add("verrucosa", ["AAAAAAAAC", "AAAAAAAAG"])
    stats.add("verrucosa", ["AAAAAAAAG", "AAAAAAAAA"])
    stats.add("mysteriosa", ["CCCCCCCCC", "CCCCCCCCC"])
    stats.add("mysteriosa", ["CCCCCCCCC", "CCCCCCCCT"])
    stats.add("enigmatica", ["GGGGGGGGG", "CCCCCCCCT"])
    stats.add("enigmatica", ["AAAAAAAAA", "AAAAAAAAA"])
    yield stats


def test_get_haplotypes(stats_example: HaploStats):
    assert stats_example.get_haplotypes() == {
        "Hap01": "AAAAAAAAA",
        "Hap02": "AAAAAAAAC",
        "Hap03": "AAAAAAAAG",
        "Hap04": "CCCCCCCCC",
        "Hap05": "CCCCCCCCT",
        "Hap06": "GGGGGGGGG",
    }


def test_get_haplotypes_per_subset(stats_example: HaploStats):
    assert stats_example.get_haplotypes_per_subset() == {
        "verrucosa": {
            "total": 6,
            "haplotypes": {
                "Hap01": 2,
                "Hap02": 2,
                "Hap03": 2,
            },
        },
        "mysteriosa": {
            "total": 4,
            "haplotypes": {
                "Hap04": 3,
                "Hap05": 1,
            },
        },
        "enigmatica": {
            "total": 4,
            "haplotypes": {
                "Hap01": 2,
                "Hap05": 1,
                "Hap06": 1,
            },
        },
    }


def test_get_haplotypes_shared_between_subsets(stats_example: HaploStats):
    assert stats_example.get_haplotypes_shared_between_subsets() == [
        {
            "species_a": "verrucosa",
            "species_b": "enigmatica",
            "common": {
                "Hap01": 2,
            },
        },
        {
            "species_a": "mysteriosa",
            "species_b": "enigmatica",
            "common": {
                "Hap05": 1,
            },
        },
    ]


def test_get_haplotypes_shared_between_subsets_including_empty(
    stats_example: HaploStats,
):
    assert stats_example.get_haplotypes_shared_between_subsets(include_empty=True) == [
        {
            "species_a": "verrucosa",
            "species_b": "mysteriosa",
            "common": {},
        },
        {
            "species_a": "verrucosa",
            "species_b": "enigmatica",
            "common": {
                "Hap01": 2,
            },
        },
        {
            "species_a": "mysteriosa",
            "species_b": "enigmatica",
            "common": {
                "Hap05": 1,
            },
        },
    ]


def test_get_fields_for_recombination(stats_example: HaploStats):
    assert stats_example.get_fields_for_recombination() == {
        "FFR01": [
            "Hap01",
            "Hap02",
            "Hap03",
        ],
        "FFR02": [
            "Hap04",
            "Hap05",
            "Hap06",
        ],
    }


def test_get_subsets_per_field_for_recombination(stats_example: HaploStats):
    assert stats_example.get_subsets_per_field_for_recombination() == {
        "FFR01": {
            "total": 8,
            "species": {
                "verrucosa": 6,
                "enigmatica": 2,
            },
        },
        "FFR02": {
            "total": 6,
            "species": {
                "mysteriosa": 4,
                "enigmatica": 2,
            },
        },
    }


def test_get_fields_for_recombination_per_subset(stats_example: HaploStats):
    assert stats_example.get_fields_for_recombination_per_subset() == {
        "verrucosa": {
            "total": 6,
            "FFRs": {
                "FFR01": 6,
            },
        },
        "mysteriosa": {
            "total": 4,
            "FFRs": {
                "FFR02": 4,
            },
        },
        "enigmatica": {
            "total": 4,
            "FFRs": {
                "FFR01": 2,
                "FFR02": 2,
            },
        },
    }


def test_get_fields_for_recombination_shared_between_subsets(stats_example: HaploStats):
    assert stats_example.get_fields_for_recombination_shared_between_subsets() == [
        {
            "species_a": "verrucosa",
            "species_b": "enigmatica",
            "common": {
                "FFR01": 1,
            },
        },
        {
            "species_a": "enigmatica",
            "species_b": "mysteriosa",
            "common": {
                "FFR02": 1,
            },
        },
    ]


def test_get_fields_for_recombination_shared_between_subsets_including_empty(
    stats_example: HaploStats,
):
    assert stats_example.get_fields_for_recombination_shared_between_subsets(
        include_empty=True
    ) == [
        {
            "species_a": "verrucosa",
            "species_b": "enigmatica",
            "common": {
                "FFR01": 1,
            },
        },
        {"species_a": "verrucosa", "species_b": "mysteriosa", "common": {}},
        {
            "species_a": "enigmatica",
            "species_b": "mysteriosa",
            "common": {
                "FFR02": 1,
            },
        },
    ]


def test_get_dataset_sizes(stats_example: HaploStats):
    assert stats_example.get_dataset_sizes() == {
        "haplotypes": 6,
        "species": 3,
        "FFRs": 2,
    }

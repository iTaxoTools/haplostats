#!/usr/bin/env python3

"""
Benchmark for random datasets with two alleles per specimen. Run with:
$ python benchmark.py <specimens> <subsets> <nucleotides>

Example run:
$ python benchmark.py 1000 500 6

"""

import random
import sys
from contextlib import contextmanager
from time import perf_counter

from itaxotools.haplostats import HaploStats


def random_input_generator(specimens: int = 4, subsets: int = 2, length: int = 2):
    alphabet = "ACGT"
    subsets -= 1

    def _get_specimen(x):
        return f"id_{x}"

    def _get_subset():
        return f"species_{random.randint(0, subsets)}"

    def _get_sequence():
        return "".join(random.choice(alphabet) for _ in range(length))

    for x in range(specimens):
        yield (_get_specimen(x), _get_subset(), _get_sequence(), _get_sequence())


def extract_input_data(raw_input):
    for _, species, seqa, seqb in raw_input:
        yield (species, [seqa, seqb])


@contextmanager
def timer(task: str):
    print(f"Computing: {task}")
    start_time = perf_counter()
    yield
    end_time = perf_counter()
    print(f"Elapsed time: {end_time - start_time:.4f} seconds")
    print()


@contextmanager
def total_timer():
    print()
    start_time = perf_counter()
    yield
    end_time = perf_counter()
    print(f"Total elapsed time: {end_time - start_time:.4f} seconds")
    print()


def main():
    if len(sys.argv) != 4:
        raise ValueError("Expected 3 arguments")

    raw_input = list(
        random_input_generator(
            specimens=int(sys.argv[1]),
            subsets=int(sys.argv[2]),
            length=int(sys.argv[3]),
        )
    )

    stats = HaploStats()

    with total_timer():
        with timer("Adding input"):
            for species, sequences in extract_input_data(raw_input):
                stats.add(species, sequences)

        with timer("Haplotype sequences"):
            stats.get_haplotypes()

        with timer("Haplotypes per species"):
            stats.get_haplotypes_per_subset()

        with timer("Haplotypes shared between species"):
            stats.get_haplotypes_shared_between_subsets()

        with timer("Fields of recombination"):
            stats.get_fields_of_recombination()

        with timer("Species count per FOR"):
            stats.get_subsets_per_field_of_recombination()

        with timer("FOR count per species"):
            stats.get_fields_of_recombination_per_subset()

        with timer("FORs shared between species"):
            stats.get_fields_of_recombination_shared_between_subsets()

        with timer("Dataset size"):
            sizes = stats.get_dataset_sizes()

    for k, v in sizes.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()

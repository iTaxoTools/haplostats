# Haplostats

[![PyPI - Version](https://img.shields.io/pypi/v/itaxotools-haplostats)](
    https://pypi.org/project/itaxotools-haplostats)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/itaxotools-haplostats)](
    https://pypi.org/project/itaxotools-haplostats)
[![GitHub - Tests](https://img.shields.io/github/actions/workflow/status/iTaxoTools/haplostats/test.yml?label=tests)](
    https://github.com/iTaxoTools/haplostats/actions/workflows/test.yml)

Find unique haplotypes, fields for recombination and subset sharing.

## Installation

Haplostats is available on PyPI. You can install it through `pip`:

```
pip install itaxotools-haplostats
```

## Usage

In Python, import and instantiate `HaploStats`:

```
from itaxotools.haplostats import HaploStats
stats = HaploStats()
```

Add your data one entry at a time. Each entry is represented by its subset tag, plus a list of associated sequences. These are usually different alleles of the same specimen:

```
# Two specimens of different species, with two alleles each.
# There are three haplotypes in total. There is a single field
# for recombination (FFR), as the specimens are connected through
# a common sequence: 'ACT'.

stats.add('mysteriosa', ['ACT', 'ACC'])
stats.add('enigmatica', ['ACT', 'ATT'])
```

After adding all entries, you are ready to analyze the dataset:

```
haplotypes = stats.get_haplotypes()
fors = stats.get_fields_for_recombination()

common_haplotypes = stats.get_haplotypes_shared_between_subsets()
common_fors = stats.get_fields_for_recombination_shared_between_subsets()
```

For a more detailed look at the available methods, please have a look at the [example script](https://github.com/iTaxoTools/haplostats/tree/main/scripts/example.py).

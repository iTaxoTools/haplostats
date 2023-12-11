# Haplostats - Find unique haplotypes, fields of recombination and subset sharing

Install using pip:

```
pip install git+https://github.com/iTaxoTools/haplostats.git
```

In Python, import and instantiate HaploStats:

```
from itaxotools.haplostats import HaploStats
stats = HaploStats()
```

Add your data one entry at a time. Each entry is represented by its subset tag, plus a list of associated sequences (eg. from different alleles of the same specimen):

```
# Two specimens of different species, with two alleles each.
# There are three haplotypes in total. There is a single field
# of recombination (FOR), as the specimens are connected through
# a common sequence: 'ACT'.

stats.add('mysteriosa', ['ACT', 'ACC'])
stats.add('enigmatica', ['ACT', 'ATT'])
```

After adding all entries, you are ready to analyze the dataset:

```
haplotypes = stats.get_haplotypes()
fors = stats.get_fields_of_recombination()

common_haplotypes = stats.get_haplotypes_shared_between_subsets()
common_fors = stats.get_fields_of_recombination_shared_between_subsets()
```

For a more detailed look at the available methods, please have a look at the [example script](scripts/example.py).

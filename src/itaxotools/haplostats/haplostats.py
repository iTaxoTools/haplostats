from itaxotools.haplostats.counters import TagCounters
from itaxotools.haplostats.indexer import StringIndexer
from itaxotools.haplostats.sets import TaggedDisjointSets


class HaploStats:
    """Get haplotype statistics from sequences"""

    def __init__(self):
        self.indexer = StringIndexer()
        self.counters = TagCounters()
        self.fors = TaggedDisjointSets()

        self.set_subset_labels()

    def set_subset_labels(
        self,
        subset_a = 'subset_a',
        subset_b = 'subset_b',
        subsets = 'subsets',
    ):
        self._subset_a = subset_a
        self._subset_b = subset_b
        self._subsets = subsets

    def add(self, subset: str, sequences: list[str]):
        ids = [self.indexer.add(sequence) for sequence in sequences]
        self.counters.update(subset, ids)
        self.fors.add(subset, ids)

    @property
    def haplotype_digits(self) -> int:
        return len(str(len(self.indexer))) + 1

    @property
    def set_digits(self) -> int:
        return len(str(len(self.fors.get_set_members()))) + 1

    def format_haplotype_id(self, id: int) -> str:
        return 'Hap' + str(id + 1).rjust(self.haplotype_digits, '0')

    def format_set_id(self, id: int) -> str:
        return 'FOR' + str(id + 1).rjust(self.set_digits, '0')

    def get_haplotypes(self) -> dict[str, str]:
        return {
            self.format_haplotype_id(id): seq
            for id, seq in self.indexer.all()
        }

    def get_haplotypes_per_subset(self) -> dict[str, dict]:
        return {
            tag: {
                'total': counter.total(),
                'haplotypes': {
                    self.format_haplotype_id(id): count
                    for id, count in counter.items()
                }
            }
            for tag, counter in self.counters.all()
        }

    def get_haplotypes_shared_between_subsets(self, include_empty=False) -> list[dict]:
        return [
            {
                self._subset_a: x,
                self._subset_b: y,
                'common': {
                    self.format_haplotype_id(id): count
                    for id, count in haplotypes.items()
                },
            }
            for x, y, haplotypes in self.counters.all_pairs()
            if haplotypes or include_empty
        ]

    def get_fields_of_recombination(self) -> dict[str, list[str]]:
        return {
            self.format_set_id(set): [
                self.format_haplotype_id(id)
                for id in haplotypes
            ]
            for set, haplotypes in enumerate(self.fors.get_set_members())
        }

    def get_subsets_per_field_of_recombination(self) -> dict[str, dict]:
        return {
            self.format_set_id(set): {
                'total': tags.total(),
                self._subsets: dict(tags)}
            for set, tags in self.fors.get_tags_per_set().items()
        }

    def get_fields_of_recombination_per_subset(self) -> dict[str, dict]:
        return {
            tag: {
                'total': sets.total(),
                'FORs': {
                    self.format_set_id(set): count
                    for set, count in sets.items()
                }
            }
            for tag, sets in self.fors.get_sets_per_tag().items()
        }

    def get_fields_of_recombination_shared_between_subsets(self, include_empty=False) -> list[dict]:
        return [
            {
                self._subset_a: x,
                self._subset_b: y,
                'common': {
                    self.format_set_id(set): count
                    for set, count in sets.items()
                },
            }
            for x, y, sets in self.fors.get_sets_per_tag_pair()
            if sets or include_empty
        ]

    def get_dataset_sizes(self) -> dict[str, int]:
        return {
            'haplotypes': len(self.indexer),
            'FORs': len(self.fors.get_set_members()),
            self._subsets: len(self.counters),
        }

import yaml

from itaxotools.haplostats.sets import TaggedDisjointSets
from itaxotools.haplostats.indexer import StringIndexer
from itaxotools.haplostats.counters import TagCounters


def dict_representer(dumper, data):
    return dumper.represent_mapping('tag:yaml.org,2002:map', data.items())


yaml.add_representer(dict, dict_representer)


def yamlify(data, title: str = None) -> str:
    if title:
        data = {title: data}
    return yaml.dump(data, default_flow_style=False)


def format_haplotype_id(id: int, digits: int = 0) -> str:
    return 'Hap' + str(id).rjust(digits, '0')


def format_set_id(id: int, digits: int = 0) -> str:
    return 'FOR' + str(id).rjust(digits, '0')


def _raw_input_generator_sample():
    yield ('specimen1', 'verrucosa',  'AAAAAAAAA', 'AAAAAAAAC')
    yield ('specimen2', 'verrucosa',  'AAAAAAAAC', 'AAAAAAAAG')
    yield ('specimen3', 'verrucosa',  'AAAAAAAAG', 'AAAAAAAAA')
    yield ('specimen4', 'mysteriosa', 'CCCCCCCCC', 'CCCCCCCCC')
    yield ('specimen5', 'mysteriosa', 'CCCCCCCCC', 'CCCCCCCCT')
    yield ('specimen6', 'enigmatica', 'GGGGGGGGG', 'CCCCCCCCT')


def input_generator_sample():
    for _, species, seqa, seqb in _raw_input_generator_sample():
        yield (species, [seqa, seqb])


print()

data = [
    dict(id = id,
        species = species,
        allele_a = seqa,
        allele_b = seqb)
    for id, species, seqa, seqb in _raw_input_generator_sample()
]
print(yamlify(data, 'Input'))
print()

input = input_generator_sample()

indexer = StringIndexer()
counters = TagCounters()
fors = TaggedDisjointSets()

for tag, seqs in input:
    ids = [indexer.add(seq) for seq in seqs]
    counters.update(tag, ids)
    fors.add(tag, ids)

haplotype_digits = len(str(len(indexer))) + 1
set_digits = len(str(len(fors.get_set_members()))) + 1

data = {
    format_haplotype_id(id, haplotype_digits): seq
    for id, seq in indexer.all()}
print(yamlify(data, 'Haplotype sequences'))
print()

data = {
    tag: {
        'total': counter.total(),
        'haplotypes': {
            format_haplotype_id(id, haplotype_digits): count
            for id, count in counter.items()}}
    for tag, counter in counters.all()}
print(yamlify(data, 'Haplotypes per species'))
print()

data = [
    {
        'species_a': x,
        'species_b': y,
        'common': {
            format_haplotype_id(id, haplotype_digits): count
            for id, count in haplotypes.items()},
    }
    for x, y, haplotypes in counters.all_pairs()
]
print(yamlify(data, 'Haplotypes shared between species'))
print()

data = {
    format_set_id(set, set_digits): [
        format_haplotype_id(id, haplotype_digits)
        for id in haplotypes]
    for set, haplotypes in enumerate(fors.get_set_members())
}
print(yamlify(data, 'Fields of recombination'))
print()

data = {
    format_set_id(set, set_digits): {
        'total': tags.total(),
        'species': dict(tags)}
    for set, tags in fors.get_tags_per_set().items()}
print(yamlify(data, 'Species count per FOR'))
print()

data = {
    tag: {
        'total': sets.total(),
        'FORs': {
            format_set_id(set, set_digits): count
            for set, count in sets.items()}}
    for tag, sets in fors.get_sets_per_tag().items()}
print(yamlify(data, 'FOR count per species'))
print()

data = [
    {
        'species_a': x,
        'species_b': y,
        'common': {
            format_set_id(set, set_digits): count
            for set, count in sets.items()},
    }
    for x, y, sets in fors.get_sets_per_tag_pair()]
print(yamlify(data, 'FORs shared between species'))
print()

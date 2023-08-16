import yaml

from itaxotools.haplostats import HaploStats


def dict_representer(dumper, data):
    return dumper.represent_mapping('tag:yaml.org,2002:map', data.items())


yaml.add_representer(dict, dict_representer)


def yamlify(data, title: str = None) -> str:
    if title:
        data = {title: data}
    return yaml.dump(data, default_flow_style=False)


def raw_input_generator():
    yield ('specimen1', 'verrucosa',  'AAAAAAAAA', 'AAAAAAAAC')
    yield ('specimen2', 'verrucosa',  'AAAAAAAAC', 'AAAAAAAAG')
    yield ('specimen3', 'verrucosa',  'AAAAAAAAG', 'AAAAAAAAA')
    yield ('specimen4', 'mysteriosa', 'CCCCCCCCC', 'CCCCCCCCC')
    yield ('specimen5', 'mysteriosa', 'CCCCCCCCC', 'CCCCCCCCT')
    yield ('specimen6', 'enigmatica', 'GGGGGGGGG', 'CCCCCCCCT')


def extract_input_data(raw_input):
    for _, species, seqa, seqb in raw_input:
        yield (species, [seqa, seqb])


def format_input(raw_input):
    return [
        dict(
            id = id,
            species = species,
            allele_a = seqa,
            allele_b = seqb)
        for id, species, seqa, seqb in raw_input
    ]


def main():
    print()

    data = format_input(raw_input_generator())
    print(yamlify(data, 'Input'))
    print()

    stats = HaploStats()
    stats.set_subset_labels(
        subset_a = 'species_a',
        subset_b = 'species_b',
        subsets = 'species',
    )

    for species, sequences in extract_input_data(raw_input_generator()):
        stats.add(species, sequences)

    data = stats.get_haplotypes()
    print(yamlify(data, 'Haplotype sequences'))
    print()

    data = stats.get_haplotypes_per_subset()
    print(yamlify(data, 'Haplotypes per species'))
    print()

    data = stats.get_haplotypes_shared_between_subsets()
    print(yamlify(data, 'Haplotypes shared between species'))
    print()

    data = stats.get_fields_of_recombination()
    print(yamlify(data, 'Fields of recombination'))
    print()

    data = stats.get_subsets_per_field_of_recombination()
    print(yamlify(data, 'Species count per FOR'))
    print()

    data = stats.get_fields_of_recombination_per_subset()
    print(yamlify(data, 'FOR count per species'))
    print()

    data = stats.get_fields_of_recombination_shared_between_subsets()
    print(yamlify(data, 'FORs shared between species'))
    print()


if __name__ == '__main__':
    main()

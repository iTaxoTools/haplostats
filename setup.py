"""A setuptools based setup module."""

# Always prefer setuptools over distutils
from pathlib import Path

from setuptools import find_namespace_packages, setup

# Get the long description from the README file
here = Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='haplostats',
    version='0.0.1',
    description='Find unique haplotypes, fields of recombination and subset sharing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_namespace_packages(
        include=('itaxotools*',),
        where='src',
    ),
    python_requires='>=3.10.2, <4',
    install_requires=[],
    extras_require={
        'dev': [
            'pyyaml',
            'pytest',
            'autoflake',
            'flake8',
            'isort',
        ],
    },
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
    include_package_data=True,
)

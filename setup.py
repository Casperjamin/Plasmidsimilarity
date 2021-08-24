#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'tables',
    'pyyaml',
    'pandas',
    'joblib',
    'networkx',
    'scipy',
    'snakemake<6',
    'matplotlib',
    'seaborn',
    'biopython'
 ]

setup_requirements = []

test_requirements = []

setup(
    author="Casper Jamin",
    author_email='casperjamin@gmail.com',
    python_requires='>3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Comparing plasmid sequences and its gene content",
    entry_points={
        'console_scripts': [
            'Plasmidsimilarity=Plasmidsimilarity.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='Plasmidsimilarity',
    name='Plasmidsimilarity',
    packages=find_packages(
        include=['Plasmidsimilarity', 'Plasmidsimilarity.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/casperjamin/Plasmidsimilarity',
    version='1.0.1',
    zip_safe=False,
)

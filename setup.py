import setuptools
setuptools.setup(
    python_requires='>=3.6',
    name="Plasmidsimilarity",
    version="0.5.0",
    author="Casper Jamin",
    author_email="casperjamin@gmail.com",
    description="Clustering plasmids based on their k-mer content",
    url="https://github.com/casperjamin/plasmidsimilarity",
    install_requires=[
        'snakemake',
        'numpy',
        'PyYAML',
        'biopython',
        'pandas',
        'networkx',
        'tables',
        'scipy',
        'matplotlib' ,
        'seaborn'],
    entry_points={"console_scripts": ['plasmidsimilarity = plasmidsimilarity.plasmidsimilarity:main']}
    
    )

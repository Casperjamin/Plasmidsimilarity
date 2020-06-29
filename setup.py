import setuptools                                                               
setuptools.setup(                                                              
    name="Plasmidsimilarity",                                                   
    version="v0.4.0",
    author="Casper Jamin",                                               
    author_email="casperjamin@gmail.com",                                       
    description="Clustering plasmids based on their k-mer content"",            
    url="https://github.com/casperjamin/plasmidsimilarity",                     
    install_requires=['numpy', 'biopython','pandas', 'networkx','pytables', 'scipy', 'matplotlib', 'seaborn'],
    python_requires='>=3.6'                                                     
    )        

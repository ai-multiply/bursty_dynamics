from setuptools import find_packages, setup


try:
    with open("Readme.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Long description of the bursty_dynamics package. Readme.md not found."


DESCRIPTION = 'bursty_dynamics is a Python package designed to facilitate the analysis of temporal patterns in longitudinal data. It provides functions to calculate the burstiness parameter (BP) and memory coefficient (MC), detect event trains, and visualise results. '

    
setup(
    name= 'bursty_dynamics',
    version = '0.0.6', 
    description = DESCRIPTION,
    packages = find_packages(),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ai-multiply/bursty_dynamics",
    author = "Alisha Angdmebe",
    author_email = "alisha.angdembe1@gmail.com",
    licence = "MIT",
    classifiers = ["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
    install_requires = ['numpy','pandas', 'seaborn','matplotlib','scipy' ]
)


    
    
    
    
    
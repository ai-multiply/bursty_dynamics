from setuptools import find_packages, setup

with open("Readme.md", "r") as d:
    long_description = d.read()

VERSION = '0.0.2' 
DESCRIPTION = 'burstydynamics is a Python package designed to facilitate the analysis of temporal patterns in longitudinal data. It provides functions to calculate the burstiness parameter (BP) and memory coefficient (MC), detect event trains, and visualize results.'

    
setup(
    name= "burstydynamics",
    version = VERSION, 
    description = DESCRIPTION,
    package_dir = {"":"burstydynamics"},
    packages = find_packages(where = "burstydynamics"),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ai-multiply/bursty_dynamics",
    author = "AI-Multiply",
    author_email = "alisha.angdembe1@gmail.com",
    licence = "MIT",
    classifiers = ["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
    install_requires = ['numpy','pandas', 'seaborn','matplotlib','scipy' ]
)


    
    
    
    
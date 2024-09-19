from setuptools import find_packages, setup

DESCRIPTION = 'bursty_dynamics is a Python package designed to facilitate the analysis of temporal patterns in longitudinal data. It provides functions to calculate the burstiness parameter (BP) and memory coefficient (MC), detect event trains, and visualise results. '

    
setup(
    name= 'bursty_dynamics',
    version = '0.1.2', 
    description = DESCRIPTION,
    packages = find_packages(),
    long_description = open('README.rst').read(),
    long_description_content_type = "text/x-rst",
    url = "https://github.com/ai-multiply/bursty_dynamics",
    author = "Alisha Angdmebe",
    author_email = "alisha.angdembe1@gmail.com",
    licence = "MIT",
    classifiers = ["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
    install_requires = ['numpy','pandas', 'seaborn','matplotlib','scipy' ]
)


    
    
    
    
    
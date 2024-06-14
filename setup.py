from setuptools import find_packages, setup

with open("Readme.md", "r") as d:
    long_description = d.read()

VERSION = '0.0.1' 
DESCRIPTION = 'Identifier of temporal patterns in longitudinal helath data.'

    
setup(
    name= "bursty_dynamics",
    version = VERSION, 
    description = DESCRIPTION,
    package_dir = {"":"bursty_dynamics"},
    packages = find_packages(where = "bursty_dynamics"),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ai-multiply/bursty_dynamics",
    author = "AI-Multiply",
    author_email = "alisha.angdembe1@gmail.com",
    # licence = "MIT",
    classifiers = ["Programming Language :: Python :: 3"],
    python_requires='>=3.6',
    install_requires = ['numpy','pandas', 'seaborn','matplotlib','scipy' ]
)


    
    
    
    
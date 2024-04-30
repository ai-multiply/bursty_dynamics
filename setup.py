from setuptools import find_packages, setup

with open("Readme.md", "r") as d:
    long_description = d.read()

VERSION = '0.0.1' 
DESCRIPTION = 'Identifier of temporal patterns in longitudinal helath data.'

    
setup(
    name= "Bursty_dynamics",
    version = VERSION, 
    description = DESCRIPTION,
    package_dir = {"":"Burst"},
    packages = find_packages(where = "Burst"),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    # url = "https://github.com/{incomplete}",
    author = "AI-Multiply",
    author_email = "alisha.angdembe1@gmail.com",
    # licence = "MIT",
    classifiers = [],
    install_requires = []
)


    
    
    
    
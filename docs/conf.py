# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bursty Dynamics'
copyright = '2024, AI-Multiply'
author = 'AI-Multiply'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os,sys
sys.path.insert(0, os.path.abspath('..'))  # Adjust the path as necessary



extensions = ['sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/.ipynb_checkpoints']

language = 'English'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]



# bursty_dynamics
#     - bursty_dynamics
#         - __init__.py
#         - trains.py
#         - scores.py
#         - visuals.py
#     - setup.py
#     - docs
#         - conf.py
#         - index.rst
#         - source
#             - bursty_dynamics.rst
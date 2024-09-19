*******************
``Bursty Dynamics``
*******************

|PyPI| |Documentation| |DOI|
    
``bursty_dynamics`` is a Python package designed to facilitate the analysis of temporal patterns in longitudinal data. It provides functions to calculate the burstiness parameter (BP) and memory coefficient (MC), detect event trains, and visualise results.

This package implements the alternate burstiness parameter described in the paper ‘Measuring Burstiness for Finite Event Sequences’ by Kim, Eun-Kyeong, and Hang-Hyun Jo, and memory coefficient described in ‘Burstiness and Memory in Complex Systems’ by Goh, K.-I., and A.-L. Barabási. 


Features
========

- Burstiness Parameter (BP) and Memory Coefficient (MC) Calculation: Calculate BP and MC to quantify the irregularity and memory effects of event timing within longitudinal data.
- Event Train Detection: Detect and label event trains based on user-defined criteria such as maximum inter-event time and minimum burst size.
- Train-Level Analysis: Analyse BP and MC for detected event trains, providing insights into temporal patterns within trains of events.
- Visualisation Tools: Visualise temporal patterns with scatter plots, histograms, kernel density estimates (KDE), and more, facilitating interpretation of analysis results.
- User-Friendly Interface: Designed for ease of use, with clear function parameters and output formats, making it accessible to both novice and experienced users.


Installation
============

You can install ``bursty_dynamics`` via pip::
    
    pip install bursty_dynamics

Usage
=====

Here's a quick overview of how to use the main functionalities of the package ::

    from bursty_dynamics.scores import calculate_scores
    from bursty_dynamics.trains import train_detection, train_info, train_scores

    # Load your longitudinal data into a DataFrame
    # df = load_data()

    # calculate BP and MC
    score_df = calculate_scores(df, subject_id = 'eid', time_col = 'event_dt')


For more example of usage, please take a look at ``examples.ipynb`` in the example folder.


Getting Help
============

For more information about ``bursty_dynamics``, please check out:

-  ``bursty_dynamics`` `documentation <https://ai-multiply.github.io/bursty_dynamics/>`__

License
=======

|License|

``bursty_dynamics`` is licensed under the MIT License. See the `LICENSE <https://github.com/ai-multiply/bursty_dynamics/blob/main/LICENSE.txt>`_ file for more details.

.. |PyPI| image:: https://badge.fury.io/py/bursty-dynamics.svg
    :target: https://badge.fury.io/py/bursty-dynamics
.. |Documentation| image:: https://img.shields.io/badge/docs-latest-blue.svg
   :target: https://ai-multiply.github.io/bursty_dynamics/
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.13790003.svg
  :target: https://doi.org/10.5281/zenodo.13790003
.. |License| image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/ai-multiply/bursty_dynamics/blob/main/LICENSE.txt


Contributing
============

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an `issue <https://github.com/ai-multiply/bursty_dynamics/issues>`_ or for questions, suggestions, or general discussion related to our project, please visit our `GitHub Discussions page <https://github.com/ai-multiply/bursty_dynamics/discussions>`_.


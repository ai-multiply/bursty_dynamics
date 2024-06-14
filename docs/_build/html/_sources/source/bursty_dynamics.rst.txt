bursty_dynamics package
========================


Module contents
---------------
This section provides an overview of the main `bursty_dynamics` package and its contents.

.. automodule:: bursty_dynamics
   :members:
   :undoc-members:
   :show-inheritance:

**Overview:**

The `bursty_dynamics` package includes submodules for scoring, training, and visualizing bursty dynamics in time series data. It is designed to be flexible and easy to use, allowing users to quickly analyze and interpret bursty behavior in their data.

**Example Usage:**

.. code-block:: python

   import bursty_dynamics
   from bursty_dynamics import scores, trains, visual

   # Example of using the scoring functions
   score = scores.calculate_scores(df, subject_id = 'eid', time_col = 'event_dt')

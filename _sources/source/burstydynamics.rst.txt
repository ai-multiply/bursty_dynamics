burstydynamics package
========================


Module contents
---------------
This section provides an overview of the main `burstydynamics` package and its contents.

.. automodule:: burstydynamics
   :members:
   :undoc-members:
   :show-inheritance:

**Overview:**

The `burstydynamics` package includes submodules for scoring, training, and visualizing bursty dynamics in time series data. It is designed to be flexible and easy to use, allowing users to quickly analyze and interpret bursty behavior in their data.

**Example Usage:**

.. code-block:: python

   import burstydynamics
   from burstydynamics import scores, trains, visual

   # Example of using the scoring functions
   score = scores.calculate_scores(df, subject_id = 'eid', time_col = 'event_dt')

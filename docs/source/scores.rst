burstydynamics.scores
======================

This module contains functions for caluclating the BP and the MC per subject id using the calculate_scores function. 

.. automodule:: burstydynamics.scores
   :members:
   :undoc-members:
   :show-inheritance:
   
**Example Usage:**

.. code-block:: python

   from burstydynamics.scores import calculate_scores
   score_df = calculate_scores(df, subject_id = 'eid', time_col = 'event_dt')
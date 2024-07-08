bursty_dynamics.trains
======================

This module contains functions for detecting the trains, calculating the BP and MC of the trains, and also getting information of the trians.

.. automodule:: bursty_dynamics.trains
   :members:
   :undoc-members:
   :show-inheritance:
   
**Example Usage:**

.. code-block:: python

   from bursty_dynamics.trains import train_detection, calculate_train_info, calculate_scores_train
   train_df = train_detection(df, subject_id = 'eid', time_col = 'event_dt', max_iet = 30, time_unit='days', min_burst=3)
   train_info = calculate_train_info(train_df, subject_id = 'eid', time_col = 'event_dt', summary_statistic=True)
   train_score = calculate_scores_train(train_df, subject_id = 'eid', time_col ='event_dt', min_event_n= 3)



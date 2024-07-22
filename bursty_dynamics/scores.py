import numpy as np
import pandas as pd
from .shared_function import *
from .visual import *

def calculate_scores(df, subject_id, time_col, scatter=False, hist=False, hue=None):
    """
    Calculate burstiness parameter and memory coefficient.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame.
    subject_id : str
        Name of the column containing subject IDs.
    time_col : str
        Name of the column containing the date.
    scatter : bool, optional
        Whether to plot scatter plot. Default is False.
    hist : bool or str, optional
        Type of histogram to plot:
            - True: Plot histograms for both Burstiness Parameter (BP) and Memory Coefficient (MC).
            - "BP": Plot histogram for Burstiness Parameter only.
            - "MC": Plot histogram for Memory Coefficient only.
            - "Both": Plot histograms for both BP and MC on the same plot.
            - False or None: Do not plot any histograms. Default is False.

    Returns
    -------
    tuple or DataFrame
        If both scatter and hist are True: returns (merged_df, scatter_plot, hist_plot).
        If only scatter is True: returns (merged_df, scatter_plot).
        If only hist is True: returns (merged_df, hist_plot).
        If neither scatter nor hist is True: returns merged_df. 
        
    Notes
    -----
    - `merged_df` : DataFrame
        The input DataFrame with added columns for burstiness parameter (BP) and memory coefficient (MC) scores.
    - `scatter_plot` : matplotlib.figure.Figure or None
        The figure object containing the scatter plot (if scatter=True).
    - `hist_plots` : matplotlib.figure.Figure or None
        The figure objects containing the histogram (if hist=True).
    - Duplicate events based on the `subject_id` and `time_col` are removed to ensure each subject has unique event times before calculating the BP and MC. 
    
    
    """    

    # Check if the required columns are in the DataFrame
    if subject_id not in df.columns:
        print(f"Error: '{subject_id}' column not found in the DataFrame.")
        return
    if time_col not in df.columns:
        print(f"Error: '{time_col}' column not found in the DataFrame.")
        return

    try:
        # Convert time_col to datetime
        df[time_col] = pd.to_datetime(df[time_col])
    except Exception as e:
        print(f"Error converting '{time_col}' to datetime: {e}")
        return

    try:
        # Remove duplicate events
        df = remove_duplicate_events(df, subject_id, time_col)
    except Exception as e:
        print(f"Error removing duplicate events: {e}")
        return

    try:
        # Calculate burstiness parameter and memory coefficient
        B_score = df.groupby(subject_id)[time_col].apply(
            lambda events: burstiness_parameter(events, find_interval_times)
        ).reset_index(name='BP')
        
        MC_pearson = df.groupby(subject_id)[time_col].apply(
            lambda events: memory_coefficient(events, find_interval_times)
        ).reset_index(name='MC')
        
        merged_df = pd.merge(B_score, MC_pearson, on=subject_id, how='outer')
    except Exception as e:
        print(f"Error during calculation of burstiness parameter and memory coefficient: {e}")
        return

    scatter_plot = None
    hist_plots = None

    try:
        if scatter:
            scatter_plot = scatterplot(merged_df, hue=hue)  # Scatter plot

        if hist:
            hist_plots = histogram(merged_df, hist)  # Histogram
    except Exception as e:
        print(f"Error during plotting: {e}")
        return

    if scatter_plot and hist_plots:
        return merged_df, scatter_plot, hist_plots
    elif scatter_plot:
        return merged_df, scatter_plot
    elif hist_plots:
        return merged_df, hist_plots
    else:
        return merged_df
    

#------------------------------------------

def find_interval_times(events):
    try:
        # Ensure events is a numpy array of datetime64
        if not isinstance(events, np.ndarray) or events.dtype.type != np.datetime64:
            raise ValueError("Input must be a numpy array of datetime64 elements.")
        
        # Ensure there are at least two events to find intervals
        if len(events) < 2:
            raise ValueError("At least two datetime events are required to find intervals.")
        
        # Calculate the intervals in minutes
        iet = (np.diff(events).astype('timedelta64[ns]').astype(int) / (10**9 * 60)).tolist()
        return iet
    
    except Exception as e:
        # print any exceptions that occur
        print(f"An error occurred: {e}")
        return []

    
    

__all__ = ['calculate_scores']


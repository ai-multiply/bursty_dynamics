import numpy as np
import pandas as pd
from .shared_function import *
from .visual import *

def calculate_scores(df, subject_id, time_col, scatter=False, hist=False):
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
    """
    try:
        df[time_col] = pd.to_datetime(df[time_col]) # Convert time_col to datetime
        df = remove_duplicate_events(df, subject_id, time_col)
        
        B_score = df.groupby(subject_id)[time_col].apply(lambda events: burstiness_parameter(events, find_interval_times)).reset_index(name='BP')
        MC_pearson = df.groupby(subject_id)[time_col].apply(lambda events: memory_coefficient(events, find_interval_times)).reset_index(name='MC')
        
#         B_score = df.groupby(subject_id)[time_col].apply(burstiness_parameter).reset_index(name='BP')
#         MC_pearson = df.groupby(subject_id)[time_col].apply(memory_coefficient).reset_index(name='MC')
        
        merged_df = pd.merge(B_score, MC_pearson, on=subject_id, how='outer')
        
        scatter_plot = None
        hist_plots = None
        
        if scatter:
            scatter_plot = scatterplot(merged_df) #scatter plot
          
        if hist:
            hist_plots = histogram(merged_df, hist) #histogram
            
        if scatter_plot and hist_plots:
            return merged_df, scatter_plot, hist_plots
        elif scatter_plot:
            return merged_df, scatter_plot
        elif hist_plots:
            return merged_df, hist_plots
        else:
            return merged_df
    
    except KeyError as e:
        print(f"Error: {e} column not found in the DataFrame.")
    except Exception as e:
        print(f"An error occurred: {e}")
        


#------------------------------------------

def find_interval_times(events):
    iet = (np.diff(events).astype('timedelta64[ns]').astype(int) / (10**9 * 60)).tolist()  # Convert nanoseconds to minutes
    return iet



__all__ = ['calculate_scores']


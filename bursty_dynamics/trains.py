import numpy as np
import pandas as pd
from .shared_function import *
from .visual import *

import seaborn as sns
import matplotlib.pyplot as plt


def train_detection(df, subject_id, time_col, max_iet, time_unit='days', min_burst=3, only_trains=True):
    """
    Detects and assigns train IDs to events in the provided DataFrame based on the specified parameters.

    Parameters
    ----------
    df : DataFrame
        The DataFrame containing the data.
    subject_id : str
        The column name for subject IDs.
    time_col : str
        The column name for the datetime values.
    max_iet : int
        Maximum distance between consecutive events in a train, in units specified by `time_unit`.
    time_unit : str, optional
        Unit of time for the intervals ('seconds', 'minutes', 'hours', 'days', 'weeks', 'months', and 'years').
        Default is 'days'.
    min_burst : int, optional
        Minimum number of events required to form a train. Default is 3.
    only_trains : bool, optional
        Whether to return only the events that form trains. Default is True.
    
    Returns
    -------
    DataFrame
        DataFrame with `train_id` included which indicates the train the events belong to.
        
    Examples
    --------
    >>> data = {
    ...     'subject_id': [1, 1, 1, 1 ,2 ,2 ],
    ...     'event_time': ['2023-01-01', '2023-01-02', '2023-01-10','2023-01-20', '2023-01-01', '2023-01-03']
    ... }
    >>> df = pd.DataFrame(data)
    >>> train_df = train_detection(df, 'subject_id', 'event_time', max_iet=30, time_unit='days', min_burst=2)
    >>> train_df
         subject_id  event_time  train_id
    0      1         2023-01-01    1
    1      1         2023-01-02    1
    2      1         2023-01-10    1
    3      1         2023-01-20    1
    4      2         2023-01-01    1
    5      2         2023-01-03    1

    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")
        
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
        df = df.sort_values([subject_id, time_col]).copy()
        train_df = df.assign(train_id=df.groupby(subject_id)[time_col].transform(lambda x: find_bursts(x.values, max_iet, time_unit, min_burst)))
    except Exception as e:
        raise RuntimeError(f"Error while assigning train IDs: {e}")
    
    if only_trains == True:
        train_df = train_df[train_df['train_id']!= 0].copy()
        
    return train_df


def train_info(train_df, subject_id, time_col, summary_statistic=None):
    """
    Calculate summary statistics for train data.

    Parameters
    ----------
    train_df : DataFrame
        DataFrame containing train information.
    subject_id : str
        Name of the column containing subject IDs.
    time_col : str
        Name of the column containing timestamps.
    summary_statistic : bool, optional
        Whether to print summary statistics. Default is False.

    Returns
    -------
    DataFrame
        DataFrame with calculated train information.
        
    Examples
    --------
    >>> train_info(train_df, subject_id = 'subject_id', time_col = 'event_time')
        subject_id train_id  unique_event_counts  total_term_counts  train_start  train_end  train_duration_yrs  total_trains
    0      1          1          4                   4                2023-01-01   2023-01-20    0.05                 1
    1      2          1          2                   2                2023-01-01   2023-01-03    0.01                 1

    
    """
    
    # Check if the required columns are in the DataFrame
    if subject_id not in df.columns:
        print(f"Error: '{subject_id}' column not found in the DataFrame.")
        return
    if time_col not in df.columns:
        print(f"Error: '{time_col}' column not found in the DataFrame.")
        return
    
    df_updated = remove_duplicate_events(train_df, subject_id, time_col)
    
    eventcounts = df_updated.groupby([subject_id, "train_id"]).size().reset_index(name='unique_event_counts') # Count unique events per patient and train_id
    eventcounts1 = train_df.groupby([subject_id, "train_id"]).size().reset_index(name='total_term_counts') #Count total number of terms per patient and train_id. can be many events in a day
    counts = eventcounts.merge(eventcounts1, on=[subject_id, 'train_id'])
    
    train_sum = counts.merge(calculate_train_duration(df_updated, subject_id, time_col), on=[subject_id, "train_id"])
    train_sum['total_trains'] = train_sum[subject_id].map(df_updated[df_updated['train_id']!= 0].groupby(subject_id)["train_id"].nunique())
    
    if summary_statistic == True:
        avg_trains = round(train_sum[train_sum['train_id'] != 0].groupby(subject_id)['train_id'].count().mean(), 2)
        print(f'Average count of trains per patient: {avg_trains}')
        
        average_duration_days = (train_sum['train_end'] - train_sum['train_start']).dt.days.mean()
        median_duration_days = (train_sum['train_end'] - train_sum['train_start']).dt.days.median()

        print("Average duration of trains (in days):", math.floor(average_duration_days))
        print("Median duration of trains (in days):", math.floor(median_duration_days))

        min_unique_events = train_sum['unique_event_counts'].min()
        max_unique_events = train_sum['unique_event_counts'].max()
        print(f"Range of unique events per train: {min_unique_events} - {max_unique_events}")

        min_total_events = train_sum['total_term_counts'].min()
        max_total_events = train_sum['total_term_counts'].max()
        print(f"Range of all events per train: {min_total_events} - {max_total_events}")

    return train_sum


def train_scores(train_df, subject_id, time_col, min_event_n=None, scatter=False, hist=False):
    """
    Calculate Burstiness Parameter (BP) and Memory Coefficient (MC) for each train_id per subject_id.
    
    Parameters
    ----------
    train_df : pd.DataFrame
        Input DataFrame.
    subject_id : str
        Name of the column containing subject IDs.
    time_col : str
        Name of the column containing the date.
    min_event_n : int, optional
        Maximum IET for filtering events. Defaults to None.
    scatter : bool, optional
        Whether to plot scatter plot. Defaults to False.
    hist : str or None, optional
        Type of histogram to plot. Options:
        - True: Plot histograms for both BP and MC.
        - "BP": Plot histogram for BP only.
        - "MC": Plot histogram for MC only.
        - "Both": Plot histograms for both BP and MC on the same plot.
        - False: Do not plot any histograms. Defaults to False.
        
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
        The input DataFrame with burstiness parameter (BP) and memory coefficient (MC) for each train_id per subject_id.
    - `scatter_plot` : matplotlib.figure.Figure or None
        The figure object containing the scatter plot (if scatter=True).
    - `hist_plots` : matplotlib.figure.Figure or None
        The figure objects containing the histogram (if hist=True).
        
    Examples
    --------
    >>> train_scores(train_df, subject_id = 'subject_id', time_col ='event_time', min_event_n= 3)
        subject_id  train_id  BP         MC
    0      1           1      -0.19709   1.0
        
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
        train_df[time_col] = pd.to_datetime(train_df[time_col])
    except Exception as e:
        print(f"Error converting '{time_col}' to datetime: {e}")
        return

    # Remove duplicate events for each subject on the same day
    train_df_updated = remove_duplicate_events(train_df, subject_id, time_col)
        
    # Filter events based on the event max_iet
    if min_event_n:
        train_lengths = train_df_updated.groupby([subject_id, "train_id"])[time_col].transform('count')
        train_df_updated = train_df_updated[(train_lengths >= min_event_n) & (train_df_updated['train_id'] != 0)].copy()

    B_score = train_df_updated.groupby([subject_id, "train_id"])[time_col].apply(lambda events: burstiness_parameter(events, find_interval_times)).reset_index(name='BP')
    MC = train_df_updated.groupby([subject_id, "train_id"])[time_col].apply(lambda events: memory_coefficient(events, find_interval_times)).reset_index(name='MC')

    merged_df = pd.merge(B_score, MC, on=[subject_id, 'train_id'], how='outer')
    
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


#------------------------------------------

def find_interval_times(events, time_unit='days'):
    
    """
    Calculate the interval times between consecutive events in specified time units.

    Parameters:
    events (list): A list of datetime objects or strings that can be converted to datetime objects.
    time_unit (str): The unit of time to convert the interval times to. Options are 
                     'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', and 'years'.
                     Default is 'days'.

    Returns:
    list: A list of interval times in the specified time unit.
    
    Raises:
    ValueError: If the provided time_unit is not one of the valid options.
    
    Example:
    events = ['2021-01-01', '2022-01-01', '2023-06-01']
    find_interval_times(events, 'months')
    # Output: [12, 17]
    """
    
    events = pd.to_datetime(events)
    diff = np.diff(events)

    if time_unit == 'seconds':
        iet = (diff / np.timedelta64(1, 's')).astype(int).tolist()  # Convert to seconds
    elif time_unit == 'minutes':
        iet = (diff / np.timedelta64(1, 'm')).astype(int).tolist()  # Convert to minutes
    elif time_unit == 'hours':
        iet = (diff / np.timedelta64(1, 'h')).astype(int).tolist()  # Convert to hours
    elif time_unit == 'days':
        iet = (diff / np.timedelta64(1, 'D')).astype(int).tolist()  # Convert to days
    elif time_unit == 'weeks':
        iet = (diff / np.timedelta64(1, 'W')).astype(int).tolist()  # Convert to weeks
    elif time_unit == 'months':
        iet = [(events[i+1] - events[i]).days // 30 for i in range(len(events)-1)]  # Approximate months
    elif time_unit == 'years':
        iet = [(events[i+1] - events[i]).days // 365 for i in range(len(events)-1)]  # Approximate years
    else:
        raise ValueError("Invalid time_unit. Choose from 'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', or 'years'.")

    return iet



def find_bursts(events, max_iet, time_unit='minutes', min_burst=3):
    import numpy as np
    """Assigns burst id to events based on max_iet
    
    :param events: a list of numeric timestamps
    :param max_iet: a numeric value for burst limit
    :param min_burst: minimum number of events to form a burst train
    :return a numpy.ndarray
    
    :Example:
    event_df["time"].groupby(event_df.individual_id).transform(lambda x: find_bursts(x.values, 365.2425)))
    """
    
    iet = find_interval_times(events,time_unit )
    # bursts_indices = np.nonzero(iet < max_iet)[0]
    bursts_indices = [i for i, value in enumerate(iet) if value < max_iet]
    indices_diff = np.diff(bursts_indices)
    bursts_breaks = np.nonzero(indices_diff > 1)[0]+1
    bursts_breaks = np.insert(bursts_breaks,[0, len(bursts_breaks)], [0, len(bursts_indices)+1])
    bursts_intervals = [(bursts_breaks[i-1], bursts_breaks[i]) for i in range(1,len(bursts_breaks))]
    bursts = np.zeros(len(events), dtype=int)
    if (len(bursts_breaks) > 0):
        for i in range(1,len(bursts_breaks)):
            begin_burst = bursts_breaks[i-1]
            end_burst = bursts_breaks[i]
            events_idx = bursts_indices[begin_burst:end_burst]
            if (len(events_idx) > 0):
                burst_ids = list(range(min(events_idx),max(events_idx)+2))
                if len(burst_ids) >= min_burst:  #changed
                    bursts[burst_ids] = i
    return bursts



def calculate_train_duration(df_updated, subject_id, time_col):
    """
    Calculate the duration of each train.

    Parameters:
    train_df (DataFrame): DataFrame containing train information.
    subject_id (str): Name of the column containing subject IDs.
    time_col (str): Name of the column containing timestamps.

    Returns:
    DataFrame: DataFrame with train durations calculated.
    """
    grouped_1 = df_updated.groupby([subject_id, "train_id"]).agg(train_start= (time_col, 'min'))
    grouped_2 = df_updated.groupby([subject_id, "train_id"]).agg(train_end= (time_col, 'max'))
    result2 = pd.merge(grouped_1, grouped_2, on=[subject_id, "train_id"]).reset_index()
    result2['train_duration_yrs'] = round((result2['train_end'] - result2['train_start']).dt.days / 365.25,2)

    return result2




__all__ = ['train_detection', 'train_info', 'train_scores']
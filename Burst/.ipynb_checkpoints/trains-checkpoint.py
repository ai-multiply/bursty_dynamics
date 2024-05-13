import numpy as np
import pandas as pd
from scores import *
import math
from scipy.stats import pearsonr

import seaborn as sns
import matplotlib.pyplot as plt


def train_detection(df, subject_id, time_col, max_iet):
    """
    Parameters:
    df (DataFrame): The DataFrame containing the data.
    subject_id (str): The column name for patient IDs.
    time_col (str): The column name for the datetime values.
    max_iet (int): Maximum distance between consecutive events in a train (in days). 
    
    Returns:
    DataFrame: DataFrame with train_id included which indicates the train the events belongs to. 
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")
        
    try:
        df[time_col] = pd.to_datetime(df[time_col])
    except ValueError:
        raise ValueError("Conversion of {} to datetime failed".format(time_col))
        
    train_df = df.assign(train_id=df.groupby(subject_id)[time_col].transform(lambda x: find_bursts(x.values, max_iet)))
    return train_df


def calculate_train_info(train_df, subject_id, time_col):
    df_updated = remove_duplicate_events(train_df, subject_id, time_col)
    
    eventcounts = df_updated.groupby([subject_id, "train_id"]).agg(eventcounts= ('train_id', 'count')).reset_index() #number of events one per day
    eventcounts1 = train_df.groupby([subject_id, "train_id"]).agg(termcounts= ('train_id', 'count')).reset_index() #number of terms, can be many events in a day
    counts = eventcounts.merge(eventcounts1, on=[subject_id, 'train_id'])
    
    train_sum = counts.merge(calculate_train_duration(df_updated, subject_id, time_col), on=[subject_id, "train_id"])
    train_sum['total_clusters'] = train_sum[subject_id].map(df_updated.groupby(subject_id)["train_id"].nunique())
    return train_sum



def calculate_scores_train(train_df, subject_id, time_col, min_event_n=None, scatter=False, hist=None):
    """
    Calculate Burstiness Parameter (BP) and Memory Coefficient (MC) for each train_id per subject_id.
    
    Args:
        train_df (pd.DataFrame): Input DataFrame.
        subject_id (str): Name of the column containing subject IDs.
        time_col (str): Name of the column containing the date.
        min_event_n (int, optional): max_iet for filtering events. Defaults to None.
        scatter (bool): Whether to plot scatter plot.
        hist (str or None): Type of histogram to plot. Options: 
            - True: Plot histograms for both BP and MC.
            - "BP": Plot histogram for BP only.
            - "MC": Plot histogram for MC only.
            - "Both": Plot histograms for both BP and MC on the same plot.
            - None: Do not plot any histograms.
        
    Returns:
        pd.DataFrame: DataFrame with Burstiness Parameter (BP) and Memory Coefficient (MC) for each train_id per subject_id.
    """
    # Convert the time column to datetime
    train_df[time_col] = pd.to_datetime(train_df[time_col])

    # Remove duplicate events for each subject on the same day
    train_df_updated = remove_duplicate_events(train_df, subject_id, time_col)
        
    # Filter events based on the event max_iet
    if min_event_n:
        train_lengths = train_df_updated.groupby([subject_id, "train_id"])[time_col].transform('count')
        train_df_updated = train_df_updated[(train_lengths >= min_event_n) & (train_df_updated['train_id'] != 0)].copy()

    B_score = train_df_updated.groupby([subject_id, "train_id"])[time_col].apply(burstiness_parameter).reset_index(name='BP')
    MC = train_df_updated.groupby([subject_id, "train_id"])[time_col].apply(memory_coefficient).reset_index(name='MC')

    merged_df = pd.merge(B_score, MC, on=[subject_id, 'train_id'], how='outer')
    
    if scatter:
        plt.figure()
        sns.set_theme(rc={'figure.figsize':(9,7)})
        sns.set_theme(style='white')
        sns.jointplot(data=merged_df, x="MC", y="BP", kind="reg", scatter_kws=dict(alpha=0.3, color='blue'),  line_kws=dict(color='black', linewidth=1));
        
    if hist == "BP":
        plt.figure()
        sns.set_theme(rc={'figure.figsize':(9,7)})
        sns.set_theme(style='white')
        sns.histplot(data=merged_df, x="BP", kde=True, color='blue')
    elif hist == "MC":
        plt.figure()
        sns.set_theme(rc={'figure.figsize':(9,7)})
        sns.set_theme(style='white')
        sns.histplot(data=merged_df, x="MC", kde=True, color='magenta')
    elif hist == "Both":
        plt.figure()
        sns.set_theme(rc={'figure.figsize':(9,7)})
        sns.set_theme(style='white')
        sns.histplot(data=merged_df, x="BP", kde=True, color='blue')
        sns.histplot(data=merged_df, x="MC", kde=True, color='magenta')
        plt.xlabel("")
        plt.legend(labels=['BP','MC'])
    elif hist == True:
        plt.figure()
        sns.set_theme(rc={'figure.figsize':(9,7)})
        sns.set_theme(style='white')
        sns.histplot(data=merged_df, x="BP", kde=True, color='blue')
        plt.figure()
        sns.set_theme(rc={'figure.figsize':(9,7)})
        sns.set_theme(style='white')
        sns.histplot(data=merged_df, x="MC", kde=True, color='magenta')

    return merged_df

#------------------------------------------

def find_interval_times(events):
    iet = (np.diff(events).astype('timedelta64[ns]').astype(int) / (10**9 * 60)).tolist()  # Convert nanoseconds to minutes
    return iet



def find_bursts(events, max_iet, min_burst=3):
    import numpy as np
    """Assigns burst id to events based on max_iet
    
    :param events: a list of numeric timestamps
    :param max_iet: a numeric value for burst limit
    :param min_burst: minimum number of events to form a burst train
    :return a numpy.ndarray
    
    :Example:
    event_df["time"].groupby(event_df.individual_id).transform(lambda x: find_bursts(x.values, 365.2425)))
    """
    
    iet = find_interval_times(events)
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
                if len(burst_ids) > min_burst:
                    bursts[burst_ids] = i
    return bursts


def remove_duplicate_events(df, patient_id, time_col):
    """
    Parameters:
    df (DataFrame): The DataFrame containing the data.
    patient_id (str): The column name for patient IDs.
    time_col (str): The column name for the datetime values.
    
    Returns:
    DataFrame: DataFrame with duplicate events removed.
    """
    df_updated = df.drop_duplicates([patient_id, time_col]).sort_values([patient_id, time_col])
    return df_updated



def calculate_train_duration(df_updated, subject_id, time_col):
    grouped_1 = df_updated.groupby([subject_id, "train_id"]).agg(train_start= (time_col, 'min'))
    grouped_2 = df_updated.groupby([subject_id, "train_id"]).agg(train_end= (time_col, 'max'))
    result2 = pd.merge(grouped_1, grouped_2, on=[subject_id, "train_id"]).reset_index()

    return result2


def burstiness_parameter(events):
    """Computes burstiness parameter using Kim and Jo (2016) formula
        
    :param events: a list of numeric timestamps
    :return a real number
    
    .. note::
    Kim, Eun-Kyeong, and Hang-Hyun Jo. ‘Measuring Burstiness for Finite Event Sequences’. Physical Review E 94, no. 3 (15 September 2016): 032311. https://doi.org/10.1103/PhysRevE.94.032311.    
    
    """
    iet = find_interval_times(events)
    n = len(events)
    if (n-1 <= 0):
        return np.nan
    r = np.std(iet)/np.mean(iet)
    p1_term = math.sqrt(n + 1)
    m1_term = math.sqrt(n - 1)
    score = (p1_term * r - m1_term)/((p1_term - 2) * r + m1_term)
    return score


def memory_coefficient(events):
    """Computes memory coefficient using Goh and Barabási (2008) formula
    
    :param events: a list of numeric timestamps
    :return a real number
    
    .. note::
    Goh, K.-I., and A.-L. Barabási. ‘Burstiness and Memory in Complex Systems’. EPL (Europhysics Letters) 81, no. 4 (February 2008): 48002. https://doi.org/10.1209/0295-5075/81/48002.
    
    """
    iet = find_interval_times(events)
    n = len(iet)
    if (n-1 <= 0):
        return np.nan
    first_n = iet[0:-1]
    last_n = iet[1:]
    mean1 = np.mean(first_n)
    mean2 = np.mean(last_n)
    std1 = np.std(first_n)
    std2 = np.std(last_n)
    term1 = first_n - mean1
    term2 = last_n - mean2
    if (std1*std2 == 0):
        return np.nan
    else:
        sum_term = np.sum(term1 * term2, axis = 0)/(std1 * std2)
        return sum_term/(n-1)
    return np.nan




__all__ = ['train_detection', 'calculate_train_info', 'calculate_scores_train']
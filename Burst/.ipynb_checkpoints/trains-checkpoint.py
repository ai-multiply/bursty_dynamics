import numpy as np
import pandas as pd
from scores import *

import numpy as np
import pandas as pd
import math
from scipy.stats import spearmanr
from scipy.stats import pearsonr


def train_detection(df, threshold, subject_id, time_col):
    train_df = df.assign(cluster_id=df.groupby(subject_id)[time_col].transform(lambda x: find_bursts(x.values, threshold)))
    return train_df

def calculate_train_info(train_df, subject_id, time_col, date_col):
    df_updated = remove_duplicate_events(train_df, subject_id, time_col)
    
    eventcounts = df_updated.groupby([subject_id, "cluster_id"]).agg(eventcounts= ('cluster_id', 'count')).reset_index() #number of events one per day
    eventcounts1 = train_df.groupby([subject_id, "cluster_id"]).agg(termcounts= ('cluster_id', 'count')).reset_index() #number of terms, can be many events in a day
    counts = eventcounts.merge(eventcounts1, on=[subject_id, 'cluster_id'])
    
    iet_days = df_updated.groupby([subject_id, "cluster_id"])[time_col].apply(np.diff).reset_index().rename(columns={time_col: 'iet_days'})
    counts_iet = counts.merge(iet_days, on=[subject_id, 'cluster_id'])

    train_sum = counts_iet.merge(calculate_train_duration(df_updated, subject_id, time_col, date_col), on=[subject_id, "cluster_id"])
    train_sum['total_clusters'] = train_sum[subject_id].map(df_updated.groupby(subject_id)["cluster_id"].nunique())
    return train_sum


def calculate_scores_train(train_df, subject_id, time_col):
    train_df_updated = remove_duplicate_events(train_df, subject_id, time_col)  #remove events on the same day
    
    B_score = train_df_updated.groupby([subject_id, "cluster_id"])[time_col].apply(burstiness_parameter).reset_index(name='Bscore')
    MC_pearson = train_df_updated.groupby([subject_id, "cluster_id"])[time_col].apply(memory_coefficient).reset_index(name='MCpearson')
    MC_spearman = train_df_updated.groupby([subject_id, "cluster_id"])[time_col].apply(memory_spearman).reset_index(name='MCspearman')
    
    IET = train_df_updated.groupby([subject_id, "cluster_id"])[time_col].apply(np.diff).reset_index(name='IET')
    
    merged_df = pd.merge(B_score, MC_pearson, on=[subject_id, 'cluster_id'], how='outer')
    merged_df = pd.merge(merged_df, MC_spearman, on=[subject_id, 'cluster_id'], how='outer')
    merged_df = pd.merge(merged_df, IET, on=[subject_id, 'cluster_id'], how='outer')
    
    return merged_df


#------------------------------------------

def remove_duplicate_events(df, subject_id, time_col):
    df_updated = df.drop_duplicates([subject_id, time_col]).sort_values([subject_id, time_col])
    return df_updated


def calculate_train_duration(df_updated, subject_id, time_col, date_col):

    grouped_1 = df_updated.groupby([subject_id, "cluster_id"]).agg(train_startdays= (time_col, 'min'))
    grouped_2 = df_updated.groupby([subject_id, "cluster_id"]).agg(train_enddays= (time_col, 'max'))
    result2 = pd.merge(grouped_1, grouped_2, on=[subject_id, "cluster_id"]).reset_index()
    
    grouped_1 = df_updated.groupby([subject_id, "cluster_id"]).agg(train_start= (date_col, 'min'))
    grouped_2 = df_updated.groupby([subject_id, "cluster_id"]).agg(train_end= (date_col, 'max'))
    result3 = pd.merge(grouped_1, grouped_2, on=[subject_id, "cluster_id"]).reset_index()
    
    merged_result = pd.merge(result2, result3, on=[subject_id, "cluster_id"])

    return merged_result


def find_bursts(events, time_threshold, min_burst=3):
    import numpy as np
    """Assigns burst id to events based on threshold
    
    :param events: a list of numeric timestamps
    :param time_threshold: a numeric value for burst limit
    :param min_burst: minimum number of events to form a burst train
    :return a numpy.ndarray
    
    :Example:
    event_df["time"].groupby(event_df.individual_id).transform(lambda x: find_bursts(x.values, 365.2425)))
    """
    iet = np.diff(events)
    bursts_indices = np.nonzero(iet < time_threshold)[0]
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

def burstiness_parameter(events):

    """Computes burstiness parameter using Kim and Jo (2016) formula
        
    :param events: a list of numeric timestamps
    :return a real number
    
    .. note::
    Kim, Eun-Kyeong, and Hang-Hyun Jo. ‘Measuring Burstiness for Finite Event Sequences’. Physical Review E 94, no. 3 (15 September 2016): 032311. https://doi.org/10.1103/PhysRevE.94.032311.    
    
    """
    iet = np.diff(events)
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
    iet = np.diff(events)
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


def memory_spearman(events):
    iet = np.diff(events)
    n = len(iet)
    if (n - 1) <= 0:
        return np.nan
    first_n = iet[:n-1]
    last_n = iet[1:]
    return spearmanr(first_n, last_n).correlation




__all__ = ['train_detection', 'calculate_train_info', 'calculate_scores_train']
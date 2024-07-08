import numpy as np
# import pandas as pd
import math
from scipy.stats import pearsonr


def remove_duplicate_events(df, subject_id, time_col):
    """
    Parameters:
    train_df (DataFrame): DataFrame containing train information.
    subject_id (str): Name of the column containing subject IDs.
    time_col (str): Name of the column containing timestamps.
    
    Returns:
    DataFrame: DataFrame with duplicate events removed.
    """
    df_updated = df.drop_duplicates([subject_id, time_col]).sort_values([subject_id, time_col])
    return df_updated


def burstiness_parameter(events, find_interval_times):
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



def memory_coefficient(events, find_interval_times):
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




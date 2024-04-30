import numpy as np
import pandas as pd
import math
from scipy.stats import spearmanr
from scipy.stats import pearsonr


def calculate_scores(df, subject_id, time_col):
    df = remove_duplicate_events(df, subject_id, time_col)
    
    B_score = df.groupby([subject_id])[time_col].apply(burstiness_parameter).reset_index(name='Bscore')
    MC_pearson = df.groupby([subject_id])[time_col].apply(memory_coefficient).reset_index(name='MCpearson')
    MC_spearman = df.groupby([subject_id])[time_col].apply(memory_spearman).reset_index(name='MCspearman')
    
    IET = df.groupby([subject_id])[time_col].apply(np.diff).reset_index(name='IET')
    
    merged_df = pd.merge(B_score, MC_pearson, on=subject_id, how='outer')
    merged_df = pd.merge(merged_df, MC_spearman, on=subject_id, how='outer')
    merged_df = pd.merge(merged_df, IET, on=subject_id, how='outer')
    
    return merged_df

#------------------------------------------

def remove_duplicate_events(df, patient_id, time_col):
    df_updated = df.drop_duplicates([patient_id, time_col]).sort_values([patient_id, time_col])
    return df_updated


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



def local_variation(events):
    """Computes local variation using Shinomoto et al. (2003)
    
    :param events: a list of numeric timestamps
    :return a real number
    
    .. note::
    Shinomoto, Shigeru, Keisetsu Shima, and Jun Tanji. ‘Differences in Spiking Patterns Among Cortical Neurons’. Neural Computation 15, no. 12 (1 December 2003): 2823–42. https://doi.org/10.1162/089976603322518759.
    
    """
    iet = np.diff(events)
    n = len(iet)
    if (n-1 <= 0):
        return np.nan
    first_n = iet[0:-1]
    last_n = iet[1:]
    upper_term = 3*pow(first_n - last_n, 2)
    lower_term = pow(first_n + last_n, 2)
    if (np.sum(lower_term, axis = 0) == 0):
        return np.nan
    term = np.sum(upper_term/lower_term, axis = 0)
    return term/(n-1)


__all__ = ['calculate_scores']
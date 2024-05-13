import numpy as np
import pandas as pd
import math
from scipy.stats import pearsonr

import seaborn as sns
import matplotlib.pyplot as plt


def calculate_scores(df, subject_id, time_col, scatter=False, hist=None):
    """
    Calculate burstiness parameter and memory coefficient.

    Parameters:
        df (DataFrame): Input DataFrame.
        subject_id (str): Name of the column containing subject IDs.
        time_col (str): Name of the column containing the date.
        scatter (bool): Whether to plot scatter plot.
        hist (str or None): Type of histogram to plot. Options: 
            - True: Plot histograms for both BP and MC.
            - "BP": Plot histogram for BP only.
            - "MC": Plot histogram for MC only.
            - "Both": Plot histograms for both BP and MC on the same plot.
            - None: Do not plot any histograms.

    Returns:
        DataFrame: Merged DataFrame containing burstiness parameter and memory coefficient scores.
    """
    try:
        df[time_col] = pd.to_datetime(df[time_col]) # Convert time_col to datetime
        df = remove_duplicate_events(df, subject_id, time_col)
        
        B_score = df.groupby(subject_id)[time_col].apply(burstiness_parameter).reset_index(name='BP')
        MC_pearson = df.groupby(subject_id)[time_col].apply(memory_coefficient).reset_index(name='MC')
        
        merged_df = pd.merge(B_score, MC_pearson, on=subject_id, how='outer')
        
        if scatter:
            plt.figure()
            sns.set_theme(style='white')
            plot= sns.jointplot(data=merged_df, x="MC", y="BP", kind="reg", scatter_kws=dict(alpha=0.3, color='blue'),  line_kws=dict(color='black', linewidth=1),
                               marginal_kws=dict(bins=20))
            plot.fig.set_size_inches((9, 7))
            plt.show()
            
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
    
    except KeyError as e:
        print(f"Error: {e} column not found in the DataFrame.")
    except Exception as e:
        print(f"An error occurred: {e}")
        


#------------------------------------------


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


def find_interval_times(events):
    iet = (np.diff(events).astype('timedelta64[ns]').astype(int) / (10**9 * 60)).tolist()  # Convert nanoseconds to minutes
    return iet



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

__all__ = ['calculate_scores']
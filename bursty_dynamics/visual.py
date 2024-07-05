import matplotlib.pyplot as plt
import seaborn as sns

def gridplot(df, bins=25, lower_limit=0, text_scaling=6, figsize=(9, 7), **kwargs):
    """
    Create a grid plot of Memory Coefficient (MC) vs Burstiness Parameter (BP) with a color bar.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame containing columns 'MC' and 'BP'.
    bins : int, optional
        Number of bins for the histogram. Default is 25.
    lower_limit : int, optional
        Minimum value for the color scale. Values below this will be colored grey. Default is 0.
    text_scaling : float, optional
        Scaling factor for the text in the plot. Default is 6.
    figsize : tuple, optional
        Size of the figure. Default is (9, 7).

    Returns
    -------
    matplotlib.figure.Figure
        The figure object containing the plot.
    """
    plt.figure(figsize=figsize)
    cmap = plt.cm.viridis
    cmap.set_under('grey')
    sns.set(style="white", font_scale=text_scaling/6)
    g = sns.histplot(data=df, x="MC", y="BP", bins=bins, cbar=True, cmap=cmap, 
                     cbar_kws=dict(label = 'count'),vmin= lower_limit,  **kwargs)
    g.set_xlim(-1, 1)
    g.set_ylim(-1, 1)
    g.set_xticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
    g.set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
    fig = g.figure
    plt.close(fig)
    return fig
    
    
def histogram(df, hist=True, set_axis=False, **kwargs):
    """
    Plot histograms for Burstiness Parameter (BP) and Memory Coefficient (MC).

    Parameters
    ----------
    df : DataFrame
        Input DataFrame containing columns 'BP' and 'MC'.
    hist : bool or str, optional
        If True, plot separate histograms for 'BP' and 'MC'.
        If 'Both', plot overlapping histograms for 'BP' and 'MC'.
        If 'BP' or 'MC', plot histogram for the specified column.
        Default is True.
    set_axis : bool, optional
        Whether to set axis limits to [-1, 1]. Default is False.

    Returns
    -------
    list
        List of matplotlib.figure.Figure objects containing the generated plots.
    """
    sns.set_theme(rc={'figure.figsize': (9, 7)}, style='white')

    hist_options = {
        "BP": ("BP", "blue"),
        "MC": ("MC", "magenta")}
    

    if hist in hist_options:
        column, color = hist_options[hist]
        fig = plt.figure()
        sns.histplot(data=df, x=column, kde=True, color=color, **kwargs)
        if set_axis:
            plt.xlim(-1, 1)
        plt.close(fig)
        return fig
    
    elif hist == "Both":
        fig = plt.figure()
        sns.histplot(data=df, x="BP", kde=True, color='blue', **kwargs)
        sns.histplot(data=df, x="MC", kde=True, color='magenta', alpha=0.5, **kwargs)
        plt.xlabel("")
        plt.legend(labels=['BP', 'MC'])
        if set_axis:
            plt.xlim(-1, 1)
        plt.close(fig)
        return fig
    
    elif hist is True:
        fig, axs = plt.subplots(1, len(hist_options), figsize=(12, 6))  # Create subplots based on number of hist_options
        for i, (column, color) in enumerate(hist_options.values()):
            sns.histplot(data=df, x=column, kde=True, color=color, ax=axs[i], **kwargs)
            axs[i].set_xlabel(column)
            if set_axis:
                axs[i].set_xlim(-1, 1)
        plt.close(fig)
        return fig
    
    else:
        print("Invalid 'hist' parameter. Please choose from 'BP', 'MC', 'Both', or True.")
        
        

def scatterplot(df, set_axis=False, **kwargs):
    """
    Create a scatter plot with marginal histograms showing the relationship between 'MC' and 'BP'.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame containing columns 'MC' and 'BP'.
    set_axis : bool, optional
        Whether to set axis limits to [-1, 1]. Default is False.
    kwargs
        Additional keyword arguments passed to `sns.jointplot`.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object containing the scatter plot and marginal histograms.
    """
    sns.set_theme(style='white')
    plot= sns.jointplot(data=df, x="MC", y="BP", kind="reg", scatter_kws=dict(alpha=0.3, color='blue'),  line_kws=dict(color='black', linewidth=1),
                       marginal_kws=dict(bins=20), **kwargs)
    if set_axis:
        plot.ax_joint.set_xlim(-1, 1)
        plot.ax_joint.set_ylim(-1, 1)
    plot.fig.set_size_inches((9.5, 7))
    plt.close(plot.fig)
    return plot.fig



def train_duration(train_info_df, x_limit=5, **kwargs):
    """
    Plots a distribution of train durations in years from the given DataFrame.

    Parameters
    ----------
    train_info_df : DataFrame
        A DataFrame containing a column named 'train_duration_yrs' which 
        holds the duration of training in years for different entries.
    x_limit : int, optional
        The upper limit for the x-axis. Default is 5.

    Returns
    -------
    None
        This function only displays the plot and does not return any value.
    """
    fig, ax = plt.subplots()
    sns.histplot(train_info_df["train_duration_yrs"], kde=True, 
                 bins=round(train_info_df['train_duration_yrs'].max()*2), color = 'darkblue', **kwargs)
    ax.set_xlabel('Train duration (years)', fontsize=14)
    ax.set_ylabel('Density', fontsize=14) 
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_xlim(0, x_limit)
    plt.close(fig)
    return fig

def event_counts(train_info_df, x_limit=30, **kwargs):
    """
    Plots a count of unique events per train from the given DataFrame.

    Parameters
    ----------
    train_info_df : DataFrame
        A DataFrame containing a column named 'unique_event_counts' which 
        holds the count of unique events (no duplicates at same time) for different entries.
    x_limit : int, optional
        The upper limit for the x-axis. Default is 30.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object containing the plot.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=train_info_df[train_info_df["unique_event_counts"] <= x_limit], 
                  x="unique_event_counts", color='darkblue', ax=ax, **kwargs)
    ax.set_xlabel('Events counts per train', fontsize=14)
    ax.set_ylabel('Counts', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.close(fig)  # Prevents the plot from displaying in interactive environments
    
    return fig
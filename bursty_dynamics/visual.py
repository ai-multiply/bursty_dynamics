import matplotlib.pyplot as plt
import seaborn as sns

def gridplot(df, bins=25, lower_limit=0, text_scaling=6, figsize=(9, 7), **kwargs):
    """
    Create a grid plot of Memory Coefficient (MC) vs Burstiness Parameter (BP) with a colour bar.

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
        
    Example
    -------
    Here is an example plot of the function:

    .. image:: /_static/images/grid.png
       :alt: Example Plot
       :align: center
       :scale: 40%

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
    
    
def histogram(df, hist=True, set_axis=False, hue=None, **kwargs):
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
    hue : str, optional
        Column name for hue segmentation. Default is None.
    kwargs : 
        Additional keyword arguments passed to `sns.histplot`.


    Returns
    -------
    matplotlib.figure.Figure or None
        Figure object containing the generated plots if successful,
        otherwise None if the 'hist' parameter is invalid.
        
    Notes
    -----
    - If 'hist' is True, it will create separate histograms for 'BP' and 'MC' in a vertical layout.
    - If 'hist' is 'Both', it will create overlapping histograms for 'BP' and 'MC' on the same plot.
    - If 'hist' is 'BP' or 'MC', it will create a histogram for the specified column.
    - The `hue` parameter allows for segmented histograms based on the specified column.
    - When `hist` is set to 'Both', the `hue` parameter is ignored.
    - The `set_axis` parameter can be used to standardize the x-axis range to [-1, 1].
    - Additional styling and plotting options can be passed through `**kwargs`.
        
    Example
    -------
    Here is an example plot of the function:

    .. image:: /_static/images/histo.png
       :alt: Example Plot
       :align: center
       :scale: 40%
       
    """
    # Check if required columns are in the DataFrame
    if hue and hue not in df.columns:
        raise ValueError(f"Hue column '{hue}' not found in DataFrame.")
        
    sns.set_theme(rc={'figure.figsize': (9, 7)}, style='white')

    hist_options = {
        "BP": "blue",
        "MC": "magenta"}
    
    if hue is not None:
        palette = sns.color_palette("bright", df[hue].nunique())
    else:
        palette = None
    

    if hist in ['BP', 'MC']:
        color = hist_options[hist]
        fig = plt.figure()
        plot = sns.histplot(data=df, x=hist, kde=True, hue=hue, palette=palette, color = color, **kwargs)
        sns.move_legend(plot, "upper left", bbox_to_anchor=(1, 1))
        if set_axis:
            plt.xlim(-1, 1)
        plt.close(fig)
        return fig
    
    elif hist == "Both":
        fig = plt.figure()
        sns.histplot(data=df, x="BP", kde=True, color='blue', **kwargs)
        sns.histplot(data=df, x="MC", kde=True, color='magenta', alpha=0.5, **kwargs)
        plt.xlabel("Score")
        plt.legend(labels=['BP', 'MC'])
        if set_axis:
            plt.xlim(-1, 1)
        plt.close(fig)
        return fig
    
    elif hist is True:
        fig, axs = plt.subplots(2, 1, figsize=(7, 9))  # Create subplots based on number of hist_options
        for i, (column, color) in enumerate({'BP': 'blue', 'MC': 'magenta'}.items()):
            sns.histplot(data=df, x=column, hue=hue, kde=True, palette=palette, color=color, ax=axs[i], **kwargs)
            axs[i].set_xlabel(column)
            
            if set_axis:
                axs[i].set_xlim(-1, 1)

        if hue is not None:
            sns.move_legend(axs[0], "upper right", bbox_to_anchor=(1.35, 1))
            sns.move_legend(axs[1], "upper right", bbox_to_anchor=(1.35, 1))

        # plt.tight_layout()
        plt.close(fig)
        return fig
    
    else:
        print("Invalid 'hist' parameter. Please choose from 'BP', 'MC', 'Both', or True.")
        

def scatterplot(df, hue=None, set_axis=False, **kwargs):
    """
    Create a scatter plot with marginal histograms showing the relationship between 'MC' and 'BP'.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame containing columns 'MC' and 'BP' which are plotted on the x and y axes, respectively.
    hue : str, optional
        Column name in the DataFrame used for color encoding of the scatter plot. If None, the plot is created without color encoding.
    set_axis : bool, optional
        Whether to set the axis limits to [-1, 1]. Default is False. If True, the x and y axes will be constrained to the range [-1, 1].
    kwargs
        Additional keyword arguments passed to `sns.jointplot`.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object containing the scatter plot and marginal histograms.
        
    Example
    -------
    Here is an example plot of the function:

    .. image:: /_static/images/scatter.png
       :alt: Example Plot
       :align: center
       :scale: 40%
       
    """
    # Check if required columns are in the DataFrame
    if 'MC' not in df.columns or 'BP' not in df.columns:
        raise ValueError("DataFrame must contain 'MC' and 'BP' columns.")
    if hue and hue not in df.columns:
        raise ValueError(f"Hue column '{hue}' not found in DataFrame.")
        
    if hue:
        plot = sns.jointplot(
            data=df,
            x='MC',
            y='BP',
            kind='scatter',
            hue=hue,
            palette="tab10",
            joint_kws=dict(s=50, alpha=0.4, edgecolor=None),
            **kwargs)       
        plt.legend(bbox_to_anchor=(1.25, 1), loc='upper left', title=hue) 
        plt.subplots_adjust(right=1)

        
    else:
        # Plot without hue
        plot = sns.jointplot(
            data=df,
            x='MC',
            y='BP',
            kind="reg",
            scatter_kws=dict(alpha=0.3, color='blue'),
            line_kws=dict(color='black', linewidth=1),
            marginal_kws=dict(bins=20),
            **kwargs)
        
    # Adjust axis limits if set_axis is True
    if set_axis:
        plot.ax_joint.set_xlim(-1, 1)
        plot.ax_joint.set_ylim(-1, 1)
        
    plot.fig.set_size_inches((9.5, 7)) 
    plt.close(plot.fig)
    return plot.fig


def train_duration(train_info_df, x_limit=5, hue=None,**kwargs):
    """
    Plots a distribution of train durations in years from the given DataFrame.

    Parameters
    ----------
    train_info_df : DataFrame
        A DataFrame containing a column named 'train_duration_yrs' which 
        holds the duration of training in years for different entries.
    x_limit : int, optional
        The upper limit for the x-axis. Default is 5.
    hue : str, optional
        Column name for hue segmentation. Default is None.
    kwargs : 
        Additional keyword arguments passed to `sns.histplot`.

    Returns
    -------
    matplotlib.figure.Figure
        Figure object containing the generated plot.
        
    Example
    -------
    Here is an example plot of the function:

    .. image:: /_static/images/train_duration.png
       :alt: Example Plot
       :align: center
       :scale: 40%
       
    """
    # Check if required columns are in the DataFrame
    if hue and hue not in train_info_df.columns:
        raise ValueError(f"Hue column '{hue}' not found in DataFrame.")
        
    # Notify about train_id filtering
    if (train_info_df["train_id"] == 0).any():
        print("Rows with train_id = 0 found and will be excluded.")
        train_info_df = train_info_df[train_info_df["train_id"] != 0]
    else:
        print("No rows with train_id = 0 found. Proceeding with all data.")
        
    fig, ax = plt.subplots()
    
    if hue is not None:
        palette = sns.color_palette("bright", train_info_df[hue].nunique())
    else:
        palette = None
        
    sns.histplot(data=train_info_df, x="train_duration_yrs", kde=True, 
                 bins=round(train_info_df['train_duration_yrs'].max()*2), hue=hue, palette=palette, color = 'darkblue', **kwargs)
    ax.set_xlabel('Train duration (years)', fontsize=14)
    ax.set_ylabel('Density', fontsize=14) 
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_xlim(0, x_limit)
    plt.close(fig)
    return fig


def event_counts(train_info_df, x_limit=30, hue=None, **kwargs):
    """
    Plots the count of non-duplicate timestamped events per train from the given DataFrame.

    Parameters
    ----------
    train_info_df : DataFrame
        A DataFrame containing a column named 'unique_event_counts' which 
        holds the count of unique events (no duplicates at same time) for different entries.
        Additionally, it is assumed that the DataFrame contains a 'train_id' column.
    x_limit : int, optional
        The upper limit for the x-axis. Default is 30.
    hue : str, optional
        Column name for hue segmentation. Default is None.
    kwargs : 
        Additional keyword arguments passed to `sns.countplot`.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object containing the plot.
        
    Example
    -------
    Here is an example plot of the function:

    .. image:: /_static/images/event_counts.png
       :alt: Example Plot
       :align: center
       :scale: 40%
       
    """
    # Check if required columns are in the DataFrame
    if hue and hue not in train_info_df.columns:
        raise ValueError(f"Hue column '{hue}' not found in DataFrame.")
        
    # Check if any train_id == 0 exists
    if (train_info_df["train_id"] == 0).any():
        print("Rows with train_id = 0 found and will be excluded.")
    else:
        print("No rows with train_id = 0 found. Proceeding with all data.")

    print(f"Filtering data to include 'unique_event_counts' ≤ {x_limit} (default value for x_limit is 30).")
    filtered_data = train_info_df[(train_info_df["train_id"] != 0) & (train_info_df["unique_event_counts"] <= x_limit)]

    fig, ax = plt.subplots(figsize=(8, 5))
    
    if hue is not None:
        palette = sns.color_palette("bright", train_info_df[hue].nunique())
    else:
        palette = None
        
    sns.countplot(data=filtered_data, 
                  x="unique_event_counts", hue=hue, palette=palette, ax=ax, **kwargs)

    # Set axis labels
    ax.set_xlabel('Number of Unique Events per Train', fontsize=14)
    ax.set_ylabel('Number of Trains', fontsize=14)
    # Adjust tick parameters
    ax.tick_params(axis='both', which='major', labelsize=14)

    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    plt.close(fig)  # Prevents the plot from displaying in interactive environments
    
    return fig

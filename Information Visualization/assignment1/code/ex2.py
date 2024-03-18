import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def plot_timeseries_accurate(csv_dir, title='Price (USD) over Time', xlab='Date', ylab='Price (USD)'):
    """
    Plots a timeseries of price data from a CSV file.

    Parameters:
    - csv_dir (str): The directory path of the CSV file.
    - title (str): The title of the plot (default: 'Price (USD) over Time').
    - xlab (str): The label for the x-axis (default: 'Date').
    - ylab (str): The label for the y-axis (default: 'Price (USD)').

    Returns:
    - df (pandas.DataFrame): The DataFrame containing the data from the CSV file.
    """
    df = pd.read_csv(csv_dir)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Price (USD)'], linestyle='-')
    plt.title(title)
    plt.ylim(0, max(df['Price (USD)']) * 1.05)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return df

def trendline_for_plot(x,y):
    model = LinearRegression()
    model.fit(x, y)
    return model.predict(x)

def rolling_average(y, window=30):
    return pd.Series(y).rolling(window).mean()

def plot_together(csv_dirs, colours, title='Price (USD) over Time', xlab='Date', ylab='Price (USD)', ymin=0, trendline=False, rolling_avg=0, scale='linear',minday=None,maxday=None, first_plot=0, other_plot=0,grid=True,leg=True):
    """"
    Plot multiple CSV files together on the same graph.

    Parameters:
    - csv_dirs (list): List of file paths to the CSV files.
    - colours (list): List of colors for each CSV file. If using rolling average, make sure the colours used allow for a "dark+colourname" version.
    - title (str): Title of the graph (default: 'Price (USD) over Time').
    - xlab (str): Label for the x-axis (default: 'Date').
    - ylab (str): Label for the y-axis (default: 'Price (USD)').
    - ymin (float): Minimum value for the y-axis (default: 0).
    - trendline (bool): Whether to plot a trendline for each CSV file (default: False).
    - rolling_avg (int): Whether to plot a rolling average for each CSV file (default: 0 meaning no rolling average displayed).
    - scale (str): Scale of the y-axis ('linear' or 'log') (default: 'linear').
    - minday (str): Minimum date to include in the plot (default: None).
    - maxday (str): Maximum date to include in the plot (default: None).
    - first_plot (int): Type of plot for the first CSV file (0 for line plot, 1 for bar plot) (default: 0).
    - other_plot (int): Type of plot for the other CSV files (0 for line plot, 1 for bar plot) (default: 0).
    - grid (bool): Whether to show grid lines on the graph (default: True).
    - leg (bool): Whether to show the legend on the graph (default: True).

    Returns:
    - None
    """
    assert len(csv_dirs) == len(colours), "Number of csv files and colours must be the same"
    df = pd.read_csv(csv_dirs[0])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    if minday != None:
        df = df[df['Date'] >= minday]
    if maxday != None:
        df = df[df['Date'] <= maxday]

    # Plotting
    plt.figure(figsize=(10, 6))
    if first_plot == 0:
        plt.plot(df['Date'], df['Price (USD)'], linestyle='-', label=csv_dirs[0].split('.')[0], color=colours[0])
    else:
        plt.bar(df['Date'], df['Price (USD)'], label=csv_dirs[0].split('.')[0], color=colours[0])
    maxy = max(df['Price (USD)'])*1.05
    if trendline:
        x = df['Date'].index.values.reshape(-1, 1)
        y = df['Price (USD)'].values.reshape(-1, 1)
        plt.plot(df['Date'], trendline_for_plot(x,y), linestyle='--', label=('Linear trendline for ' + csv_dirs[0].split('.')[0]), color=colours[0])
    if rolling_avg!=0:
        plt.plot(df['Date'], rolling_average(df['Price (USD)'],window=rolling_avg), linestyle='--', label=('Rolling average (' + str(rolling_avg) + ' days) for ' + csv_dirs[0].split('.')[0]), color=('dark'+str(colours[0])))

    # Rest of the csv files
    for csv_dir in csv_dirs[1:]:
        df = pd.read_csv(csv_dir)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        if minday != None:
            df = df[df['Date'] >= minday]
        if maxday != None:
            df = df[df['Date'] <= maxday]

        # Plotting
        if other_plot == 0:
            plt.plot(df['Date'], df['Price (USD)'], linestyle='-', label=csv_dir.split('.')[0], color=colours[csv_dirs.index(csv_dir)])
        else:
            plt.bar(df['Date'], df['Price (USD)'], label=csv_dir.split('.')[0], color=colours[csv_dirs.index(csv_dir)])
        if max(df['Price (USD)']) > maxy:
            maxy = max(df['Price (USD)'])*1.05
        if trendline:
            x = df['Date'].index.values.reshape(-1, 1)
            y = df['Price (USD)'].values.reshape(-1, 1)
            plt.plot(df['Date'], trendline_for_plot(x,y), linestyle='--', label=('Linear trendline for ' + csv_dir.split('.')[0]), color=colours[csv_dirs.index(csv_dir)])
        if rolling_avg!=0:
            plt.plot(df['Date'], rolling_average(df['Price (USD)'],window=rolling_avg), linestyle='--', label=('Rolling average (' + str(rolling_avg) + ' days) for '  + csv_dir.split('.')[0]), color=('dark'+str(colours[csv_dirs.index(csv_dir)])))

    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.yscale(scale)
    plt.ylim(ymin, maxy)
    plt.xticks(rotation=25)
    if leg:
        plt.legend()
    plt.grid(grid)
    plt.tight_layout()
    plt.show()
    return None

# Function to plot two data frames together but with different y-axis
def plot_together_diff(csv_dir1, csv_dir2, colours, title='Price (USD) over Time', xlab='Date', ylab1='Price (USD)', ylab2='Price (USD)', ymin1=0, ymin2=0, trendline=False, scale='linear', minday=None, maxday=None):
    df1 = pd.read_csv(csv_dir1)
    df1['Date'] = pd.to_datetime(df1['Date'])
    df1 = df1.sort_values(by='Date')
    if minday != None:
        df1 = df1[df1['Date'] >= minday]
    if maxday != None:
        df1 = df1[df1['Date'] <= maxday]

    df2 = pd.read_csv(csv_dir2)
    df2['Date'] = pd.to_datetime(df2['Date'])
    df2 = df2.sort_values(by='Date')
    if minday != None:
        df2 = df2[df2['Date'] >= minday]
    if maxday != None:
        df2 = df2[df2['Date'] <= maxday]

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(df1['Date'], df1['Price (USD)'], linestyle='-', label=csv_dir1.split('.')[0], color=colours[0])
    ax2.plot(df2['Date'], df2['Price (USD)'], linestyle='-', label=csv_dir2.split('.')[0], color=colours[1])

    if trendline:
        x1 = df1['Date'].index.values.reshape(-1, 1)
        y1 = df1['Price (USD)'].values.reshape(-1, 1)
        ax1.plot(df1['Date'], trendline_for_plot(x1, y1), linestyle='--', label=('Linear trendline for ' + csv_dir1.split('.')[0]), color=colours[0])

        x2 = df2['Date'].index.values.reshape(-1, 1)
        y2 = df2['Price (USD)'].values.reshape(-1, 1)
        ax2.plot(df2['Date'], trendline_for_plot(x2, y2), linestyle='--', label=('Linear trendline for ' + csv_dir2.split('.')[0]), color=colours[1])

    ax1.set_title(title)
    ax1.set_xlabel(xlab)
    ax1.set_ylabel(ylab1)
    ax2.set_ylabel(ylab2)
    ax1.set_yscale(scale)
    ax2.set_yscale(scale)
    ax1.set_ylim(ymin1, max(df1['Price (USD)'])*1.05)
    ax2.set_ylim(ymin2, max(df2['Price (USD)'])*1.05)
    ax1.xaxis.set_tick_params(rotation=25)
    #ax1.legend(loc='lower left')
    #ax2.legend(loc='right')
    ax1.grid(True)
    ax2.grid(True)
    plt.tight_layout()
    plt.show()
    return None


if __name__ == '__main__':
    csv_bitcoin = 'Bitcoin.csv'
    csv_nasdaq = "Nasdaq.csv"
    ## Bias pro-bitcoin
    # plot_together([csv_bitcoin, csv_nasdaq], colours=['darkorange','mediumseagreen'], ymin=10000, trendline=True, minday='2020-10-01', maxday='2021-02-15', first_plot=1)
    ## Bias pro-nasdaq
    # plot_together_diff(csv_bitcoin, csv_nasdaq, colours=['salmon','mediumseagreen'], ymin1=15000, trendline=True, minday='2022-03-01', maxday='2023-10-01', ylab1='Bitcoin Price (USD)', ylab2='NASDAQ Price (USD)')
    ## Neutral
    plot_together([csv_bitcoin, csv_nasdaq], colours=['violet','slategray'], grid=True, rolling_avg=60)
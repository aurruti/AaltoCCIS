import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.manifold import Isomap

def trellis(data):
    """
    Create a trellis plot of the data. The plot will have 9 subplots, with the following
    variables plotted against each other: X vs Y, X vs Z, Y vs X, Y vs Z, Z vs X, Z vs Y.
    The diagonal will be histograms of the respective variables.
    The color of the points will be the row number.
    
    Inputs:
    - data: a pandas DataFrame with 3 columns
    
    Returns:
    - fig: the figure object
    - axs: an array of the 9 axes objects
    """
    x = data.iloc[:, 0]
    y = data.iloc[:, 1]
    z = data.iloc[:, 2]
    colors = np.arange(1, len(data)+1)

    fig, axs = plt.subplots(3, 3, figsize=(12, 12))
    axs = axs.flatten()
    
    # Plot each subplot
    axs[0].hist(x, bins=20, color='blue', alpha=0.7)
    axs[0].get_yaxis().set_visible(False)
    axs[0].get_xaxis().set_visible(False)
    axs[0].set_title('X')
    axs[0].set_ylabel('X')
    axs[1].scatter(x, y, c=colors, cmap='viridis', alpha=0.7, marker='.')
    axs[1].set_title('Y')
    axs[1].get_xaxis().set_visible(False)
    axs[2].scatter(x, z, c=colors, cmap='viridis', alpha=0.7, marker='.')
    axs[2].set_title('Z')
    axs[2].get_yaxis().set_visible(False)
    axs[2].get_xaxis().set_visible(False)

    axs[3].scatter(y, x, c=colors, cmap='viridis', alpha=0.7, marker='.')
    axs[3].set_ylabel('Y')
    axs[3].get_xaxis().set_visible(False)
    axs[4].hist(y, bins=20, color='blue', alpha=0.7)
    axs[4].get_yaxis().set_visible(False)
    axs[4].get_xaxis().set_visible(False)
    axs[5].scatter(y, z, c=colors, cmap='viridis', alpha=0.7, marker='.')
    axs[5].get_yaxis().set_visible(False)

    axs[6].scatter(z, x, c=colors, cmap='viridis', alpha=0.7, marker='.')
    axs[6].set_ylabel('Z')
    axs[7].scatter(z, y, c=colors, cmap='viridis', alpha=0.7, marker='.')
    axs[7].get_yaxis().set_visible(False)
    axs[8].hist(z, bins=20, color='blue', alpha=0.7)
    axs[8].get_yaxis().set_visible(False)
    axs[8].get_xaxis().set_visible(False)
        
    plt.tight_layout()
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=1, vmax=len(data)))
    sm._A = []
    cbar = plt.colorbar(sm, ax=axs, orientation='vertical', pad=0.1)
    cbar.set_label('Row number')
    cbar.set_ticks([1, len(data)])
    cbar.set_ticklabels(['1', str(len(data))])
    cbar.ax.yaxis.set_ticks_position('right')
    cbar.ax.yaxis.set_label_position('right')

    plt.show()
    return fig, axs

def PCA_1D(data, hist=True):
    """
    Uses Principal Component Analysis (PCA) to project the data to the first principal component, and plot the data in one dimension using the
    same color scale for row numbers as in the trellis function.
    Note that this function also centers the data before applying PCA.

    Inputs:
    - data: pandas DataFrame with 3 columns
    - hist: boolean, if True, plot the histogram of the data

    Returns:
    - data_pca: the transformed data
    """
    # Center the data
    centered_data = data - data.mean()

    # Perform PCA
    pca = PCA(n_components=1)
    data_pca = pca.fit_transform(centered_data)

    # Plot the data
    colors = np.arange(1, len(data)+1)
    plt.scatter(data_pca, np.zeros_like(data_pca), c=colors, cmap='viridis', alpha=0.7, marker='.')
    plt.yticks([])
    plt.colorbar(label='Row number')
    plt.show()

    # Plot histogram
    if hist:
        plt.hist(data_pca, bins=20, color='blue', alpha=0.7)
        plt.yscale('log')
        plt.ylabel('Frequency')
        plt.xlabel('First principal component')
        plt.gca().yaxis.set_major_formatter(ScalarFormatter())
        plt.ticklabel_format(useOffset=False)
        plt.show()

    return data_pca

def PCA_2D(df):
    """
    M   akes two two-dimensional plots of the data:
    - One plot with the data projected to the (plane defined by the) first and second PCA components,
    - One plot with the data projected to the (plane defined by the) second and third PCA components.
    The color of the points will be the row number.

    Inputs:
    - df: pandas DataFrame with 3 columns, no headers

    Returns:
    - figs: array of 2 figure objects
    - axs: array of 2 axes objects
    """
    # Center the data
    centered_data = df - df.mean()

    # Perform PCA
    pca = PCA(n_components=3)
    data_pca = pca.fit_transform(centered_data)

    # Plot the data
    colors = np.arange(1, len(df)+1)

    figs, axs = [], []
    for i in range(2):
        fig, ax = plt.subplots(figsize=(6, 6))
        axs.append(ax)
        figs.append(fig)
        if i == 0:
            scatter = ax.scatter(data_pca[:, 0], data_pca[:, 1], c=colors, cmap='viridis', alpha=0.7, marker='.')
            ax.set_xlabel('First principal component')
            ax.set_ylabel('Second principal component')
        else:
            scatter = ax.scatter(data_pca[:, 1], data_pca[:, 2], c=colors, cmap='viridis', alpha=0.7, marker='.')
            ax.set_xlabel('Second principal component')
            ax.set_ylabel('Third principal component')
        plt.colorbar(scatter, label='Row number', ax=ax)

    plt.show()
    return figs, axs

def nMDS_plot(df):
    """
    Makes a two-dimensional plot of the data using non-metric multidimensional scaling (nMDS).
    The color of the points will be the row number.

    Inputs:
    - df: pandas DataFrame with 3 columns, no headers

    Returns:
    - fig: figure object
    - ax: axes object
    """
    # Center the data
    centered_data = df - df.mean()

    # Perform nMDS
    nMDS = MDS(n_components=2, metric=False)
    data_nMDS = nMDS.fit_transform(centered_data)

    # Plot the data
    colors = np.arange(1, len(df)+1)

    fig, ax = plt.subplots(figsize=(6, 6))
    scatter = ax.scatter(data_nMDS[:, 0], data_nMDS[:, 1], c=colors, cmap='viridis', alpha=0.7, marker='.')
    ax.set_xlabel('First dimension')
    ax.set_ylabel('Second dimension')
    plt.colorbar(scatter, label='Row number', ax=ax)

    plt.show()
    return fig, ax

def isomap_plot(df, k=7):
    """
    Uses ISOMAP to embed the data into one or two dimensions and plots the data.
    Neighbour parameter k means that for i and j to be neighbours, they must be among the k closest points to each other.

    Inputs:
    - df: pandas DataFrame with 3 columns, no headers
    - k: integer, number of neighbours to consider (default 7)

    Returns:
    - fig: figure object
    - ax: axes object
    """
    # Center the data
    centered_data = df - df.mean()

    # Perform ISOMAP
    isomap = Isomap(n_components=2, n_neighbors=k)
    data_isomap = isomap.fit_transform(centered_data)

    # Plot the data
    colors = np.arange(1, len(df)+1)

    fig, ax = plt.subplots(figsize=(6, 6))
    scatter = ax.scatter(data_isomap[:, 0], data_isomap[:, 1], c=colors, cmap='viridis', alpha=0.7, marker='.')
    ax.set_xlabel('First dimension')
    ax.set_ylabel('Second dimension')
    plt.colorbar(scatter, label='Row number', ax=ax)

    plt.show()
    return fig, ax



if __name__ == '__main__':
    folder = 'data'
    csvfile = 'Mystery'
    df = pd.read_csv(f'{folder}/{csvfile}.csv', header=None)
    trellis(df)
    PCA_1D(df, hist=True)
    PCA_2D(df)
    nMDS_plot(df)
    isomap_plot(df)
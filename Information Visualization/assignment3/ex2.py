import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import MDS
from scipy.spatial.distance import pdist, squareform

def data_handling(df, highlight_list):
    """
    Drops the first row of the DataFrame and centers the data.

    Inputs:
    - df: pandas DataFrame, first row are headers, first columns is not numeric.
    - highlight_list: list of strings, names of the rows to highlight in the plot.

    Returns:
    - centered_data: pandas DataFrame, centered data
    - rows_to_highlight: list of integers, row numbers to highlight
    """
    # Data drops and centering
    df = df.drop([0])
    data = df.drop(columns=['Area','Total'])
    centered_data = data - data.mean()

    # Highlighting to row number
    rows_to_highlight = [df.index[df['Area'] == highlight].tolist()[0] for highlight in highlight_list]

    return centered_data, rows_to_highlight


def mmds_map(df, highlight_list, color, highlight_color):
    """
    Computes and plots both Metric Multidimensional Scaling (MMDS).
    The function will try to drop the columns named 'Area' and 'Total' first.

    Inputs:
    - df: pandas DataFrame, first row are headers, first columns is not numeric.
    - highlight_list: list of strings, names of the rows to highlight in the plot.
    - color: string, color of the points
    - highlight_color: string, color of the highlighted points

    Returns:
    - fig: figure object
    - ax: axis object
    """
    centered_data, rows_to_highlight = data_handling(df, highlight_list)

    # Perform MMDS
    mmds = MDS(n_components=2, metric=True, dissimilarity='euclidean')
    data_mmds = mmds.fit_transform(centered_data)
    min_x = min(data_mmds[:, 0])
    print('Area with the minimum x value: ' + df['Area'][np.where(data_mmds[:, 0] == min_x)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_mmds[:, 0] == min_x)[0][0]]))
    rows_to_highlight.append(np.where(data_mmds[:, 0] == min_x)[0][0])
    highlight_list.append(df['Area'][np.where(data_mmds[:, 0] == min_x)[0][0]])
    max_x = max(data_mmds[:, 0])
    print('Area with the maximum x value: ' + df['Area'][np.where(data_mmds[:, 0] == max_x)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_mmds[:, 0] == max_x)[0][0]]))
    rows_to_highlight.append(np.where(data_mmds[:, 0] == max_x)[0][0])
    highlight_list.append(df['Area'][np.where(data_mmds[:, 0] == max_x)[0][0]])
    min_y = min(data_mmds[:, 1])
    print('Area with the minimum y value: ' + df['Area'][np.where(data_mmds[:, 1] == min_y)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_mmds[:, 1] == min_y)[0][0]]))
    rows_to_highlight.append(np.where(data_mmds[:, 1] == min_y)[0][0])
    highlight_list.append(df['Area'][np.where(data_mmds[:, 1] == min_y)[0][0]])
    max_y = max(data_mmds[:, 1])
    print('Area with the maximum y value: ' + df['Area'][np.where(data_mmds[:, 1] == max_y)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_mmds[:, 1] == max_y)[0][0]]))
    rows_to_highlight.append(np.where(data_mmds[:, 1] == max_y)[0][0])
    highlight_list.append(df['Area'][np.where(data_mmds[:, 1] == max_y)[0][0]])

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))
      
    # Scatter plot for all points
    scatter = ax.scatter(data_mmds[:, 0], data_mmds[:, 1], c=color, alpha=0.7, marker='.')
    
    # Scatter plot for highlighted points
    highlight_scatter = ax.scatter(data_mmds[rows_to_highlight, 0], data_mmds[rows_to_highlight, 1], c=highlight_color, alpha=0.7, marker='x')
    
    ax.set_xlabel('First dimension')
    ax.set_ylabel('Second dimension')
            
    # Highlighting
    order = 0
    for row in rows_to_highlight:
        ax.text(data_mmds[row, 0], data_mmds[row, 1], highlight_list[order], fontsize=8, ha='right', va='top', color=highlight_color)
        order += 1

    plt.show()

    # Sheppard plot
    input_distances = pdist(centered_data, 'euclidean')
    output_distances = pdist(data_mmds, 'euclidean')
    plt.figure()
    plt.scatter(input_distances, output_distances, edgecolors='b', facecolors='none')
    plt.plot([0, max(input_distances)], [0, max(output_distances)], 'k--')
    plt.xlabel('Input distances')
    plt.ylabel('Output distances')
    plt.title('Shepard Plot')
    plt.legend(['Data points', 'Ideal Line'])
    plt.show()

    return fig, ax

def sammon_map(df, highlight_list, color, highlight_color):
    """
    Computes and plots Sammon Mapping.
    The function will try to drop the columns named 'Area' and 'Total' first.

    Inputs:
    - df: pandas DataFrame, first row are headers, first columns is not numeric.
    - highlight_list: list of strings, names of the rows to highlight in the plot.
    - color: string, color of the points
    - highlight_color: string, color of the highlighted points

    Returns:
    - fig: figure object
    - ax: axis object
    """

    centered_data, rows_to_highlight = data_handling(df, highlight_list)

    # Perform Sammon Mapping
    sammon = MDS(n_components=2, metric=True, dissimilarity='euclidean', n_init=1, max_iter=300, eps=1e-3)
    data_sammon = sammon.fit_transform(centered_data)

    # Plot the data
    min_x = min(data_sammon[:, 0])
    print('Area with the minimum x value: ' + df['Area'][np.where(data_sammon[:, 0] == min_x)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_sammon[:, 0] == min_x)[0][0]]))
    rows_to_highlight.append(np.where(data_sammon[:, 0] == min_x)[0][0])
    highlight_list.append(df['Area'][np.where(data_sammon[:, 0] == min_x)[0][0]])
    max_x = max(data_sammon[:, 0])
    print('Area with the maximum x value: ' + df['Area'][np.where(data_sammon[:, 0] == max_x)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_sammon[:, 0] == max_x)[0][0]]))
    rows_to_highlight.append(np.where(data_sammon[:, 0] == max_x)[0][0])
    highlight_list.append(df['Area'][np.where(data_sammon[:, 0] == max_x)[0][0]])
    min_y = min(data_sammon[:, 1])
    print('Area with the minimum y value: ' + df['Area'][np.where(data_sammon[:, 1] == min_y)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_sammon[:, 1] == min_y)[0][0]]))
    rows_to_highlight.append(np.where(data_sammon[:, 1] == min_y)[0][0])
    highlight_list.append(df['Area'][np.where(data_sammon[:, 1] == min_y)[0][0]])
    max_y = max(data_sammon[:, 1])
    print('Area with the maximum y value: ' + df['Area'][np.where(data_sammon[:, 1] == max_y)[0][0]] + ', Total population: ' + str(df['Total'][np.where(data_sammon[:, 1] == max_y)[0][0]]))
    rows_to_highlight.append(np.where(data_sammon[:, 1] == max_y)[0][0])
    highlight_list.append(df['Area'][np.where(data_sammon[:, 1] == max_y)[0][0]])

    # Plot the data
    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot for all points
    scatter = ax.scatter(data_sammon[:, 0], data_sammon[:, 1], c=color, alpha=0.7, marker='.')
    
    # Scatter plot for highlighted points
    highlight_scatter = ax.scatter(data_sammon[rows_to_highlight, 0], data_sammon[rows_to_highlight, 1], c=highlight_color, alpha=0.7, marker='x')
    
    ax.set_xlabel('First dimension')
    ax.set_ylabel('Second dimension')
            
    # Highlighting
    order = 0
    for row in rows_to_highlight:
        ax.text(data_sammon[row, 0], data_sammon[row, 1], highlight_list[order], fontsize=8, ha='right', va='top', color=highlight_color)
        order += 1

    plt.show()

    # Sheppard plot
    input_distances = pdist(centered_data, 'euclidean')
    output_distances = pdist(data_sammon, 'euclidean')
    plt.figure()
    plt.scatter(input_distances, output_distances, edgecolors='b', facecolors='none')
    plt.plot([0, max(input_distances)], [0, max(output_distances)], 'k--')
    plt.xlabel('Input distances')
    plt.ylabel('Output distances')
    plt.title('Shepard Plot')
    plt.legend(['Data points', 'Ideal Line'])
    plt.show()

    return fig, ax

if __name__ == '__main__':
    folder = 'data'
    csvfile = 'population_data'
    city_highlights = ['Helsinki', 'Espoo', 'Vantaa', 'Tampere', 'Rovaniemi', 'Turku', 'Oulu', 'Joensuu', 'Kuopio']
    color = 'dimgray'
    highlight_color = 'red'
    df = pd.read_csv(f'{folder}/{csvfile}.csv', delimiter=';')
    mmds_map(df, city_highlights, color, highlight_color)
    sammon_map(df, city_highlights, color, highlight_color)

    
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as mpatches 

def plot_graph(df, type='spring',labels=True):
    """
    Plots the given graph, according to style type.

    Inputs:
    - df: pandas DataFrame, containing the graph.
    - type: string, style of the plot. Default is 'spring'. Valid types: 'spring', 'kamada', 'circular', 'random', 'shell', 'spectral', 'planar'.
    - labels: boolean, whether to show labels or not. Default is True.

    Outputs:
    - None
    """
    # Create the graph
    G = nx.from_pandas_edgelist(df, source=0, target=1)

    # Plot the graph
    if type == 'spring':
        pos = nx.spring_layout(G, seed=42)
    elif type == 'kamada':
        pos = nx.kamada_kawai_layout(G)
    elif type == 'circular':
        pos = nx.circular_layout(G)
    elif type == 'random':
        pos = nx.random_layout(G)
    elif type == 'shell':
        pos = nx.shell_layout(G)
    elif type == 'spectral':
        pos = nx.spectral_layout(G)
    elif type == 'planar':
        pos = nx.planar_layout(G)
    else:
        raise ValueError('Invalid type.')
    # Node Coloring
    node_colors = []
    for node in G.nodes():
        if G.degree(node) > 3:
            node_colors.append('red')
        elif G.degree(node) == 3:
            node_colors.append('orange')
        elif G.degree(node) > 1:
            node_colors.append('purple')
        else:
            node_colors.append('blue')
    
    nx.draw(G, pos, with_labels=labels, node_size=10, node_color=node_colors, edge_color='black', width=0.5)
    pop_a = mpatches.Patch(color='red', label='More than 3 connections') 
    pop_b = mpatches.Patch(color='orange', label='3 connections') 
    pop_c = mpatches.Patch(color='purple', label='2 connections')
    pop_d = mpatches.Patch(color='blue', label='End of transmission chain')
    plt.legend(handles=[pop_a, pop_b, pop_c, pop_d], loc = 'lower right') 
    plt.show()


if __name__ == '__main__':
    folder = 'data/graphs/'
    #file = 'drugspider_caffeine.adj'
    #file = 'drugspider_chloralhydrate.adj'
    file = 'hiv.adj'
    #file = 'railways_finland.adj'
    #file = 'kindergarden.adj'
    df = pd.read_csv(folder + file, sep=' ', header=None)
    plot_graph(df, 'kamada', labels=False)
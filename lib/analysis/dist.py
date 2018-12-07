import numpy as np
import graph_tool.all as gt


def degree(g: gt.Graph, deg='total') -> np.array:
    '''
    Returns array of degree frequencies.
    '''
    degrees = g.degree_property_map(deg=deg).a
    counts = np.bincount(degrees)[1:]
    return counts / np.sum(counts)

def excess_degree(g: gt.Graph, deg='total') -> np.array:
    '''
    Returns array of excess degree frequencies.
    '''
    def compute_excess(k, degrees):
        edges = g.get_edges()[:, :2]
        # find all nodes with degree k+1
        nodes = g.vp['id'].a[degrees == k + 1]
        # find all edges that contain those nodes
        associated_edges = np.isin(edges, nodes)
        # return the number of edges found
        return np.sum(associated_edges)

    degrees = g.degree_property_map(deg=deg).a
    k = np.arange(1, degrees.max())
    counts = compute_excess(k,degrees)
    return counts / np.sum(counts)

def power(g: gt.Graph, a_hat, k_min=1):
    k = np.arange(1, degree(g).max())
    return (a_hat - 1) / k_min * np.power(k / k_min, -a_hat)


if __name__ == '__main__':
    pass

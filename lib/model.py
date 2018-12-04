import numpy as np
import graph_tool.all as gt

from numpy.random import choice
from graph_tool import stats


def erdos_renyi(n, m, directed=False) -> gt.Graph:
    '''
    generates and returns a new Erdos-Renyi graph with N vertices and M edges
    '''
    # create new graph and add N edges
    g = gt.Graph(directed=directed); g.add_vertex(n)
    # add M edges
    g.add_edge_list(np.random.choice(g.get_vertices(), size=(m, 2)))
    # randomly rewire the edges with Erdos-Renyi model
    gt.random_rewire(g, model='erdos')
    return g

def small_world(n, m) -> gt.Graph:
    '''
    generates and returns a new Small World graph with N vertices and M edges
    '''
    # start with circular graph
    g = gt.circular_graph(n, 2)
    
    # generate complete graph to sample edges from
    complete = gt.complete_graph(n)
    complete_m = complete.num_edges()

    while g.num_edges() != m:
        # sample enough edges to reach the desired number of edges
        idx = choice(np.arange(complete_m), size=(m - g.num_edges()))
        sample = complete.get_edges()[idx, :2]
        # add sampled edges
        g.add_edge_list(sample)
        stats.remove_parallel_edges(g)
    
    return g

def barabasi_albert(n, seed=erdos_renyi(5, 3), directed=False):
    return gt.price_network(n, seed_graph=seed, directed=False)

if __name__ == '__main__':
    pass
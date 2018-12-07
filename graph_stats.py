import graph_tool.all as gt
import numpy as np
from lib.analysis import clustering
from lib.analysis import dist
from lib.analysis import model
from lib.analysis import power

    # Input: gt.Graph
    # Returns comma-separated values:
    #     Number of edges
    #     Number of vertices
    #     Average clustering coefficient
    #     Average degree
    #     Average excess degree
    #     Average path length
    #     Size of largest connected component
    #     Number of connected components
def stats(g: gt.Graph):
    
    # Number of edges
    num_edges = g.num_edges()
    
    # Number of vertices
    num_vertices = g.num_vertices()
    
    # Clustering coefficient
    clustering_coefficient = clustering.coefficient(g)
    
    # Average degree
    avg_degree = np.mean(dist.degree(g))
    
    # Average excess degree
    excess_degree = np.mean(dist.excess_degree(g))
    
    # Average path length
    all_sd = gt.shortest_distance(g)
    avg_path = np.mean(list(all_sd))
    
    # Size of largest connected component
    l = gt.label_largest_component(g)
    u = gt.GraphView(g, vfilt=l)
    lcc = u.num_vertices()
    
    # Number of connected components
    labeled = gt.label_components(g)
    num_cc = max(np.unique(labeled[0].a))
    
    return("num_edges: %s" % num_edges, 
          "num+vertices: %s" % num_vertices, 
          "clustering_coefficient: %s" % clustering_coefficient,
          "avg_degree: %s" % avg_degree,
          "excess_degree: %s" % excess_degree,
          "avg_path: %s" % avg_path,
          "lcc: %s" % lcc,
          "num_cc: %s" % num_cc)
    

if __name__ == "__main__":
    pass
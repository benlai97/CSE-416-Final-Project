import graph_tool.all as gt
import numpy as np
from functools import reduce
from .clustering import coefficient as clustering_coefficient
from .dist import degree, excess_degree

def generate_party_property(g: gt.Graph, label: str):
    partyMap = {}
    out = []
    parties = [party for party in g.vertex_properties[label]]
    d = dict([(y,x+1) for x,y in enumerate(sorted(set(parties)))])
    for party in parties:
        out.append(d[party])
    party_id = g.new_vertex_property("int32_t")
    for i in range(len(out)):
        party_id[g.vertex(i)] = out[i]
    g.vertex_properties['party_id'] = party_id

def assortativity(g: gt.Graph, attribute_map: gt.PropertyMap) -> np.float:
    coeff, _ = gt.assortativity(g, attribute_map)
    return coeff

def assortativity_summary(g: gt.Graph, label: str):
    '''Returns a summary of graph assortivity on given label'''
    coeff = assortativity(g, g.vertex_properties[label])
    data = {
    'Assortivity on: ' + label: coeff,
    }
    return Summary(data)  

class Summary:
    def __init__(self, data: dict):
        self.data = data

    def __str__(self):
        return self.as_csv()
    
    def __repr__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.data.items()])

    def as_csv(self):
        return ','.join(map(str, self.data.values()))

    def get_headers(self):
        return ','.join(self.data.keys())
    


def num_components(g: gt.Graph):
    # Number of connected components
    cc, hist = gt.label_components(g)
    num_cc = np.sum(hist > 0)
    components = [gt.GraphView(g, vfilt=np.equal(cc.a, i)) for i in range(num_cc)]
    return num_cc, components


def average_distance(g: gt.Graph):
    nc, components = num_components(g)
    sums, counts = [], []

    for component in components:
        if component.num_vertices() > 1:
            ds = np.array(list(gt.shortest_distance(component)))
            count = ds[ds > 0].shape[0] / 2
            sums.append(np.sum(ds) / 2)
            counts.append(count)

    return 0 if nc == g.num_vertices() else sum(sums) / sum(counts)


def summary(g: gt.Graph):
    '''
    Returns a summary of graph statistics with given graph G.

    Statistics:
        Number of edges
        Number of vertices
        Average clustering coefficient
        Average degree
        Average excess degree
        Average path length
        Size of largest connected component
        Number of connected components
    '''
    
    # Number of edges
    num_edges = g.num_edges()
    
    # Number of vertices
    num_vertices = g.num_vertices()
    
    # Clustering coefficient
    clustering_coeff = clustering_coefficient(g)

    # Average degree
    _, avg_degree = degree(g, report_avg=True)
    
    # Average excess degree
    _, avg_excess_degree = excess_degree(g, report_avg=True)
    
    # Size of largest connected component
    l = gt.label_largest_component(g)
    u = gt.GraphView(g, vfilt=l)
    lcc = u.num_vertices()

    # Number of connected components
    num_cc, _ = num_components(g)

    # Average path length
    avg_path = average_distance(g)
    

    data = {
        'Number of Edges': num_edges,
        'Number of Vertices': num_vertices,
        'Clustering Coefficient': clustering_coeff,
        'Average Degree': avg_degree,
        'Average Excess Degree': avg_excess_degree,
        'Average Distance': avg_path,
        'Size of LCC': lcc,
        'Number of CC': num_cc
    }
    
    return Summary(data)    


if __name__ == "__main__":
    pass

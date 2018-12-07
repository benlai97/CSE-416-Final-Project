import graph_tool.all as gt
import os 
from functools import reduce
from re import search

def combine_graphs(path):
    data = os.listdir(path)
    graphs = [gt.load_graph(path + x) for x in data]
    graph = reduce(gt.graph_union, graphs)
    graph.set_directed(False)
    gt.remove_parallel_edges(graph)
    file_name = search(r'/(\w+)/?$', path).group(1)
    graph.save(path + f'{file_name}.graphml')
    
def load_graphs(path):
    data = os.listdir(path)
    graphs = [gt.load_graph(path + x) for x in data]

if __name__ == '__main__':
    from sys import argv
    _, path = argv
    
    print(f'Combining graphs @ {path}')
    combine_graphs(path)
    
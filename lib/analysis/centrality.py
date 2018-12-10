import graph_tool.all as gt
import numpy as np

def betweenness(g: gt.Graph, scale=None) -> (gt.PropertyMap, gt.PropertyMap):
    '''returns both vertex and edge betweeness'''
    vertex, edge = gt.betweenness(g, norm=True)
    if scale:
        vertex = g.new_vp('float', vertex.a * scale)
        edge = g.new_ep('float', edge.a * scale)
    return vertex, edge

def closeness(g: gt.Graph, scale=None) -> gt.PropertyMap:
    '''returns vertex closeness'''
    vertex = gt.closeness(g, norm=True)
    if scale:
        vertex = g.new_vp('float', vertex.a * scale)
    return vertex

def eigenvector(g: gt.Graph, scale=None) -> (np.float64, gt.PropertyMap):
    '''returns eigenvector and largest eigvenvalue'''
    value, vector = gt.eigenvector(g)
    if scale:
        value *= scale
        vector = g.new_vp('float', vector.a * scale)
    return value, vector

if __name__ == '__main__':
    pass


import graph_tool.all as gt
import numpy as np

def betweeness(g: gt.Graph) -> (gt.PropertyMap, gt.PropertyMap):
    '''returns both vertex and edge betweeness'''
    vertex, edge = gt.betweeness(g, norm=True)
    return vertex, edge

def closeness(g: gt.Graph) -> gt.PropertyMap:
    '''returns vertex closeness'''
    vertex = gt.closeness(g, norm=True)
    return vertex

def eigenvector(g: gt.Graph) -> (np.float64, gt.PropertyMap):
    '''returns eigenvector and largest eigvenvalue'''
    value, vector = gt.eigenvector(g)
    return value, vector

if __name__ == '__main__':
    pass


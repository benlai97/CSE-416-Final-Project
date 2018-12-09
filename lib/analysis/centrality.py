import graph_tool.all as gt


def betweenness(g: gt.Graph) -> (gt.PropertyMap, gt.PropertyMap):
    '''returns both vertex and edge betweenness'''
    vertex, edge = gt.betweenness(g, norm=True)
    return vertex, edge


if __name__ == '__main__':
    pass

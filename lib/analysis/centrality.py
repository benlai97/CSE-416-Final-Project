import graph_tool.all as gt


def betweeness(g: gt.Graph) -> (gt.PropertyMap, gt.PropertyMap):
    '''returns both vertex and edge betweeness'''
    vertex, edge = gt.betweeness(g, norm=True)
    return vertex, edge


if __name__ == '__main__':
    pass

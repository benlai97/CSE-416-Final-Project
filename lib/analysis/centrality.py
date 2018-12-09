import graph_tool.all as gt


def betweeness(g: gt.Graph) -> (gt.PropertyMap, gt.PropertyMap):
    '''returns both vertex and edge betweeness'''
    return gt.betweeness(g, norm=True)


if __name__ == '__main__':
    pass

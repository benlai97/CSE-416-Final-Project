import numpy as np
import graph_tool.all as gt


def coefficient(g: gt.Graph) -> np.float64:
    return gt.local_clustering(g).a.mean()

if __name__ == '__main__':
    pass
import numpy as np
import graph_tool.all as gt

from scipy.linalg import eigh
from scipy.sparse.linalg import eigs


def coefficient(g: gt.Graph) -> np.float64:
    '''returns the average clustering coefficient for a graph'''
    cs = gt.local_clustering(g)
    C, _ = gt.vertex_average(g, cs)
    return C

def modularity(g: gt.Graph, partitioning: gt.PropertyMap) -> np.float64:
    '''returns the modularity score for a given partitioning of graph G'''
    return gt.modularity(g, partitioning)

def betweenness_based(g, k=2):
    '''
    1. The betweenness of all existing edges in the network is calculated first.
    2. The edge with the highest betweenness is removed.
    3. The betweenness of all edges affected by the removal is recalculated.
    4. Steps 2 and 3 are repeated until no edges remain.
    '''
    def get_nc(g):
        '''returns the number of connected components'''
        _, hist = gt.label_components(g)
        return sum(hist > 0)
    
    # make a working copy of the graph
    h = g.copy()
    
    while get_nc(h) < k:
        # compute edge betweenesses
        _, ebs = gt.betweenness(h)
        # find highest betweenness edge(s)
        mb = np.argmax(ebs.a)
        mbs = gt.find_edge(h, ebs, ebs.a[mb])
        # remove it/them
        for edge in mbs: h.remove_edge(edge)

    # return the a Vertex PropertyMap of the partition assignments
    return g.new_vp('int', gt.label_components(h)[0].a)

def _modularity_maximization(g: gt.Graph) -> (gt.Graph, gt.Graph):
    '''
    returns the modularity maximizing partitioning given a graph G
    '''
    N = g.num_vertices()
    # compute parent modularity matrix
    B = gt.modularity_matrix(g)
    # find leading eigenvector u of B
    vals, vecs = eigs(B, (6 if N > 7 else N - 2)) # NOTE: will not work if N < 7
    u = vecs[:, np.argmax(vals)] < 0
    # divide nodes into two partitions and add to partition map
    return gt.GraphView(g, vfilt=u), gt.GraphView(g, vfilt=~u)    

def _spectral(g: gt.Graph, k=2) -> (gt.Graph, gt.Graph):
    '''
    returns a two-way spectral partitioning of a graph G
    
    1. Build Laplacian
    2. Find the eigenvector corresponding to the second smallest eigenvalue
    3. sort the choosen eigenvector and split positive negative (or by median)
    '''
    # build laplacian
    L = gt.laplacian(g).todense()
    # decompose on the second smallest value
    vals, vecs = eigh(L)
    u = vecs[:, np.argsort(vals)[1]]
    part = u > np.median(u)
    # divide nodes into two partitions and add to partition map
    return gt.GraphView(g, vfilt=part), gt.GraphView(g, vfilt=~part)

def cluster(g, method='modularity', k=2) -> gt.PropertyMap:
    '''
    performs community detection using a 2-way splitting METHOD
    and returns K communities.

    Has two methods:
        (1) modularity
        (2) spectral
    
    1. compute the necessary depth to find K clusterings and then compute the
       maximal partitionings at that level using METHOD.
    2. build each up all possible combinations of partitionings with K clusters
       and return the one with the largest modularity score.
    '''
    # current cluster number
    i = 0
    
    def collect(clusters: [gt.GraphView]):
        '''
        joins a list of clusters into a single property map
        indicating node cluster.
        '''
        part = np.zeros(g.num_vertices())
        
        for cluster in clusters:
            nonlocal i
            nodes = cluster.get_vertices()
            part[nodes] = i
            i += 1
        
        return g.new_vp('int', part)

    def combo(d):
        '''returns every combination of range [0, 2^d]'''
        mesh = np.meshgrid(*[np.arange(2 ** (d-1)) for _ in range(2 ** (d-1))])
        return np.array(mesh).T.reshape(-1, 2 ** (d-1))

    if method == 'modularity':
        partitioner = _modularity_maximization
    elif method == 'spectral':
        partitioner = _spectral
    else:
        raise ValueError(f'Not a valid method (given {method})')
    
    # compute the necessary depth: ceil(log2 k)
    d = np.int64(np.ceil(np.log2(k)))
    # prepare storage for partitionings at each level
    partition_map = {level: [] for level in range(d+1)}
    partition_map[0] = [g]
    # compute the modularity maximizing partitionings at that level
    for level in range(1, d+1):
        for parent in partition_map[level-1]:
            # compute maximal child graphs
            left, right = partitioner(parent)
            # divide nodes into two partitions and add to partition map
            partition_map[level] += [left, right]

    # if K is exactly 2^d then we are done
    if k == (2 ** d):
        return collect(partition_map[d])
    
    # otherwise, we need to build valid partitionings of K clusters
    number_needed_from_prev = 2 ** d - k
    # make all combinations of indices
    ics = combo(d)
    clusters = {}
    qs = np.zeros(ics.shape[0])
    # evaluate modularity of all possible partitionings
    for t, part in enumerate(ics):
        # get clusters from level d-1
        i_from_prev = part[:number_needed_from_prev]
        from_prev = [partition_map[d-1][i] for i in i_from_prev]
        # get indices of clusters from level d
        i_from_d = part[number_needed_from_prev:]
        from_d = [c for i in i_from_d for c in partition_map[d][2*i:2*i+1]]
        # combine clusterings
        c = collect(from_prev + from_d)
        q = gt.modularity(g, c)
        # store results
        clusters[q] = c
        qs[t] = q
        
    return clusters[np.max(qs)]


if __name__ == '__main__':
    pass

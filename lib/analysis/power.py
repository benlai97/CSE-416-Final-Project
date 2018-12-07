import numpy as np
import graph_tool.all as gt

from scipy import sparse
from scipy.linalg import lstsq
from .dist import degree

def fit_power(g: gt.Graph, method='ccdf', k_min=1):
    pdf = degree(g)
    k = np.arange(pdf.shape[0]) + 1

    if method == 'pdf':
        df = pdf
    elif method == 'ccdf':
        df = np.triu(np.tile(pdf,(pdf.shape[0], 1))).sum(axis=1) - pdf
    else:
        raise ValueError(f'METHOD must be either `pdf` or `ccdf` (given: {method}')

    X = np.log(k[df != 0] / k_min)[:, np.newaxis] ** [0, 1]
    y = np.log(df[df != 0])

    w, _, _, _ = lstsq(X, y)
    return -w[1] if method == 'pdf' else -w[1] + 1

if __name__ == '__main__':
    pass

import numpy as np
import mpmath as mp

from .load_graph import max_degree

def get_emb_par(G, k, eps, weighted):
    """
    Compute the tau for a required precision, i.e:
    If you want a worst-case distortion of at most (1 + epsilon) this function
    computes the appropiate scaling factor tau.

    Input:
        * G: NetworkX DiGraph object. The graph to compute the tau for.
        * k: Int.
        * eps: Float. Epsilon that states the required precision.
        * weighted: Boolean. Whether or not G is a weighted tree.

    Output:
        * Float. The scaling factor tau.
    """
    n       = G.order()
    degrees = G.degree()
    d_max   = max([cd[1] for cd in dict(degrees).items()])

    (nu, tau) = (0, 0)

    beta    = mp.pi/(1.2*d_max)
    v       = -2*k*mp.log(mp.tan(beta/2))
    m       = len(G.edges())

    if weighted:
        w = float('Inf')
        for edge in G.edges()(data=True):
            ew = edge[3]["weight"]
            w  = ew if ew < w  else w
        if w == float('Inf'):
            w = 1
    else:
        w = 1

    _, d_max     = max_degree(G)
    alpha        = 2*mp.pi/(d_max)-2*beta
    _len_        = -2*k*mp.log(mp.tan(alpha/2))
    nu           = _len_/w if (_len_/w > nu) else nu
    tau          = ((1+eps)/eps*v)/w if (1+eps)/eps*v > w*nu else nu

    return tau

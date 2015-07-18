from Graph2 import graph
from unionfind import UnionFind
from numpy import argsort

class MSPTree:
  def __init__(graph):
    A = {}
    N = len(graph.vertices)
    uf = UnionFind(N)

    order = numpy.argsort(graph.weights)
    for i in order:
      (u,v) = graph.edges(i)
      if not uf.connected(u,v):
        A.add(u,v)
        uf.union(u,v)
    return A

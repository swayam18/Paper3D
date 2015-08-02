import numpy as np
from numpy import linalg
from numpy import argsort
from numpy import argmin
from unionfind import UnionFind
from random import choice
from utilities import close_enough
import tree

class Graph:
  def __init__(self, triangles):
    self.nodes = []
    self.edges = []
    self.edge_ids = []

    self.l_min = float("inf")
    self.l_max = 0.0

    for i,t in enumerate(triangles):
      v1 = t[0].tolist()
      v2 = t[1].tolist()
      v3 = t[2].tolist()
      n = t[3].tolist()

      node = Node(v1,v2,v3,n)
      node.index = i
      self.nodes.append(node)


      self.l_min = min(self.l_min, min(node.edge_lengths))
      self.l_max = max(self.l_max, max(node.edge_lengths))

    if self.l_min == self.l_max: self.l_max += 0.0001
    self.generate_edges()
    self.defaultHeuristic = lambda edge_length: (self.l_max - edge_length)/(self.l_max - self.l_min)

  def toMSPTree(self, heuristicFn = None):
    if heuristicFn == None:
      heuristicFn = self.defaultHeuristic
    edges = self.mspEdges(heuristicFn)
    treeNodes = [TreeNode(node) for node in self.nodes]

    for edge in edges:
      node_u = treeNodes[edge[0]]
      node_v = treeNodes[edge[1]]

      node_u.children.append(node_v)
      node_v.children.append(node_u)

    #root = treeNodes[choice(choice(edges))]
    root = treeNodes[edges[0][0]]
    return root

  def findPath(self,start_id, end_id):
    frontier = [start_id]
    explored = {}
    explored[start_id] = None
    exp = self.bfs(end_id, frontier, explored)
    path = []
    node_id = end_id
    while exp[node_id] != None:
      path.append((exp[node_id], node_id))
      node_id = exp[node_id]
    path.reverse()
    return path

  def bfs(self, goal_id, frontier,explored):
    node_id = frontier.pop()
    parent_id = explored[node_id]
    if node_id == goal_id:
      return explored
    else:
      node = self.nodes[node_id]
      for child_id in node.children:
        if not child_id in explored:
          explored[child_id] = node_id
          frontier.append(child_id)
      return self.bfs(goal_id, frontier, explored)

  def mspEdges(self, heuristicFn):
    A = []
    N = len(self.nodes)
    uf = UnionFind(N)
    weights = self.generate_weights(heuristicFn)

    order = argsort(weights)
    for i in order:
      (u,v) = self.edges[i]
      if not uf.connected(u,v):
        A.append((u,v))
        uf.union(u,v)
    return A

  def cutEdges(self, paths, heuristicFn=None):
    if heuristicFn == None:
      heuristicFn = self.defaultHeuristic
    weights = self.generate_weights(heuristicFn)

    S = set()
    P = set()
    for path in paths:
      P.add(path)
    C = set()
    edges = {}

    for path in paths:
      for e in path:
        if e not in edges:
          edges[e] = set()
        edges[e].add(path)

    while C != P:
      e_min = None
      e_min_cost = float("inf")
      e_min_paths = set()
      for e in edges.keys():
        i = self.edges.index((min(e),max(e)))
        weight = weights[i]
        l_paths = edges[e] - C
        size = len(l_paths) + 0.000001
        cost = 1.0/size

        if cost < e_min_cost:
          e_min_cost = cost
          e_min = e
          e_min_paths = l_paths
      S.add(e_min)
      C = C.union(e_min_paths)
    return S

  def getMaxMinLenghts(self):
    return (self.l_min, self.l_max)

  def generate_weights(self, heuristicFn):
    weights = []
    for i,(node1,node2) in enumerate(self.edges):
      edge_id = self.edge_ids[i]
      edge = self.nodes[node1].edge_lengths[edge_id]
      weights.append(heuristicFn(edge))
    return weights

  def generate_edges(self):
    for i in xrange(len(self.nodes)):
      for j in xrange(len(self.nodes)):
        if i == j: continue
        edge_id = self.connected(self.nodes[i], self.nodes[j])
        if edge_id != -1:
          self.nodes[i].children.add(j)
          self.nodes[j].children.add(i)
          self.edges.append((i,j))
          self.edge_ids.append(edge_id)
          self.nodes[i].edge_to_nodes[edge_id] = (i,j) if i < j else (j,i)    

  def connected(self, node1, node2):
    for i, node1edge in enumerate(node1.edges):
      for j, node2edge in enumerate(node2.edges):
        if close_enough(node1edge,node2edge) or close_enough(node1edge[::-1],node2edge):
          return i
    return -1

# Every Node is a triangular face
class Node:
  def __init__(self, v1, v2, v3, normal):
    self.index = -1
    self.v1=v1
    self.v2=v2
    self.v3=v3
    self.n = normal

    self.edges = [(v1, v2), (v2, v3), (v3, v1)]
    self.children = set()
    self.edge_to_nodes = [None] * 3
    self.edge_lengths = map(linalg.norm, self.edges)

  def __repr__(self):
    return str(self)

  def __str__(self):
    return "{},{},{}".format(self.v1,self.v2,self.v3)

  def getVertices(self):
    return (self.v1,self.v2,self.v3)

# Only adds parent and child information
class TreeNode:
  def __init__(self,node):
    self.face = node
    self.children = []

  def checkIntersection(self):
    tn = tree.traverse(self,set())
    tn.root = True
    tree.unfold(tn)
    tn.rotateToFlat()
    return tn.checkIntersection()

  def makeArrayRepresentation(self,size):
    array = [-1] * size
    stack = [self]
    explored = set()
    while stack:
      node = stack.pop()
      explored.add(node)
      for child in node.children:
        if child not in explored:
          array[child.face.index] = node.face.index
          stack.append(child)
    return array

  def makeEdgeRepresentation(self):
    out = [] 
    stack = [self]
    explored = set()
    while stack:
      node = stack.pop()
      explored.add(node)
      for child in node.children:
        if child not in explored:
          out.append((node.face.index,child.face.index) if node.face.index < child.face.index else (child.face.index, node.face.index)) 
          stack.append(child)
    return out

def treeLength(msp,explored):
  explored.add(msp)
  u_children = 1
  for child in msp.children:
    if child not in explored:
      u_children += treeLength(child,explored)
  return u_children

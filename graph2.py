from numpy import linalg
from numpy import argsort
from unionfind import UnionFind
from random import choice
import tree

class Graph:
  def __init__(self, triangles):
    self.nodes = []
    self.edges = []
    self.weights = []

    self.l_min = float("inf")
    self.l_max = 0.0

    for t in triangles:
      v1 = t[0].tolist()
      v2 = t[1].tolist()
      v3 = t[2].tolist()
      n = t[3].tolist()

      node = Node(v1,v2,v3,n)
      self.nodes.append(node)

      self.l_min = min(self.l_min, min(node.edge_lengths))
      self.l_max = max(self.l_max, max(node.edge_lengths))

    if self.l_min == self.l_max: self.l_max += 0.0001
    self.generate_edges()

  def toMSPTree(self):
    edges = self.mspEdges()
    treeNodes = [TreeNode(node) for node in self.nodes]

    for edge in edges:
      node_u = treeNodes[edge[0]]
      node_v = treeNodes[edge[1]]

      node_u.children.append(node_v)
      node_v.children.append(node_u)


    #root = treeNodes[choice(choice(edges))]
    root = treeNodes[edges[0][0]]
    return root


  def mspEdges(self):
    A = []
    N = len(self.nodes)
    uf = UnionFind(N)

    order = argsort(self.weights)
    for i in order:
      (u,v) = self.edges[i]
      if not uf.connected(u,v):
        A.append((u,v))
        uf.union(u,v)
    return A

  def generate_edges(self):
      for i in xrange(len(self.nodes)):
        for j in xrange(i,len(self.nodes)):
          if i == j: continue
          weight = self.connected(self.nodes[i], self.nodes[j])
          if weight != float("inf"):
            self.nodes[i].children.add(j)
            self.nodes[j].children.add(i)
            self.edges.append((i,j))
            self.weights.append(weight)

  def connected(self, node1, node2):
    for i, node1edge in enumerate(node1.edges):
      for j, node2edge in enumerate(node2.edges):
        if node1edge == node2edge or node1edge[::-1] == node2edge:
          # minimum perimeter heuristic to the edge
          weight = (self.l_max - node1.edge_lengths[i])/(self.l_max - self.l_min)
          return weight
    return float("inf")

  def brute_force(self):
     stack = [0]
     root = None
     parent_node = None 
     explored = set()
     while stack:
         node = self.nodes[stack.pop()]
         explored.add(node)
         treenode = TreeNode(node)
         if root == None:
             root = treenode
             parent_node = treenode
         else: 
             parent_node.children.append(treenode)
         tn = tree.traverse(root)
         unfold(tn)
         tn.rotateToFlat()
         if tn.checkIntersection() == []:
             for child in node.children:
                 if child not in explored:
                     stack.append(child)

      # check for intersection
      # if intersection return false
      # if not call _brute_force as a parent




# Every Node is a triangular face
class Node:
  def __init__(self, v1, v2, v3, normal):
    self.v1=v1
    self.v2=v2
    self.v3=v3
    self.n = normal

    self.edges = [(v1, v2), (v2, v3), (v3, v1)]
    self.children = set()
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


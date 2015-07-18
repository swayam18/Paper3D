import numpy
from stl import mesh
from pprint import pprint


class Reader:
  @staticmethod
  def read(filename):
    my_mesh = mesh.Mesh.from_file(filename)
    triangles = []
    for triangle,normal in zip(my_mesh.points,my_mesh.normals): 
      t = [triangle[0:3], triangle[3:6], triangle[6:9], normal]
      triangles.append(t)
    return triangles




class Graph:
  def __init__(self, triangles):
    self.vertices = []
    self.normals = []
    self.nodes = []

    for t in triangles:
      v1 = t[0].tolist()
      v2 = t[1].tolist()
      v3 = t[2].tolist()
      n = t[3].tolist()

      a1 = self.add_vertex(v1)
      a2 = self.add_vertex(v2)
      a3 = self.add_vertex(v3)
      self.normals.append(n)

      self.nodes.append(GraphNode(a1,a2,a3))

    for node in self.nodes:
      self.generate_edges()

    # check for neighbouring triangles
    for node in self.nodes:
      print node.neighbouring_triangles


  def add_vertex(self, vertex):
    if vertex in self.vertices:
      idx = self.vertices.index(vertex)
    else:
      idx = len(self.vertices)
      self.vertices.append(vertex)

    return idx

  def generate_edges(self):
    nodes = self.nodes[:]
    while(len(nodes) > 1):
      for i in xrange(len(nodes)-1):
        self._generate_edges(nodes[0], nodes[i+1])
      nodes = nodes[1:]



  def _generate_edges(self, node1, node2):
    for i, node1edge in enumerate(node1.edges): 
      for j, node2edge in enumerate(node2.edges):
        if node1edge == node2edge or node1edge[::-1] == node2edge:
          node1.neighbouring_triangles[i] = self.nodes.index(node2)
          node2.neighbouring_triangles[j] = self.nodes.index(node1)

  def generate_dfs_path(self, root_node_idx):
    root = self.nodes[root_node_idx]
    frontier = []
    







class GraphNode:
  def __init__(self, v1_idx, v2_idx, v3_idx):
    self.v1=v1_idx
    self.v2=v2_idx
    self.v3=v3_idx

    self.edges = [(v1_idx, v2_idx), (v2_idx, v3_idx), (v3_idx, v1_idx)]
    self.neighbouring_triangles = [None] * 3

  






triangles = Reader.read("cube.stl")
g = Graph(triangles)



from numpy import linalg

class Graph:
  def __init__(self, triangles):
    self.vertices = []
    self.normals = []
    self.nodes = []
    self.edges = [] # duplicated here for krushkal speed up

    self.l_min = float("inf")
    self.l_max = 0.0

    for t in triangles:
      v1 = t[0].tolist()
      v2 = t[1].tolist()
      v3 = t[2].tolist()
      n = t[3].tolist()

      a1 = self.add_vertex(v1)
      a2 = self.add_vertex(v2)
      a3 = self.add_vertex(v3)
      self.normals.append(n)

      node = GraphNode(a1,a2,a3)
      self.l_min = min(self.l_min, min(node.edge_lengths))
      self.l_max = max(self.l_max, max(node.edge_lengths))

      self.nodes.append(node)

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

          # minimum perimeter heuristic to the edge
          node1.neighbouring_weights[i] = (self.l_max - node1.edge_lengths[i])/(self.l_max - self.l_min)
          node2.neighbouring_weights[j] = node1.neighbouring_weights[i]


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
    self.neighbouring_weights = [0] * 3
    self.edge_lengths = map(linalg.norm, self.edges)

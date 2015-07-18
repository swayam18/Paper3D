import numpy
from graph2 import Graph
from stl import mesh
from pprint import pprint
from copy import copy
from tree import TriangleNode


class Reader:
  @staticmethod
  def read(filename):
    my_mesh = mesh.Mesh.from_file(filename)
    triangles = []
    for triangle,normal in zip(my_mesh.points,my_mesh.normals):
      t = [triangle[0:3], triangle[3:6], triangle[6:9], normal]
      triangles.append(t)
    return triangles

#triangles = Reader.read("stanford_bunny_309_faces.stl")
triangles = Reader.read("cube.stl")
g = Graph(triangles)
msp = g.toMSPTree()

def traverse(node, explored):
  parent = TriangleNode(node.face)
  explored.add(node)
  if len(node.children) == 1 and node.children[0] in explored:
    return parent
  else:
    for child in node.children:
      if child not in explored:
        edges = []
        for v1 in node.face.getVertices():
          for v2 in child.face.getVertices():
            if v1 == v2:
              edges.append(v1)
        assert(len(edges)==2)
        parent.addChildren(traverse(child,explored),edges)
    return parent

def traverse_for_vertices(triangleNode):
  face_vertex = [[ x.tolist() for x in triangleNode.transformed_vertices ]]
  if len(triangleNode.children) == 0:
    return face_vertex
  else:
    for child,edges in triangleNode.children:
      face_vertex.extend(traverse_for_vertices(child))
    return face_vertex

def unfold(triangleNode):
  if len(triangleNode.children) == 0:
    triangleNode.unfold()
  else:
    for child,edges in triangleNode.children:
      unfold(child)
    triangleNode.unfold()

#tn = traverse(msp,set())
#tn.root = True
#v = traverse_for_vertices(tn)
#print reduce(lambda x,y: x+y, v)
#unfold(tn)
#v = traverse_for_vertices(tn)
#print reduce(lambda x,y: x+y, v)


import numpy
from graph2 import Graph
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

triangles = Reader.read("stanford_bunny_309_faces.stl")
g = Graph(triangles)

print g.toMSPTree()

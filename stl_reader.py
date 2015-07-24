import numpy
from graph2 import Graph, TreeNode
from stl import mesh
from pprint import pprint
from copy import copy
import tree
from tree import TriangleNode, parseArrayIntoTree

from solid import *
from solid.utils import *

SEGMENTS = 48

class Reader:
  @staticmethod
  def read(filename):
    my_mesh = mesh.Mesh.from_file(filename)
    triangles = []
    for triangle,normal in zip(my_mesh.points,my_mesh.normals):
      t = [triangle[0:3], triangle[3:6], triangle[6:9], normal]
      triangles.append(t)
    return triangles

triangles = Reader.read("stl/cube.stl")
g = Graph(triangles)
msp = g.toMSPTree()
array = msp.makeArrayRepresentation(len(g.nodes))
print array
tn = parseArrayIntoTree(g.nodes, array)
tn.unfold()
v = tn.getAllChildVertices()

def assembly():
    a = polyhedron(
            points=v,
            triangles=[[x for x in range(y,y+3)] for y in range(0,len(v),3)])
    return a

if __name__ == '__main__':
    a = assembly()
    #a = intersecting()
    scad_render_to_file(a,'test.scad', file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

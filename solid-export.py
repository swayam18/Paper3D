#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
import tree
from numpy import array,cross
from tree import TriangleNode,traverse,traverse_for_vertices,unfold
from stl_reader import Reader
from graph2 import Graph
from utilities import getMatrixArbitraryAxis

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

triangles = Reader.read("stl/icosahedron.stl")
g = Graph(triangles)
msp = g.toMSPTree()
tn = traverse(msp,set())
tn.root = True
#v = traverse_for_vertices(tn)
#print reduce(lambda x,y: x+y, v)
unfold(tn)
up = array([0,0,1])
axis = tree.unitVector(cross(up, tn.normal))
m = getMatrixArbitraryAxis(axis, tree.angleBetween(up,tn.normal))
tn.unfold(m)
v = traverse_for_vertices(tn)
vertices = reduce(lambda x,y: x+y, v)
#print vertices
vertices = [y[:3] for y in vertices ]
#print vertices
def assembly():
    a = polyhedron(
            points=vertices,
            triangles=[[x for x in range(y,y+3)] for y in range(0,len(vertices),3)])
    return rotate(90)(a)

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a,'unfold.scad', file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

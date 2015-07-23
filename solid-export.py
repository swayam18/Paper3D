#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
import tree
import utilities
from numpy import array,cross
from tree import TriangleNode,traverse,traverse_for_vertices,unfold
from stl_reader import Reader
from graph2 import Graph
from utilities import getMatrixArbitraryAxis, findIntersectingTriangles

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

triangles = Reader.read("stl/rhino-quarter.stl")
g = Graph(triangles)
msp = g.toMSPTree()
tn = traverse(msp)
tn.root = True
unfold(tn)
tn.rotateToFlat()
v = traverse_for_vertices(tn)
vertices = reduce(lambda x,y: x+y, v)
#print vertices
vertices = [y[:3] for y in vertices ]
vertices2D = [ [ [round(i,5) for i in y][:2] for y in x] for x in v ]
#print vertices2D
#print tn.getTransformedVertices()[:2]
#print utilities.checkTriangleIntersections(tn.getTransformedVertices2D(), vertices2D)
xs = findIntersectingTriangles(tn, vertices2D)
print len(xs)
print [x.node for x in xs]

def assembly():
    a = polyhedron(
            points=vertices,
            triangles=[[x for x in range(y,y+3)] for y in range(0,len(vertices),3)])
    return a

def intersecting():
    a = polygon(points=xs[0].getTransformedVertices2D())
    for xx in xs[1:]:
        a += polygon(points=xx.getTransformedVertices2D())
    return a

if __name__ == '__main__':
    #a = assembly()
    a = intersecting()
    scad_render_to_file(a,'intersection.scad', file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

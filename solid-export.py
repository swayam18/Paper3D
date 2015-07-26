#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
import tree
import utilities
from numpy import array,cross
from tree import TriangleNode, parseArrayIntoTree
from stl_reader import Reader
from graph2 import Graph,TreeNode,treeLength
from utilities import getMatrixArbitraryAxis
from dxf_writer import DXFWriter

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

triangles = Reader.read("stl/icosahedron.stl")
g = Graph(triangles)
msp = g.toMSPTree()
array_rep = msp.makeArrayRepresentation(len(g.nodes))
print array_rep
print treeLength(msp,set()), "faces"
tn = parseArrayIntoTree(g.nodes, array_rep)
tn.unfold()
v = tn.getAllChildVertices()
v2d = tn.getAllChildVertices2D()

intersects = tn.checkIntersection() # return nodes thats intersect
print len(intersects), "faces that intersects"
#v_i = [ x.getTransformedVertices2D() for x in intersects ]
#v = reduce(lambda x,y: x+y, v_i)

#print [x.node for x in xs]
#print len(xs)

def assembly():
    a = polyhedron(
            points=v,
            triangles=[[x for x in range(y,y+3)] for y in range(0,len(v),3)])
    return a

def intersecting():
    a = polygon(
            points=v2d,
            paths=[[x for x in range(y,y+3)] for y in range(0,len(v),3)])
    return a

if __name__ == '__main__':
    a = assembly()
    #a = intersecting()
    scad_render_to_file(a,'unfold.scad', file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    d = DXFWriter(v2d) 
    d.generate_file()

$fn = 48;

polyhedron(points = [[38.9255295343, -28.8750927454, 95.2417418154], [-14.6088363780, 11.9224002142, 95.2417416042], [-43.9609988465, -58.6307821855, 95.2417411369], [-43.9609988430, -58.6307821952, 95.2417417036], [-0.5262010384, -67.3900668776, 95.2417416656], [38.9255295308, -28.8750927356, 95.2417412487], [-0.5262010462, -67.3900669159, 95.2417416647], [-43.9609988353, -58.6307821569, 95.2417417045], [-47.6763941053, -139.8460777401, 95.2417422734], [58.4975517449, -109.6241145972, 95.2417417320], [38.9255301105, -28.8750933294, 95.2417407502], [-0.5262016181, -67.3900662838, 95.2417421641], [32.0263045712, -147.4734512895, 95.2417422126], [58.4975517645, -109.6241145698, 95.2417422396], [-0.5262016377, -67.3900663112, 95.2417416565], [32.0263045884, -147.4734513015, 95.2417421622], [82.8640214293, -157.7272841738, 95.2417431583], [58.4975517473, -109.6241145578, 95.2417422900], [38.9255295293, -28.8750927520, 95.2417416962], [49.5263421922, 48.6541307900, 95.2417416713], [-14.6088363730, 11.9224002208, 95.2417417233], [49.5263422010, 48.6541307888, 95.2417416877], [38.9255295205, -28.8750927507, 95.2417416799], [98.0557325432, -31.5169481829, 95.2417417304], [98.0557325442, -31.5169481612, 95.2417417435], [38.9255295195, -28.8750927725, 95.2417416668], [116.3819536586, -58.9412003715, 95.2417418842]], triangles = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23], [24, 25, 26]]);
/***********************************************
******      SolidPython code:      *************
************************************************
 
#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
import tree
import utilities
from numpy import array,cross
from tree import TriangleNode, parseArrayIntoTree, parseEdgeArrayIntoTree, cutTreeIntoPatches
from stl_reader import Reader
from graph2 import Graph,TreeNode,treeLength
from utilities import getMatrixArbitraryAxis
from dxf_writer import DXFWriter
from evolution import TreeWorld

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

triangles = Reader.read("stl/rhino-quarter.stl")
g = Graph(triangles)
hFn = lambda e: g.defaultHeuristic(e)
msp = g.toMSPTree(hFn)
edge_rep = msp.makeEdgeRepresentation()

hFn = lambda e: -g.defaultHeuristic(e)
msp2 = g.toMSPTree(hFn)
edge_rep2 = msp2.makeEdgeRepresentation()

world = TreeWorld(g, [edge_rep, edge_rep2])
child1 = world.generateFittest()
print child1
tn = parseEdgeArrayIntoTree(g.nodes, child1)
print treeLength(msp,set()), "faces"
#tn = parseArrayIntoTree(g.nodes, array_rep)
tn.unfold()
v = tn.getAllChildVertices()
v2d = tn.getAllChildVertices2D()
tn.getAllChildTriangles()
kdtree = utilities.makeKDTree(tn.getAllChildTriangles())

intersects = tn.checkIntersection() # return nodes thats intersect
print len(intersects), "faces that intersects"
paths = world.paths_intersection(child1)
cutEdges = g.cutEdges(paths)
print "Edges to cut:", cutEdges
tns = cutTreeIntoPatches(tn,cutEdges)

#v_i = [ x.getTransformedVertices2D() for x in intersects ]
#v = reduce(lambda x,y: x+y, v_i)

#print [x.node for x in xs]
#print len(xs)


#array_rep = [19, 55, 115, 49, -1, 147, 55, 194, 230, 180, 14, 82, 8, 198, 157, 197, 196, 81, 254, 240, 148, 120, 26, 46, 181, 123, 210, 223, 125, 143, 52, 21, 107, 16, 212, 250, 125, 73, 196, 27, 75, 249, 167, 39, 57, 103, 166, 23, 207, 15, 3, 240, 178, 191, 33, 181, 111, 29, 184, 177, 7, 92, 118, 59, 15, 93, 129, 58, 199, 94, 97, 98, 40, 61, 143, 64, 234, 251, 75, 91, 32, 78, 186, 133, 76, 134, 90, 4, 187, 218, 51, 49, 218, 182, 106, 43, 176, 138, 121, 63, 216, 151, 36, 10, 149, 146, 47, 226, 198, 133, 66, 104, 103, 46, 162, 10, 113, 251, 25, 83, 114, 62, 11, 5, 114, 206, 120, 38, 245, 185, 159, 110, 238, 1, 189, 226, 87, 154, 142, 160, 96, 54, 44, 5, 233, 68, 74, 12, 242, 253, 54, 208, 222, 211, 33, 93, 124, 155, 127, 215, 137, 127, 168, 13, 50, 173, 19, 152, 2, 24, 230, 6, 248, 115, 195, 153, 222, 232, 170, 148, 51, 173, 52, 254, 34, 253, 171, 84, 203, 205, 153, 135, 8, 197, 128, 60, 246, 141, 4, 9, 108, 3, 140, 144, 79, 117, 221, 100, 45, 158, 214, 20, 32, 22, 175, 111, 76, 18, 182, 175, 119, 85, 190, 139, 163, 99, 151, 234, 22, 63, 8, 144, 177, 144, 76, 237, 113, 193, 239, 238, 19, 162, 26, 244, 174, 140, 235, 225, 172, 41, 249, 117, 84, 77, 18, 239]
#print array_rep
#tn = parseArrayIntoTree(g.nodes, array_rep)
#tn.unfold()
#v = tn.getAllChildVertices()

def assembly(v):
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
  for i,tn in enumerate(tns):
    v = tn.getAllChildVertices()
    a = assembly(v)
    scad_render_to_file(a,'unfold{0}.scad'.format(i), file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

    #a = intersecting()
    #scad_render_to_file(a,'unfold.scad', file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    #d = DXFWriter(v2d) 
    #d.generate_file()
 
 
***********************************************/
                            

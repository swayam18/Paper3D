$fn = 48;

polyhedron(points = [[29.5476640199, 33.7395804468, 4.3911293753], [26.0520936911, 30.2529972180, 4.3911292406], [30.1450110485, 28.7572917436, 4.3911293442], [30.1450110540, 28.7572917442, 4.3911293222], [33.1702276779, 32.1648655626, 4.3911293832], [29.5476640145, 33.7395804461, 4.3911293972], [31.5068621554, 37.0144554081, 4.3911293866], [29.5476640164, 33.7395804505, 4.3911293952], [33.1702276760, 32.1648655582, 4.3911293852], [31.5068621417, 37.0144554164, 4.3911293856], [27.6005484680, 35.6167259961, 4.3911293990], [29.5476640301, 33.7395804422, 4.3911293962], [34.5914201727, 34.6054957665, 4.3911293495], [31.5068621035, 37.0144553903, 4.3911295089], [33.1702277280, 32.1648655761, 4.3911292629], [35.5704886640, 37.6693982964, 4.3911293964], [31.5068620871, 37.0144553693, 4.3911293995], [34.5914201891, 34.6054957875, 4.3911294590], [31.5068620857, 37.0144553782, 4.3911293902], [35.5704886654, 37.6693982875, 4.3911294057], [34.2245091448, 40.1493123944, 4.3911293956], [35.5704886633, 37.6693982863, 4.3911293876], [37.6174629202, 40.7504529827, 4.3911294446], [34.2245091469, 40.1493123955, 4.3911294137], [41.6243168099, 40.6073834780, 4.3911296228], [37.6174628196, 40.7504530495, 4.3911295266], [35.5704887639, 37.6693982195, 4.3911293056], [35.5704886731, 37.6693982935, 4.3911293891], [34.5914201799, 34.6054957905, 4.3911294663], [37.9902860136, 33.9621429116, 4.3911294468], [37.9902860119, 33.9621429105, 4.3911294008], [39.5748946764, 34.3260481028, 4.3911293841], [35.5704886748, 37.6693982946, 4.3911294350], [42.2832399796, 37.2008245250, 4.3911295898], [35.5704886803, 37.6693983011, 4.3911292913], [39.5748946709, 34.3260480963, 4.3911295278], [37.4089789611, 32.5986190277, 4.3911293117], [34.5914201588, 34.6054957746, 4.3911293200], [33.1702277419, 32.1648655680, 4.3911292924], [36.4462365628, 27.2332567816, 4.3911291891], [37.4089789605, 32.5986190341, 4.3911292523], [33.1702277425, 32.1648655615, 4.3911293518], [37.4089789783, 32.5986190309, 4.3911291056], [36.4462365450, 27.2332567848, 4.3911293359], [38.2532289380, 30.5020661221, 4.3911291592], [37.4089789901, 32.5986190357, 4.3911290984], [38.2532289262, 30.5020661174, 4.3911291664], [38.9149909675, 31.9859694354, 4.3911291111], [40.1809488409, 29.4951080160, 4.3911291971], [38.9149909677, 31.9859694353, 4.3911291445], [38.2532289259, 30.5020661175, 4.3911291331], [42.8379330570, 32.4442261628, 4.3911291773], [38.9149909723, 31.9859694376, 4.3911291720], [40.1809488364, 29.4951080137, 4.3911291695], [42.8379330572, 32.4442261626, 4.3911291578], [40.1809488362, 29.4951080139, 4.3911291890], [45.5097582792, 29.6714651165, 4.3911290633], [40.1278826486, 29.3994591062, 4.3911292998], [38.2532289536, 30.5020661135, 4.3911292131], [36.4462365295, 27.2332567934, 4.3911292820]], triangles = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23], [24, 25, 26], [27, 28, 29], [30, 31, 32], [33, 34, 35], [36, 37, 38], [39, 40, 41], [42, 43, 44], [45, 46, 47], [48, 49, 50], [51, 52, 53], [54, 55, 56], [57, 58, 59]]);
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
filename = "kitten-122.stl"
triangles = Reader.read("stl/" + filename)
# triangles = Reader.read("stl/icosahedron.stl")
g = Graph(triangles)
n = len(g.nodes)
print "There are a total of ", n, " nodes"
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
ds = [tn.convertToDict() for tn in tns]
print "No of Patches:", len(ds)



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
        scad_render_to_file(a,'unfold.scad', file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    
    d_writer = DXFWriter(n, ds, filename)
    d_writer.generate_file()
 
 
***********************************************/
                            

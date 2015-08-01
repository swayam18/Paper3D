$fn = 48;

polyhedron(points = [[-12.0444705526, -1.5298455635, 15.8930888896], [7.3471214117, -9.6658941500, 15.8930890294], [4.6973500050, 11.1957413527, 15.8930889485], [7.3471214076, -9.6658941505, 15.8930889594], [24.0889415076, 3.0596928818, 15.8930881957], [4.6973500092, 11.1957413533, 15.8930890185], [26.7387122215, -17.8019434579, 15.8930885893], [24.0889416303, 3.0596927204, 15.8930884287], [7.3471212849, -9.6658939891, 15.8930887264], [9.9968916144, -30.5275299470, 15.8930886467], [26.7387121532, -17.8019436207, 15.8930882641], [7.3471213532, -9.6658938263, 15.8930890515], [4.6973499479, 11.1957412072, 15.8930886103], [24.0889415689, 3.0596930278, 15.8930886038], [21.4391697768, 23.9213280417, 15.8930886268], [-9.3946995701, -22.3914814540, 15.8930888340], [7.3471214335, -9.6658940980, 15.8930890371], [-12.0444705744, -1.5298456155, 15.8930888818], [-12.0444705923, -1.5298455112, 15.8930887765], [4.6973500448, 11.1957413005, 15.8930890615], [-14.6942414331, 19.3317892808, 15.8930894356], [-14.6942414607, 19.3317892150, 15.8930892486], [4.6973500724, 11.1957413663, 15.8930892486], [2.0475786678, 32.0573760810, 15.8930892486], [-31.4360626312, 6.6062024192, 15.8930889389], [-12.0444708707, -1.5298455466, 15.8930887009], [-14.6942411547, 19.3317893162, 15.8930895112], [-31.4360627159, 6.6062025306, 15.8930891448], [-14.6942410700, 19.3317892047, 15.8930893054], [-34.0858323706, 27.4678378058, 15.8930894424], [-34.0858324389, 27.4678376430, 15.8930897676], [-14.6942410017, 19.3317893676, 15.8930889802], [-17.3440110654, 40.1934245123, 15.8930893628], [-31.4360629453, 6.6062025015, 15.8930888370], [-34.0858321412, 27.4678378350, 15.8930897502], [-50.8276539059, 14.7422522549, 15.8930894179], [-50.8276538832, 14.7422522251, 15.8930898482], [-34.0858321639, 27.4678378648, 15.8930893199], [-53.4774235651, 35.6038877933, 15.8930897656], [-50.8276538136, 14.7422522339, 15.8930899494], [-53.4774236348, 35.6038877844, 15.8930896644], [-70.2192444451, 22.8783022316, 15.8930903235], [-70.2192443427, 22.8783020970, 15.8930901072], [-53.4774237371, 35.6038879191, 15.8930898807], [-72.8690144698, 43.7399383343, 15.8930899073], [-53.4774237010, 35.6038880052, 15.8930896628], [-56.1271934249, 56.4655240064, 15.8930896310], [-72.8690145060, 43.7399382481, 15.8930901253], [-67.5694749914, 2.0166670718, 15.8930901365], [-50.8276538412, 14.7422521681, 15.8930901365], [-70.2192444174, 22.8783022975, 15.8930901365], [-34.0858321137, 27.4678379843, 15.8930894263], [-36.7356021632, 48.3294741319, 15.8930895209], [-53.4774236153, 35.6038876738, 15.8930896592], [-31.4360630208, 6.6062023216, 15.8930889071], [-50.8276538304, 14.7422524348, 15.8930893479], [-48.1778847562, -6.1193825759, 15.8930883254], [-31.4360625684, 6.6062025689, 15.8930891259], [-28.7862920425, -14.2554326058, 15.8930888735], [-12.0444709335, -1.5298456963, 15.8930885139]], triangles = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23], [24, 25, 26], [27, 28, 29], [30, 31, 32], [33, 34, 35], [36, 37, 38], [39, 40, 41], [42, 43, 44], [45, 46, 47], [48, 49, 50], [51, 52, 53], [54, 55, 56], [57, 58, 59]]);
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
from tree import TriangleNode, parseArrayIntoTree, parseEdgeArrayIntoTree
from stl_reader import Reader
from graph2 import Graph,TreeNode,treeLength
from utilities import getMatrixArbitraryAxis
from dxf_writer import DXFWriter
from evolution import TreeWorld

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
 
 
***********************************************/
                            

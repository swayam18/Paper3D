#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re
from numpy import array
from tree import TriangleNode

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48
points = [[0,0,0,1], [10,0,0,1], [0,10,0,1], [10,10,10,1], [10,0,20,1]]
triangles = [[0,1,2],[1,3,2],[2,3,4]]

vertices = [
    array([0,0,0,1]),
    array([10,0,0,1]),
    array([0,10,0,1]),
    array([10,10,10,1]),
    array([10,0,20,1]),
    array([ 1.7763568394e-15 ,  10.0 ,  1.7763568394e-15 , 1]),
    array([ 10.0 ,  10.0 ,  10.0, 1 ]),
    array([ 10.0 ,  20.0 ,  20.0, 1 ])
]
vertices = vertices
root = TriangleNode([vertices[0],vertices[1],vertices[2]])
child1 = TriangleNode([vertices[1],vertices[3],vertices[2]])
child2 = TriangleNode([vertices[2],vertices[3],vertices[4]])
root.addChildren(child1,(vertices[1],vertices[2]))
child1.addChildren(child2,(vertices[2],vertices[3]))
child2.unfold()
child1.unfold()

#print root.transformed_vertices
#print child1.transformed_vertices
#print child2.transformed_vertices
cr = [ x.tolist() for x in root.transformed_vertices ]
c1 = [ x.tolist()[0] for x in child1.transformed_vertices ]
c2 = [ x.tolist()[0] for x in child2.transformed_vertices ]
unfolded_vs = cr+c1+c2
print unfolded_vs
def assembly():
    a = polyhedron(
            points=[x.tolist()[:3] for x in vertices],
            triangles=triangles)
    b = polyhedron(
            points = [x[:3] for x in unfolded_vs],
            triangles = [[0,1,2],[3,4,5],[6,7,8]]) 
    return union()(a,b)

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a,'unfold.scad', file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

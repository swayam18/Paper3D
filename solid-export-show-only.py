#! /usr/bin/env python
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
from obj_reader import ObjReader

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48
filename = "uv_sphere.obj"
mesh = ObjReader().read("obj/sphere/" + filename)
triangles = mesh.triangles()
# triangles = Reader.read("stl/icosahedron.stl")
g = Graph(triangles, mesh)
n = len(g.nodes)
print "There are a total of ", n, " nodes"
hFn = lambda e: g.defaultHeuristic(e)
msp = g.toMSPTree(hFn)
edge_rep = msp.makeEdgeRepresentation()

hFn = lambda e: -g.defaultHeuristic(e)
msp2 = g.toMSPTree(hFn)
edge_rep2 = msp2.makeEdgeRepresentation()

world = TreeWorld(g, [edge_rep, edge_rep2])
child1 = world.generateFittest(maxGenerations=1)
print child1
tn = parseEdgeArrayIntoTree(g.nodes, child1)
print treeLength(msp,set()), "faces"
#tn = parseArrayIntoTree(g.nodes, array_rep)
print tn.node
tn.unfold()
tn.generateMesh()
mesh.setMesh()

################ START OF SHOW
#!/usr/bin/env python
import sys
sys.path.append('..')
import ctypes

import pyglet
from pyglet.gl import *

rotation = 0

meshes = mesh.originalMesh.mesh

window = pyglet.window.Window()

lightfv = ctypes.c_float * 4

print mesh.originalMesh.material.vertices

@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., float(width)/height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    glEnable(GL_LIGHT0)

    glTranslated(0, 0, -3)
    glRotatef(rotation, 0, 1, 0)
    glRotatef(-25, 1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glEnable(GL_LIGHTING)

    mesh.originalMesh.mesh.draw()

def update(dt):
    pass
    global rotation
    rotation += 90*dt
    if rotation > 720: rotation = 0

pyglet.clock.schedule(update)

pyglet.app.run()

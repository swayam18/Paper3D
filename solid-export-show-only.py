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
filename = "earth.obj"
mesh = ObjReader().read("obj/earth/" + filename)
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
tn.unfold()
tn.generateMesh()
mesh.setMesh()

################ START OF SHOW
"""This script shows another example of using the PyWavefront module."""
# This example was created by intrepid94
import sys
sys.path.append('..')
import ctypes

import pyglet
from pyglet.gl import *

from pywavefront import Wavefront

rotation = 0

window = pyglet.window.Window(1800, 900, caption = 'Demo', resizable = True)

lightfv = ctypes.c_float * 4
label = pyglet.text.Label('Hello, world', font_name = 'Times New Roman', font_size = 12, x = 800, y = 700, anchor_x = 'center', anchor_y = 'center')
@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width)/height, 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():
    window.clear()
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)
    # glTranslated(0, 4, -8)
 #    glRotatef(90, 0, 1, 0)
 #    glRotatef(-60, 0, 0, 1)
   # Rotations for sphere on axis - useful
    glTranslated(-20, -10, -50)
    glRotatef(rotation, 0, 0, 1)
    mesh.originalMesh.mesh.draw()

def update(dt):
    global rotation
    return
    rotation += 45 * dt
    if rotation > 720: 
       rotation = 0

pyglet.clock.schedule(update)

pyglet.app.run()

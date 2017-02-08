# This file reads obj files

import pywavefront
import numpy as np
from pprint import pprint
from copy import copy
from utilities import getNormal, toNpArray

class ObjReader:
  def read(self, filename):
    wavefront = pywavefront.Wavefront(filename)
    parsedObject = pywavefront.ObjParser(wavefront, wavefront.file_name)

    vertices = self.groupVertices(parsedObject.material.vertices)

    return ObjectMesh(self.toFaces(vertices))

  def toFaces(self, vertices):
    return map(ObjectFace, zip(*[iter(vertices)]*3))

  def groupVertices(self, vertices):
      return [ObjectVertex(vertices[i:i + 8]) for i in xrange(0, len(vertices), 8)]

class ObjectVertex:
    def __init__(self, vertices):
        self.t = toNpArray(vertices[0:2])
        self.n = toNpArray(vertices[2:5])
        self.v = toNpArray(vertices[5:8])

    def __str__(self):
        return "Vertex: <{},{},{}>".format(self.v,self.n,self.t)

    def __repr__(self):
        return self.__str__()

class ObjectFace:
    def __init__(self, vertices):
        self.v1 = vertices[0]
        self.v2 = vertices[1]
        self.v3 = vertices[2]

        self.n = getNormal([self.v1.v, self.v2.v, self.v3.v])

    def triangle(self):
       return [self.v1.v, self.v2.v, self.v3.v, self.n, self.v1.t, self.v2.t, self.v3.t]

    def __str__(self):
        return "Face: <{},{},{}>".format(self.v1,self.v2,self.v3)

    def __repr__(self):
        return self.__str__()

class ObjectMesh:
    def __init__(self, faces):
        self.faces = faces

    def triangles(self):
        return map(lambda f: f.triangle(),self.faces)

    def __str__(self):
        return "Mesh: <{}>".format(self.faces)

    def __repr__(self):
        return self.__str__()

# to test only...
reader = ObjReader()
reader.read('obj/sphere/uv_sphere.obj')

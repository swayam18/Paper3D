# This file reads obj files

import pywavefront
import numpy as np
from pprint import pprint
from copy import copy
from utilities import getNormal, toNpArray

class ObjReader:
  def read(self, filename):
    wavefront = pywavefront.Wavefront('obj/sphere/uv_sphere.obj')
    parsedObject = pywavefront.ObjParser(wavefront, wavefront.file_name)

    groupedVertices = self.groupVertices(parsedObject.material.vertices)
    vertices = [v[5:] for v in groupedVertices]

    return map(self.toTriangle, self.toFaces(vertices))

  def toFaces(self, vertices):
    return map(self.toFace, zip(*[iter(vertices)]*3))

  def toFace(self, vertices):
    return map(toNpArray, vertices)

  def toTriangle(self, face):
    face.append(getNormal(face))
    return face

  def groupVertices(self, vertices):
      return [vertices[i:i + 8] for i in xrange(0, len(vertices), 8)]

reader = ObjReader()
reader.read('')


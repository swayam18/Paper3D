from numpy import matrix, linalg, cross, dot, array
import numpy as np
from math import cos, sin, pi
from utilities import getMatrixArbitraryAxis, angleBetween, getTranslationMatrix, getNormal, unitVector

def getUnfoldingMatrix(normal1, normal2, edge):
    m1 = getTranslationMatrix((-edge[0]-edge[1])/2)
    axis = unitVector(cross(normal1,normal2))
    m2 = getMatrixArbitraryAxis(axis, angleBetween(normal1,normal2))
    m3 = getTranslationMatrix((edge[0]+edge[1])/2)
    return m3 * m2 * m1

def traverse(node, explored):
  parent = TriangleNode(node.face)
  explored.add(node)
  if len(node.children) == 1 and node.children[0] in explored:
    return parent
  else:
    for child in node.children:
      if child not in explored:
        edges = []
        for v1 in node.face.getVertices():
          for v2 in child.face.getVertices():
            if v1 == v2:
              edges.append(v1)
        assert(len(edges)==2)
        parent.addChildren(traverse(child,explored),edges)
    return parent

def traverse_for_vertices(triangleNode):
  face_vertex = [[ x.tolist() for x in triangleNode.transformed_vertices ]]
  if len(triangleNode.children) == 0:
    return face_vertex
  else:
    for child,edges in triangleNode.children:
      face_vertex.extend(traverse_for_vertices(child))
    return face_vertex

def unfold(triangleNode):
  if len(triangleNode.children) == 0:
    triangleNode.unfold()
  else:
    for child,edges in triangleNode.children:
      unfold(child)
    triangleNode.unfold()

class TriangleNode:
    def __init__(self,face):
        #child is a tuple: (TriangleNode, edges(v1,v2))
        self.root = False
        self.children = []
        #[(x,y,z),(x,y,z)] in anti-clockwise
        if len(face.v1)==3:
            self.vertices = [np.append(face.v1,1),np.append(face.v2,1),np.append(face.v3,1)]
        else:
            self.vertices = [array(face.v1), array(face.v2), array(face.v3)]
        self.transformed_vertices = self.vertices
        self.normal = array(face.n)

    #edges: (v1,v2) index of vertices
    def addChildren(self,node,edges):
        self.children.append([node,[array(edge) for edge in edges]])
        node.setParent(self)

    def setParent(self, parent):
        self.parent = parent
        for node,edges in parent.children:
            if self == node:
                self.localFlattenMatrix = getUnfoldingMatrix(self.parent.normal,self.normal,edges)

    def unfold(self, unfold_matrix=None):
        if self.root and unfold_matrix is None: return
        if unfold_matrix == None:
            unfold_matrix = self.localFlattenMatrix
        for i,x in enumerate(self.transformed_vertices):
            #if x.shape == (4,1):
                #self.transformed_vertices[i] = unfold_matrix * matrix(x)
            self.transformed_vertices[i] = array((unfold_matrix * matrix(x).T).T)[0]
        for child, edge in self.children:
            child.unfold(unfold_matrix)

    def getTransformedVertices(self):
        if self.root: return [[ x.tolist() for x in triangleNode.transformed_vertices ]]


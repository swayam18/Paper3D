from numpy import matrix, linalg, cross, dot, array
import numpy as np
from math import cos, sin, pi
def getMatrixArbitraryAxis(point1,point2, angle):
    axis = unitVector(point2-point1)
    x,y,z = axis[:3]
    c = cos(angle)
    s = sin(angle)
    t = 1 - c
    return matrix([
        [t*x*x + c,   t*x*y - s*z, t*x*z + s*y, 0],
        [t*x*y + s*z, t*y*y + c,   t*y*z - s*x, 0],
        [t*x*z - s*y, t*y*z + s*x, t*z*z + c,   0],
        [0,           0,           0,           1]])

def getMatrixArbitraryAxis2(axis, angle):
    x,y,z = axis[:3]
    c = cos(angle)
    s = sin(angle)
    t = 1 - c
    return matrix([
        [t*x*x + c,   t*x*y - s*z, t*x*z + s*y, 0],
        [t*x*y + s*z, t*y*y + c,   t*y*z - s*x, 0],
        [t*x*z - s*y, t*y*z + s*x, t*z*z + c,   0],
        [0,           0,           0,           1]])

def angleBetween(v1,v2):
    v1_u = unitVector(v1)
    v2_u = unitVector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    reference = unitVector((array([0,0,1]),v1_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    #if dot(v2_u,reference) < 0:
        #return -angle
    return -angle

def getTranslationMatrix(vector):
    return matrix([
            [1,0,0,vector[0]],
            [0,1,0,vector[1]],
            [0,0,1,vector[2]],
            [0,0,0,1]])

def columnCross(v1,v2):
    return cross(v1.T[0,0:3],v2.T[0,0:3]).T

def getNormal(vertices):
    edge1 = vertices[0] - vertices[1]
    edge2 = vertices[0] - vertices[2]
    v = cross(edge1[:3], edge2[:3])
    return np.append(unitVector(v),0)

def unitVector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def getUnfoldingMatrix(parent, child, edge):
    m1 = getTranslationMatrix((-edge[0]-edge[1])/2)
    axis = unitVector(cross(parent.normal,child.normal))
    m2 = getMatrixArbitraryAxis2(axis, angleBetween(parent.normal,child.normal))
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
                self.localFlattenMatrix = getUnfoldingMatrix(self.parent,self,edges)

    def unfold(self, unfold_matrix=None):
        if self.root: return
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


from numpy import matrix, linalg, cross, dot, array
import numpy as np
import utilities
from math import cos, sin, pi
from utilities import getMatrixArbitraryAxis, angleBetween, getTranslationMatrix, getNormal, unitVector, getUnfoldingMatrix, flatternMatrixArray

def parseArrayIntoTree(nodes, array):
    print [x.index for x in nodes]
    root = TriangleNode(nodes[array.index(-1)]).makeRoot()
    stack = [root]
    while stack:
        parent = stack.pop(0)
        idxs = [i for i,x in enumerate(array) if x == parent.node.index]
        children = [ TriangleNode(nodes[i]) for i in idxs]
        for child in children:
            edges = []
            for v1 in parent.node.getVertices():
              for v2 in child.node.getVertices():
                if v1 == v2:
                  edges.append(v1)
            assert(len(edges)==2)
            parent.addChild(child,edges)
        stack.extend(children)
    return root

class TriangleNode:
    def __init__(self,face):
        #child is a tuple: (TriangleNode, edges(v1,v2))
        self.node = face
        self.children = []
        self.matrix = []
        #[(x,y,z),(x,y,z)] in anti-clockwise
        if len(face.v1)==3:
            self.vertices = [np.append(face.v1,1),np.append(face.v2,1),np.append(face.v3,1)]
        else:
            self.vertices = [array(face.v1), array(face.v2), array(face.v3)]
        self.transformed_vertices = self.vertices
        self.normal = array(face.n)

    def makeRoot(self):
        up = array([0,0,1])
        axis = unitVector(cross(up, self.normal))
        self.matrix = [getMatrixArbitraryAxis(axis, angleBetween(up,self.normal))]
        return self

    #edges: (v1,v2) index of vertices
    def addChild(self,node,edges):
        self.children.append([node,[array(edge) for edge in edges]])
        node.setParent(self)

    def setParent(self, parent):
        self.parent = parent
        for node,edges in parent.children:
            if self == node:
                self.localFlattenMatrix = getUnfoldingMatrix(self.parent.normal,self.normal,edges)
                self.matrix = parent.matrix + [self.localFlattenMatrix] 

    def unfold(self):
        for i,x in enumerate(self.transformed_vertices):
            self.transformed_vertices[i] = array((flatternMatrixArray(self.matrix) * matrix(x).T).T)[0]
        for child, edge in self.children:
            child.unfold()

    def getTransformedVertices2D(self):
        return [[ round(i,5) for i in x][:2] for x in self.transformed_vertices ]

    def checkIntersection(self):
        v = traverse_for_vertices(self)
        vertices2D = [[[round(i,5) for i in y][:2] for y in x] for x in v]
        return utilities.findIntersectingTriangles(self,vertices2D)

    def _getAllChildVertices(self):
        face_vertex = [[ x.tolist() for x in self.transformed_vertices ]]
        if len(self.children) == 0:
            return face_vertex
        else:
            for child,edges in self.children:
              face_vertex.extend(child._getAllChildVertices())
            return face_vertex

    def getAllChildVertices(self):
        v = self._getAllChildVertices()
        return [y[:3] for y in reduce(lambda x,y: x+y, v)]

    def getAllChildVertices2D(self):
        v = self._getAllChildVertices()
        return [y[:2] for y in reduce(lambda x,y: x+y, v)]

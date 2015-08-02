from numpy import matrix, linalg, cross, dot, array
import numpy as np
import utilities
from math import cos, sin, pi
from utilities import getMatrixArbitraryAxis, angleBetween, getTranslationMatrix, getNormal, unitVector, getUnfoldingMatrix, flatternMatrixArray, vertex_close_enough
import operator

def parseArrayIntoTree(nodes, array):
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
                if vertex_close_enough(v1,v2):
                  edges.append(v1)
            assert(len(edges)==2)
            parent.addChild(child,edges)
        stack.extend(children)
    return root

def parseEdgeArrayIntoTree(nodes, array):
    root = TriangleNode(nodes[0]).makeRoot()
    stack = [root]
    copy = array[:]
    while stack:
        parent = stack.pop(0)
        index = parent.node.index
        for i,e in enumerate(copy[:]):
            child = None
            if e[0] == index:
                child = TriangleNode(nodes[e[1]])
                copy.remove(e)
            elif e[1] == index:
                child = TriangleNode(nodes[e[0]])
                copy.remove(e)
            if child == None: continue
            edges = []
            for v1 in parent.node.getVertices():
                for v2 in child.node.getVertices():
                    if vertex_close_enough(v1,v2):
                        edges.append(v1)
            assert(len(edges)==2)
            parent.addChild(child,edges)
            stack.append(child)
    return root

def cutTreeIntoPatches(root,cutEdges):
  cuts = []
  roots = [root]
  stack = [root]
  while stack:
    parent = stack.pop(0)
    index = parent.node.index
    children = parent.children
    edges = [(index,child[0].node.index) for child in children]
    for i,edge in enumerate(edges):
      if edge not in cutEdges and (edge[1],edge[0]) not in cutEdges:
        continue
      cuts.append((parent,children[i]))
    for child in children:
      stack.append(child[0])
  for parent, child in cuts:
    roots.append(child[0])
    parent.children.remove(child)

  for rt in roots:
    rt.makeRoot()
  return roots


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

    def getAllNodeIndices(self):
        return self._getAllNodeIndices()

    def _getAllNodeIndices(self):
        indices = [self.node.index]
        if len(self.children) == 0:
            return indices
        for child,edge in self.children:
            indices.extend(child._getAllNodeIndices())
        return indices

    def getAllEdges(self):
        return self._getAllEdges()

    def _getAllEdges(self):
        edges = [self.node.edge_to_nodes]
        if len(self.children) == 0:
            return edges
        for child,edge in self.children:
            edges.extend(child._getAllEdges())
        return edges

    def convertToDict(self):
        d = self._convertToDict()
        
        return d

    def _convertToDict(self):
        d = {}
        d[self.node.index] = self
        if len(self.children) == 0:
            return d
        for child,edge in self.children:
            d.update(child._convertToDict())
        return d


    def checkIntersection(self):
        v_i = self._getAllFaceVertices2D()
        faceVertices = [ x[0] for x in v_i]
        faceIndex = [ x[1] for x in v_i]
        kdtree = utilities.makeKDTree(faceVertices)
        return self._checkIntersection(faceVertices,faceIndex,kdtree)

    def _checkIntersection(self, triangles, index, kdtree):
        #t = utilities.checkTriangleIntersections(self.getTransformedVertices2D(), triangles)
        t = kdtree.intersection(utilities.Triangle(self.getTransformedVertices2D(),self.node.index))
        if t!=False:
            out = [(self.node.index,index[t])]
        else: out = []
        if len(self.children) == 0:
            return out
        else:
            for child, edge in self.children:
                out.extend(child._checkIntersection(triangles, index, kdtree))
            return out

    def _getAllChildVertices(self):
        face_vertex = [[ x.tolist() for x in self.transformed_vertices ]]
        if len(self.children) == 0:
            return face_vertex
        else:
            for child,edges in self.children:
              face_vertex.extend(child._getAllChildVertices())
            return face_vertex

    def _getAllFaceVertices2D(self):
        face_vertex = [(self.getTransformedVertices2D(),self.node.index)]
        if len(self.children) == 0:
            return face_vertex
        else:
            for child,edges in self.children:
              face_vertex.extend(child._getAllFaceVertices2D())
            return face_vertex

    def getAllChildVertices(self):
        v = self._getAllChildVertices()
        return [y[:3] for y in reduce(lambda x,y: x+y, v)]

    def getAllChildVertices2D(self):
        v = self._getAllChildVertices()
        return [y[:2] for y in reduce(lambda x,y: x+y, v)]

    def getAllChildTriangles(self):
        ts = self._getAllChildVertices()
        return [ [ v[:2] for v in t ] for t in ts]

import numpy as np
from unionfind import UnionFind
from numpy import matrix, linalg, cross, dot, array
from math import cos, sin, pi

eps = 0.0001
def close_enough(edge1, edge2):
    # edge: (v1,v2)
    e1v1 = edge1[0]
    e1v2 = edge1[1]
    e2v1 = edge2[0]
    e2v2 = edge2[1]

    diff_x = abs(e1v1[0] - e2v1[0]) < eps
    diff_y = abs(e1v1[1] - e2v1[1]) < eps 
    diff_z = abs(e1v1[2] - e2v1[2]) < eps
    s = diff_x and diff_y and diff_z
    diff_x = abs(e1v2[0] - e2v2[0]) < eps
    diff_y = abs(e1v2[1] - e2v2[1]) < eps 
    diff_z = abs(e1v2[2] - e2v2[2]) < eps
    a = diff_x and diff_y and diff_z

    return a and s

def vertex_close_enough(v1,v2):
    diff_x = abs(v1[0] - v2[0]) < eps
    diff_y = abs(v1[1] - v2[1]) < eps 
    diff_z = abs(v1[2] - v2[2]) < eps
    return diff_x and diff_y and diff_z

def memoize(f):
    """ Memoization decorator for a function taking one or more arguments. """
    class memodict(dict):
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            ret = self[key] = f(*key)
            return ret

    return memodict().__getitem__

def flatternMatrixArray(array):
    return reduce(lambda m1,m2: matrixMultiply(m1,m2), array)

@memoize
def matrixMultiply(m1,m2):
    return m1*m2

def getUnfoldingMatrix(normal1, normal2, edge):
    m1 = getTranslationMatrix((-edge[0]-edge[1])/2)
    axis = unitVector(cross(normal1,normal2))
    m2 = getMatrixArbitraryAxis(axis, angleBetween(normal1,normal2))
    m3 = getTranslationMatrix((edge[0]+edge[1])/2)
    return m3 * m2 * m1

def getMatrixArbitraryAxis(axis, angle):
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

# check if p1 -> p2 intersects pA -> pB
def checkLineIntersection(point1, point2, pointA, pointB):
   assert((len(point1) == 2) and (len(pointA) == 2))
   a,b = point1
   c,d = point2
   p,q = pointA
   r,s = pointB
   det = float((c - a) * (q - s) - (p - r) * (d - b))
   if det == 0:
       return False
   l = round(((q - s) * (p - a) + (r - p) * (q - b)) / det,6)
   g = round(((b - d) * (p - a) + (c - a) * (q - b)) / det,6)
   return (0.0 < l and l < 1.0) and (0.0 < g and g < 1.0)

#print checkLineIntersection((0,0),(1,1),(0,1),(1,0))

def planeCheck(p1,p2,p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def checkPointInTriangle(point, vertices):
    b1 = planeCheck(point, vertices[0], vertices[1]) < 0
    b2 = planeCheck(point, vertices[1], vertices[2]) < 0
    b3 = planeCheck(point, vertices[2], vertices[0]) < 0
    return b1 == b2 and b1 == b3

def checkTriangleIntersection(t1,t2):
    for i in range(3):
        for j in range(3):
            if checkLineIntersection(t1[i],t1[(i+1)%3],t2[j],t2[(j+1)%3]):
                return True
    t1 = [tuple(x) for x in t1]
    t2 = [tuple(x) for x in t2]
    s1 = set(t1)
    s2 = set(t2)
    _s1 = s1 - s2
    _s2 = s2 - s1
    if len(_s1) == 0: return False
    for v in _s1:
        if checkPointInTriangle(v,t2):
            return True
    for v in _s2:
        if checkPointInTriangle(v,t1):
            return True
    return False
    

def checkTriangleIntersections(t1, triangles):
    for i,t in enumerate(triangles):
        if checkTriangleIntersection(t1,t): return i
    return False

def makeKDTree(triangles):
    ts = [Triangle(x,i) for i,x in enumerate(triangles)]
    bbMin = [float('inf'),float('inf')]
    bbMax = [float('-inf'),float('-inf')]
    axis = 0
    for t in ts:
        bbMin[0] = min(bbMin[0], t.bbMin[0])
        bbMin[1] = min(bbMin[1], t.bbMin[1])
        bbMax[0] = max(bbMax[0], t.bbMax[0])
        bbMax[1] = max(bbMax[1], t.bbMax[1])
    root = _makeKDTree(ts, bbMin, bbMax, axis)
    return root

def _makeKDTree(triangles, bbMin, bbMax, axis):
    root = KdNode(axis)
    root.bbMin = bbMin
    root.bbMax = bbMax
    root.objects = triangles
    if len(triangles) < 3:
        root.leaf = True
        return root
    middle = (bbMin[axis] + bbMax[axis]) / 2
    root.middle = middle
    left_triangles = []
    right_triangles = []
    overlap = 0
    for t in triangles:
        if t.bbMax[axis] <= middle:
            left_triangles.append(t)
        elif t.bbMin[axis] >= middle:
            right_triangles.append(t)
        else:
            overlap+=1
            right_triangles.append(t)
            left_triangles.append(t)
    if (overlap * 2) > len(triangles):
        leaf = KdNode(axis)
        leaf.objects = triangles
        leaf.leaf = True
        return leaf

    left_bbMax = bbMax[:]
    left_bbMax[axis] = middle
    right_bbMin = bbMin[:]
    right_bbMin[axis] = middle

    root.left = _makeKDTree(left_triangles, bbMin, left_bbMax, (axis+1)%2)
    root.right = _makeKDTree(right_triangles, right_bbMin, bbMax, (axis+1)%2)
    return root
    
class KdNode:
    def __init__(self,axis):
        self.axis = axis
        self.bbMin = []
        self.bbMax = []
        self.middle = None
        self.leaf = False
        self.objects = []
        self.left = None
        self.right = None

    def intersection(self,triangle):
        if self.leaf:
            for t in self.objects:
                if checkTriangleIntersection(triangle.vs, t.vs): return t.index
            return False
        else:
            x1 = False
            x2 = False
            if not triangle.bbMin[self.axis] > self.middle:
                x1 = self.left.intersection(triangle)
            if not triangle.bbMax[self.axis] < self.middle:
                x2 = self.right.intersection(triangle)
            return x1 or x2

class Triangle:
    def __init__(self,vs,i):
        self.index = i
        self.vs = vs
        self.bbMin = [0,0]
        self.bbMax = [0,0]
        self.bbMin[0] = reduce(lambda x,y: min(x,y), [x[0] for x in vs])
        self.bbMin[1] = reduce(lambda x,y: min(x,y), [x[1] for x in vs])
        self.bbMax[0] = reduce(lambda x,y: max(x,y), [x[0] for x in vs])
        self.bbMax[1] = reduce(lambda x,y: max(x,y), [x[1] for x in vs])

def makeUnionFind(_set,N):
    uf = UnionFind(N)
    for i,j in _set:
        uf.union(i,j)
    return uf

#assert(checkTriangleIntersection([(0,0),(1,0),(0,1)],[(0,0),(0.5,0),(0,0.5)]))
#assert(checkTriangleIntersection([(0,0),(1,0),(0,1)],[(0,0),(1,0),(0,1)]))
#assert(checkTriangleIntersection([(0,0),(1,0),(0,1)],[(0,0),(1,0),(0,0.5)]))
#assert(not checkTriangleIntersection([(0,0),(1,0),(0,1)],[(0,0),(-1,0),(0,-1)]))
#assert(not checkTriangleIntersection([(0,0),(1,0),(0,1)],[(-0.1,-0.1),(-1,0),(0,-1)]))
#assert(checkTriangleIntersection([(0,0),(1,0),(0,1)],[(0.1,0.1),(0.5,0.1),(0.1,0.5)]))
#assert(not checkTriangleIntersection([(0,0),(1,0),(0,1)],[(0,1),(1,0),(1,1)]))
#assert(not checkTriangleIntersection([(0,0),(1,0),(0,1)],[(0,0),(0,1),(-1,0)]))
#assert(not checkTriangleIntersection([[-12.04447, -1.52985], [7.34713, -9.66589], [4.69735, 11.19574]],[[26.73872, -17.80193], [24.08894, 3.0597], [7.34713, -9.66589]]))

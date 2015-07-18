import numpy as np
from math import cos, sin, pi
from numpy import matrix, linalg, cross, dot, array

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

triangle1 = [0,1,2]
triangle2 = [1,2,3]
triangle3 = [2,3,4]
triangle4 = [5,7,6]

# normal1 = normal2 * m
def makeRotationalMatrix(normal1, normal2):
    v = cross(normal1,normal2)
    s = linalg.norm(v)
    c = dot(normal1, normal2)
    m_v = matrix([
        [0,-v[2],v[1]],
        [v[2],0,-v[0]],
        [-v[1],v[0],0]])
    return np.identity(3) + m_v + (m_v * m_v * (1 - c) / (s * s))

def getNormal(triangle):
    edge1 = vertices[triangle[0]] - vertices[triangle[1]]
    edge2 = vertices[triangle[0]] - vertices[triangle[2]]
    v = cross(edge1[:3], edge2[:3])
    return np.append(unit_vector(v),0)

def unit_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def getMatrixArbitraryAxis(point1, point2, angle):
    a = point1[0]
    b = point1[1]
    c = point1[2]
    axis = unit_vector(point2-point1)
    u = axis[0]
    v = axis[1]
    w = axis[2]
    c = cos(angle)
    s = sin(angle)

    return matrix([
        [u*u + (v*v + w*w) * c, u*v * (1 - c) - w*s,   u*w * (1 - c) + v*s,   (a * (v*v + w*w) - u * (b*v + c*w)) * (1 - c) + (b*w - c*v) * s],
        [u*v * (1 - c) + w*s,   v*v + (u*u + w*w) * c, v*w * (1 - c) - u*s,   (b * (u*u + w*w) - v * (a*u + c*w)) * (1 - c) + (c*u - a*w) * s],
        [u*w * (1 - c) - v*s,   v*w * (1 - c) + u*s,   w*w + (u*u + v*v) * c, (c * (u*u + v*v) - w * (a*u + b*v)) * (1 - c) + (a*v - b*u) * s],
        [0,0,0,1]])

def getMatrixArbitraryAxis2(point1,point2, angle):
    axis = unit_vector(point2-point1)
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
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

def getTranslationMatrix(vector):
    return matrix([
            [1,0,0,vector[0]],
            [0,1,0,vector[1]],
            [0,0,1,vector[2]],
            [0,0,0,1]])


def unfold(edge, triangle, parent):
    normal1 = getNormal(parent)
    normal2 = getNormal(triangle)
    m1 = getTranslationMatrix((-vertices[edge[0]] - vertices[edge[1]])/2)
    m2 = getMatrixArbitraryAxis2(vertices[edge[0]], vertices[edge[1]], pi-angleBetween(normal1,normal2))
    m3 = getTranslationMatrix((vertices[edge[0]] + vertices[edge[1]])/2) 
    points = []
    for i in triangle:
        point = ( m3 * m2 * m1 * np.transpose(matrix(vertices[i]))).tolist()
        print '[',point[0][0],', ',point[1][0],', ',point[2][0],'],'
        points.append(point)
    return points

normal1 = getNormal(triangle1)
normal2 = getNormal(triangle2)
#m = makeRotationalMatrix(normal1, normal2)
#print normal1
#print normal2*m

m2 = getMatrixArbitraryAxis2(vertices[1], vertices[2], pi-angleBetween(normal1,normal2))
m1 = getTranslationMatrix((-vertices[1] - vertices[2])/2)
m3 = getTranslationMatrix((vertices[1] + vertices[2])/2) 
mm = m1*m2*m3
for i in triangle3:
    #point = (vertices[i] * m2).tolist()[0]
    point = m3 * m2 * m1 * np.transpose(matrix(vertices[i]))
    plist = point.tolist()
    print '[',plist[0][0],', ',plist[1][0],', ',plist[2][0],'],'

#print unfold((2,3), triangle3, triangle2)
unfold((1,2),triangle4,triangle1)

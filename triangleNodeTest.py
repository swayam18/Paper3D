import unittest
import tree
from numpy import array
from tree import TriangleNode

class TestTriangleNode(unittest.TestCase):
    def setUp(self):
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
        self.vertices = vertices
        self.root = TriangleNode([vertices[0],vertices[1],vertices[2]])
        self.child1 = TriangleNode([vertices[1],vertices[3],vertices[2]])
        self.child2 = TriangleNode([vertices[2],vertices[3],vertices[4]])
        self.root.addChildren(self.child1,(vertices[1],vertices[2]))
        self.child1.addChildren(self.child2,(vertices[2],vertices[3]))

    def assertNumpyArrayEqual(self, actual, expected):
        self.assertEqual((actual-expected).any(), False)

    def test_normal(self):
        normal = tree.getNormal(self.root.vertices) 
        self.assertNumpyArrayEqual(normal, array([0,0,1,0]))

    def test_unit(self):
        vector = self.vertices[0] - self.vertices[1]
        unit = tree.unitVector(vector)
        self.assertNumpyArrayEqual(unit, array([-1,0,0,0]))

    def test_local_unfold(self):
        self.child1.unfold()

if __name__ == '__main__':
    unittest.main()

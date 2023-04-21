import unittest
import numpy
from pynite_element import models

class TestTrussModel(unittest.TestCase):

    def setUp(self):
        self.truss = models.Truss(
            nodes=[models.Node(0, 0), models.Node(0, 120)],
            elasticity=30 * (10 ** 6),
            area=2
        )

    def test_stiffness_matrix(self):
        actual_stiffness_matrix = (((30 * (10 ** 6)) * 2) / 120) * numpy.array([
            [0, 0, 0, 0],
            [0, 1, 0, -1],
            [0, 0, 0, 0],
            [0, -1, 0, 1]
        ])
        comparison = self.truss.stiffness_matrix == actual_stiffness_matrix
        self.assertTrue(comparison.all())


class TestSpringModel(unittest.TestCase):

    def setUp(self):
        nodes = [models.Node(0, 0), models.Node(120, 0)]
        self.spring = models.Spring(nodes=nodes, stiffness=200)

    def test_stiffness_matrix(self):
        actual_stiffness_matrix = numpy.array([
            [200, -200],
            [-200, 200]
        ])
        comparison = self.spring.stiffness_matrix == actual_stiffness_matrix
        self.assertTrue(comparison.all())


if __name__ == '__main__':
    unittest.main()
import unittest
import numpy
from pynite_element import models

class TestTrussModel(unittest.TestCase):

    def setUp(self):
        self.truss = models.Truss(
            [models.Node(0, 0, 0), models.Node(0, 120, 1)],
            30 * (10 ** 6),
            2
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


if __name__ == '__main__':
    unittest.main()
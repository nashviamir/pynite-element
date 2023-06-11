import unittest
import numpy
from pynite_element import solvers, models


class TestDefaultSolver(unittest.TestCase):
    def setUp(self):
        node1 = models.Node(0, 0, dx=0)
        node2 = models.Node(100, 0)
        node3 = models.Node(200, 0, fx=50)
        element1 = models.Spring(
            nodes=[node1, node2],
            stiffness=1000
        )
        element2 = models.Spring(
            nodes=[node2, node3],
            stiffness=2000
        )
        self.solver = solvers.DefaultSolver(elements=[element1, element2])
        self.solver.enumerate_nodes()
        

    def test_assemble(self):
        actual_stiffness_matrix = numpy.array([
            [ 1000, -1000,     0,],
            [-1000,  3000, -2000,],
            [    0, -2000,  2000,]
        ])

        assambled_stiffness_matrix = self.solver.assemble()
        comparison = actual_stiffness_matrix == assambled_stiffness_matrix

        self.assertTrue(comparison.all())

    def test_displacement_matrix(self):
        actual_displacement_matrix = numpy.array([
            [0],
            [1],
            [1]
        ])

        solver_displacement_matrix = self.solver.get_displacement_matrix()
        comparison = actual_displacement_matrix == solver_displacement_matrix
        self.assertTrue(comparison.all())

    def test_force_matrix(self):
        actual_force_matrix = numpy.array([
            [0],
            [0],
            [50]
        ])

        solver_force_matrix = self.solver.get_force_matrix()
        comparison = actual_force_matrix == solver_force_matrix
        self.assertTrue(comparison.all())


    def test_matrix_reduction(self):
        stiffness_matrix = self.solver.assemble()
        solver_reduced_stiffness_matrix = self.solver.reduce_matrix(stiffness_matrix, column=True)
        actual_reduced_stiffness_matrix = numpy.array([
            [3000, -2000,],
            [-2000,  2000,]
        ])
        comparison = actual_reduced_stiffness_matrix == solver_reduced_stiffness_matrix
        self.assertTrue(comparison.all())
        


if __name__ == '__main__':
    unittest.main()
import numpy


class Solver(object):

    def __init__(self, elements):
        self.elements = elements
        self.nodes = list(dict.fromkeys(sum([element.nodes for element in self.elements], [])))
        self.SYS_DOF = sum([node.DOF for node in self.nodes])
        

    def enumerate_nodes(self):
        for i, node in enumerate(self.nodes):
            node.index = i

class DefaultSolver(Solver):
    
    def solve(self):
        self.enumerate_nodes()
        stiffness_matrix = self.assemble()

    
    def assemble(self):
        self.stiffness_matrix = numpy.zeros([self.SYS_DOF, self.SYS_DOF])

        for element in self.elements:
            element_stiffness_matrix = element.stiffness_matrix
            
            addresses = self.create_addresses(element)
            for i, row_addr in enumerate(addresses):
                for j, col_addr in enumerate(addresses):
                    self.stiffness_matrix[row_addr][col_addr] += element_stiffness_matrix[i][j]

        return self.stiffness_matrix


    def get_displacement_matrix(self):
        self.displacement_matrix = numpy.ones((self.SYS_DOF,1))
        for element in self.elements:
            element_displacement_matrix = element.displacement_matrix

            addresses = self.create_addresses(element)
            for i , addr in enumerate(addresses):
                if not element.displacement_matrix[i] is None:
                    self.displacement_matrix[addr, 0] = element.displacement_matrix[i]

        return self.displacement_matrix


    def reduce_stiffness_matrix(self, stiffness_matrix):
        indexes_to_remove = [i for i, value in enumerate(self.get_displacement_matrix().transpose()[0]) if value == 0]
        self.reduced_stiffness_matrix = numpy.delete(stiffness_matrix, indexes_to_remove, 0)
        self.reduced_stiffness_matrix = numpy.delete(self.reduced_stiffness_matrix, indexes_to_remove, 1)
        return self.reduced_stiffness_matrix
            


    def create_addresses(self, element):
        addresses = []
        for node in element.nodes:
            for i in reversed(range(element.DOF)):
                addresses.append(element.DOF * node.index - i)

        return addresses
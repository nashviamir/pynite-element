import numpy


class Solver(object):

    def __init__(self, elements):
        self.elements = elements
        self.nodes = list(dict.fromkeys(sum([element.nodes for element in self.elements], [])))
        

    def enumerate_nodes(self):
        for i, node in enumerate(self.nodes):
            node.index = i

class DefaultSolver(Solver):
    
    def solve(self):
        stiffness_matrix = self.assemble()

    
    def assemble(self):
        SYS_DOF = sum([node.DOF for node in self.nodes])
        
        stiffness_matrix = numpy.zeros([SYS_DOF, SYS_DOF])

        for element in self.elements:
            element_stiffness_matrix = element.stiffness_matrix
            
            addresses = self.create_addresses(element)
            for i, row_addr in enumerate(addresses):
                for j, col_addr in enumerate(addresses):
                    stiffness_matrix[row_addr][col_addr] += element_stiffness_matrix[i][j]

        return stiffness_matrix

    def create_addresses(self, element):
        addresses = []
        for node in element.nodes:
            for i in reversed(range(element.DOF)):
                addresses.append(element.DOF * node.index - i)

        return addresses
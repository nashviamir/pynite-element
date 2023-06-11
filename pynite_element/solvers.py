import numpy
import json
from .models import Spring, Truss, Beem, Node


class Solver(object):

    def __init__(self, elements):
        self.elements = elements
        self.nodes = list(dict.fromkeys(sum([element.nodes for element in self.elements], [])))
        self.SYS_DOF = sum([node.DOF for node in self.nodes])
        

    def enumerate_nodes(self):
        for i, node in enumerate(self.nodes):
            node.index = i

class DefaultSolver(Solver):
    
    @classmethod
    def from_json(cls, filename):
        models = {
            "spring": Spring,
            "truss": Truss,
            "beem": Beem
        }
        elements = []
        with open(filename, "r") as file:
            data = json.load(file)
            nodes = [Node(**node_data) for node_data in data["nodes"]]
            for i, element in enumerate(data["elements"]):
                model_type = element.pop("type")
                element["nodes"] = [nodes[i], nodes[i + 1]]
                element = models[model_type](**element)
                elements.append(element)

        return cls(elements=elements)

                


    def solve(self):
        #preprocessing
        self.enumerate_nodes()
        stiffness_matrix = self.assemble()
        force_matrix = self.get_force_matrix()
        displacement_matrix = self.get_displacement_matrix()

        # matrix reduction (deleting rows and columns of constrained nodes)
        reduced_stiffness_matrix = self.reduce_matrix(stiffness_matrix, column=True)
        reduced_force_matrix = self.reduce_matrix(force_matrix)
        reduced_displacement_matrix = self.reduce_matrix(displacement_matrix)
        
        #processing
        displacement_results = numpy.matmul(numpy.linalg.inv(reduced_stiffness_matrix), reduced_force_matrix)
        transposed_displacement_results = iter(displacement_results.transpose()[0])

        for i, displacement in enumerate(displacement_matrix.transpose()[0]):
            if displacement == 1:
                displacement_matrix[i,0] = next(transposed_displacement_results)

        force_results = numpy.matmul(stiffness_matrix, displacement_matrix)
        transposed_force_results = iter(force_results.transpose()[0])
        for i, force in enumerate(force_matrix.transpose()[0]):
            if force == 0:
                force_matrix[i,0] = next(transposed_force_results)

        self.set_results(displacement_matrix, force_matrix)

        
            
    def set_results(self, displacements, forces):
        for element in self.elements:
            addresses = self.create_addresses(element)
            for addr in addresses:
                element.result_displacement.append(displacements[addr, 0])
                element.result_force.append(forces[addr, 0])

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

    def get_force_matrix(self):
        self.force_matrix = numpy.zeros((self.SYS_DOF,1))
        for element in self.elements:
            element_force_matrix = element.force_matrix

            addresses = self.create_addresses(element)
            for i , addr in enumerate(addresses):
                if not element.force_matrix[i] is None:
                    self.force_matrix[addr, 0] = element.force_matrix[i]

        return self.force_matrix

    def reduce_matrix(self, matrix, column=False):
        indexes_to_remove = [i for i, value in enumerate(self.get_displacement_matrix().transpose()[0]) if value == 0]
        reduced_matrix = numpy.delete(matrix, indexes_to_remove, 0)
        if column:
            reduced_matrix = numpy.delete(reduced_matrix, indexes_to_remove, 1)
        return reduced_matrix
            


    def create_addresses(self, element):
        addresses = []
        for node in element.nodes:
            for i in reversed(range(element.DOF)):
                addresses.append(element.DOF * node.index - i)

        return addresses
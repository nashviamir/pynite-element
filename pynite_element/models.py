import numpy
from math import dist

class Node(object):

    def __init__(self, x, y, index=None, fx=None, fy=None, dx=None, dy=None):
        self.x = x
        self.y = y

        if index is not None:
            self.index = index
            
        self.fx = fx
        self.fy = fy
        self.dx = dx
        self.dy = dy
    
    
class Element(object):
    DOF = 1
    def __init__(self, nodes=None):
        self.nodes = nodes
        for node in self.nodes:
            node.DOF = self.DOF

    @property
    def stiffness_matrix(self):
        raise NotImplementedError("Abstract Class Element doesnt implement stiffness matrix")

    @property
    def displacement_matrix(self):
        raise NotImplementedError("Abstract Class Element doesnt implement displacement matrix")



class Spring(Element):
    
    def __init__(self, nodes, stiffness):
        super().__init__(nodes)
        self.start, self.end = self.nodes
        self.stiffness = stiffness

    @property
    def stiffness_matrix(self):
        k = self.stiffness * numpy.array([
            [1, -1],
            [-1, 1]
        ])
        return k




class Truss(Element):
    
    def __init__(self, nodes, elasticity, area):
        super().__init__(nodes)
        self.start, self.end = self.nodes
        self.length = dist((self.start.x, self.start.y), (self.end.x, self.end.y))
        self.elasticity = elasticity
        self.area = area

    @property
    def stiffness_matrix(self):
        constant = (self.area * self.elasticity) / self.length

        
        c = (self.end.x - self.start.x) / self.length
        s = (self.end.y - self.start.y) / self.length
        cc = c ** 2
        ss = s ** 2
        cs = c * s

        k = constant * numpy.array([
            [cc, cs, -cc, -cs],
            [cs, ss, -cs, -ss],
            [-cc, -cs, cc, cs],
            [-cs, -ss, cs, ss]
        ])

        return k
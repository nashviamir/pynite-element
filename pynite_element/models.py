import numpy
from math import dist

class Node(object):

    def __init__(self, x, y, index=None, fx=None, fy=None, m=None, dx=None, dy=None, phi =None,):
        self.x = x
        self.y = y
        

        if index is not None:
            self.index = index
            
        self.fx  = fx
        self.fy  = fy
        self.m   = m
        self.dx  = dx
        self.dy  = dy
        self.phi = phi

    
    @property
    def displacesments(self):
        return [self.dx , self.dy , self.phi]


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

    @property
    def force_matrix(self):
        raise NotImplementedError("Abstract Class Element doesnt implement force matrix")


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

    @property
    def displacement_matrix(self):
        return [self.start.dx, self.end.dx]

    @property
    def force_matrix(self):
        return [self.start.fx, self.end.fx]




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

    @property
    def displacement_matrix(self):
        return [self.start.dx, self.start.dy, self.end.dx, self.end.dy]

    @property
    def force_matrix(self):
        return [self.start.fx, self.start.fy, self.end.fx, self.end.fy]
    

   
class Beem(Element):
        def __init__(self, nodes, elasticity, area ):
            super().__init__(nodes)
            self.start, self.end = self.nodes
            self.length = dist((self.start.x, self.start.y),(self.end.x, self.end.y))
            self.elasticity = elasticity
            self.area = area

        @property
        def stiffness_matrix(self):
          constant =(self.elasticity*self.area)/(self.length)**3 

          k = constant * numpy.array ([    
                [12            , 6*self.length     , -12            , 6*self.length   ],
                [6*self.length , 4*self.length**2  , -6*self.length , 2*self.length**2],
                [-12           , -6*self.length    , 12             , -6*self.length  ],
                [6*self.length , 2*self.length**2  , -6*self.length , 4*self.length**2],
             ])
          
          return k

        @property
        def displacement_matrix(self):
            return [self.start.dy, self.start.phi, self.end.dy, self.end.phi]
        

        @property
        def force_matrix(self):
            return [self.start.fx, self.start.m, self.end.fx, self.end.m]
    
    

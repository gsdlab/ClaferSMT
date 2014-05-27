'''
Created on Mar 24, 2013

@author: ezulkosk
'''


class FunExp(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, operation, elements):
        self.operation = operation
        self.elements = elements
        
        
    def __str__(self):
        from constraints.BracketedConstraint import ClaferToZ3OperationsMap
        arity = ClaferToZ3OperationsMap[self.operation][0]
        if arity == 1:
            return self.operation + str(self.elements[0])
        elif arity == 2:
            return str(self.elements[0]) + " " + self.operation + " " + str(self.elements[1])
        else:
            return self.operation + str(self.elements[0]) + str(self.elements[1]) + str(self.elements[2])
    
    def __repr__(self):
        return self.__str__()
    
    def toString(self, level):
        return str(self)
    
    
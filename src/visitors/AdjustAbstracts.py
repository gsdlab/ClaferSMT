'''
Created on Nov 11, 2013

@author: ezulkosk
'''
from pip.backwardcompat import reduce
from visitors import VisitorTemplate
import ast
import operator
import visitors

class AdjustAbstracts(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.scopeStack = []

    def claferVisit(self, element):
        sort = self.z3.z3_sorts[element.uid]
        newScope = reduce(operator.mul, self.scopeStack, 1)
        (_, u) = element.card
        if sort.numInstances != newScope and self.scopeStack and u.value != -1:
            sort.numInstances = self.scopeStack[-1] * u.value
        self.scopeStack.append(sort.numInstances)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.scopeStack.pop()    
        
            
    
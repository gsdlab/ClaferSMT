'''
Created on Nov 10, 2013

@author: ezulkosk
'''
from visitors import VisitorTemplate
import ast
import visitors

class SetScopes(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3

    
    def claferVisit(self, element):
        sort = self.z3.z3_sorts[element.uid]
        a = 0
        for i in range(sort.numInstances):
            sort.getInstanceRange(i)
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
            
    
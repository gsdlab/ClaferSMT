'''
Created on May 1, 2013

@author: ezulkosk
'''

from visitors import VisitorTemplate
import ast
import visitors

class GroupCardConstraints(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Creates the Clafer hierarchy using Z3 Datatypes and Sorts.
    The fields will need to be changed to lists ASAP.
    '''
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3

    
    def claferVisit(self, element):
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        for i in element.elements:
            if isinstance(i, ast.Clafer.Clafer):
                self.z3.z3_sorts[element.uid].addField(self.z3.z3_sorts[i.uid])
         
    
    
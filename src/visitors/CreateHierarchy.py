'''
Created on May 1, 2013

@author: ezulkosk
'''

from visitors import VisitorTemplate
import ast
import visitors

class CreateHierarchy(VisitorTemplate.VisitorTemplate):
    '''
    :var cfr: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Creates the Clafer hierarchy using Z3 Datatypes and Sorts.
    The fields will need to be changed to lists ASAP.
    '''
    def __init__(self, cfr):
        '''
        :param cfr: The Z3 solver.
        :type cfr: :class:`~common.Z3Instance`
        '''
        self.cfr = cfr

    
    def claferVisit(self, element):
        self.cfr.cfr_sorts[element.uid].checkSuperAndRef()
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        for i in element.elements:
            if isinstance(i, ast.Clafer.Clafer):
                self.cfr.cfr_sorts[element.uid].addField(self.cfr.cfr_sorts[i.uid])
    
    
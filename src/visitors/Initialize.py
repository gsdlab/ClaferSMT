'''
Created on Nov 6, 2013

@author: ezulkosk
'''
from visitors import VisitorTemplate
import ast
import visitors

class Initialize(VisitorTemplate.VisitorTemplate):
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

        self.cfr.cfr_sorts[element.uid].initialize()

        for i in element.elements:
            visitors.Visitor.visit(self, i)
            
class Scopeless_Initialize(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Creates the Clafer hierarchy using Z3 Datatypes and Sorts.
    The fields will need to be changed to lists ASAP.
    '''
    def __init__(self, cfr):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.cfr = cfr

    
    def claferVisit(self, element):
        self.cfr.cfr_sorts[element.uid].scopeless_initialize()
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    
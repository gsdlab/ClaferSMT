'''
Created on Apr 28, 2013

@author: ezulkosk
'''


from structures.ClaferSort import ClaferSort
from visitors import VisitorTemplate
import common.Common
import visitors.Visitor

class CreateSorts(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Adds sorts to the :mod:`~common.Z3Instance` for each clafer.
    '''
    
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.stack = []
    
    def claferVisit(self, element):
        '''
        Instantiates a ClaferSort for each clafer.
        
        *see* :mod:`common.ClaferSort`
        '''
        visitors.Visitor.visit(self,element.supers)
        sort = ClaferSort(element, self.z3, self.stack)
        #print(element.uid)
        self.z3.addSort(element.uid, sort)  
        self.stack.append(sort)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.stack.pop()
            
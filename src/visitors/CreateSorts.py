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
    Adds sorts to the :mod:`~common.Z3Instance` for each clafer.
    '''
    
    def __init__(self, cfr):
        '''
        :param cfr: The Clafer model.
        :type cfr: :class:`~common.ClaferModel`
        '''
        self.cfr = cfr
        self.stack = []
    
    def claferVisit(self, element):
        '''
        Instantiates a ClaferSort for each clafer.
        
        *see* :mod:`common.ClaferSort`
        '''
        visitors.Visitor.visit(self,element.supers)
        sort = ClaferSort(element, self.cfr, self.stack)
        #print(element.uid)
        self.cfr.addSort(element.uid, sort)  
        self.stack.append(sort)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.stack.pop()
            
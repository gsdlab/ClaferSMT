'''
Created on Apr 28, 2013

@author: ezulkosk
'''

from common import ClaferSort
from visitors import VisitorTemplate
import common.Common
import visitors.Visitor

class CreateSorts(VisitorTemplate.VisitorTemplate):
    '''
    adds sorts to the Z3Instance for each clafer
    fields:
        z3(Z3Instance): the Z3Instance object
    '''
    
    def __init__(self, z3instance):
        self.z3 = z3instance
    
    def claferVisit(self, element):
        visitors.Visitor.visit(self,element.supers)
        self.z3.addSort(element.uid, ClaferSort.ClaferSort(element.uid))  
        for i in element.elements:
            visitors.Visitor.visit(self, i)
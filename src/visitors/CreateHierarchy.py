'''
Created on May 1, 2013

@author: ezulkosk
'''
from common import ClaferDatatype
from visitors import VisitorTemplate
import visitors

class CreateHierarchy(VisitorTemplate.VisitorTemplate):
    '''
    creates the Clafer hierarchy using Z3 Datatypes and Sorts
    the fields will need to be changed to lists ASAP
    fields:
        z3(Z3Instance): the Z3Instance object
    '''
    def __init__(self, z3instance):
        self.z3 = z3instance
    
    def claferVisit(self, element):
        claferDatatype = ClaferDatatype.ClaferDatatype(self.z3, self.z3.z3_sorts[element.uid])
        self.z3.addDatatype(self.z3.z3_sorts[element.uid], claferDatatype)
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    
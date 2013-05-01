'''
Created on Apr 30, 2013

@author: ezulkosk
'''
from constraints import CardinalityConstraint
from visitors import VisitorTemplate
import visitors.Visitor


class CreateCardinalityConstraints(VisitorTemplate.VisitorTemplate):
    '''
    adds cardinality based constraints to Z3Instance
    fields:
        z3(Z3Instance): the Z3Instance object
    '''
    def __init__(self, z3instance):
        self.z3 = z3instance
    
    def claferVisit(self, element):
        self.z3.addConstraint(CardinalityConstraint.CardinalityConstraint(self.z3.z3_sorts[element.uid], element.card))
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    

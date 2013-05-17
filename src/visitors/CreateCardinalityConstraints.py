'''
Created on Apr 30, 2013

@author: ezulkosk
'''
from constraints import CardinalityConstraint
from visitors import VisitorTemplate
import visitors.Visitor



class CreateCardinalityConstraints(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Adds cardinality based constraints to :mod:`~common.Z3Instance`.
    '''
    
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
    
    def claferVisit(self, element):
        '''
        Instantiates a Cardinality constraint.
        
        *see* :mod:`constraints.CardinalityConstraint`
        '''
        self.z3.addConstraint(CardinalityConstraint.CardinalityConstraint(self.z3.z3_sorts[element.uid], element.card, element.glCard))
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    

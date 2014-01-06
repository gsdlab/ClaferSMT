'''
Created on Nov 10, 2013

@author: ezulkosk
'''
from ast.IntegerLiteral import IntegerLiteral
from common import Options
from common.Exceptions import UnusedAbstractException
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
        self.glStack = [1]

    '''
    may need to fix for 3..*
    '''
    
    def claferVisit(self, element):
        (_, upper) = element.card
        (glower, _) = element.glCard
        upper = upper.value
        
        if upper == -1:
            element.glCard = (glower, IntegerLiteral(Options.GLOBAL_SCOPE))
            self.glStack.append(Options.GLOBAL_SCOPE)
        else:
            upper = self.glStack[-1] * upper
            element.glCard = (glower, IntegerLiteral(upper))
            self.glStack.append(upper)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.glStack.pop()
            

    
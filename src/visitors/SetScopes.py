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
    def __init__(self, cfr):
        '''
        :param cfr: The Clafer model.
        :type cfr: :class:`~common.ClaferModel`
        '''
        self.cfr = cfr
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
            

    
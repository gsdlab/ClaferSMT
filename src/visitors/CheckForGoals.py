'''
Created on Jan 13, 2014

@author: ezulkosk
'''
from ast import IntegerLiteral
from common import Options
from constraints import Operations
from gia import consts
from structures.ExprArg import JoinArg
from visitors import VisitorTemplate, Visitor, CreateBracketedConstraints
from z3 import Sum
import visitors

class CheckForGoals(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    
    
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3

    '''
    may need to fix for 3..*
    '''
    
    def goalVisit(self, element):
        bracketedConstraintsVisitor = CreateBracketedConstraints.CreateBracketedConstraints(self)
        op = element.exp.iExp[0].operation
        if op == "min":
            op = consts.METRICS_MINIMIZE
        else:
            op = consts.METRICS_MAXIMIZE
        expr = bracketedConstraintsVisitor.objectiveVisit(element.exp.iExp[0].elements[0])
        if isinstance(expr[0], JoinArg):
            expr = Operations.computeJoin(expr)
        mask = expr[0][1]
        valueList = [i for i in mask.values()]
        self.z3.objectives.append((op, Sum(valueList)))
    

            

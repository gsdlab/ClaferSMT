'''
Created on Jan 13, 2014

@author: ezulkosk
'''
from ast import IntegerLiteral
from common import Options, Common, SMTLib
from constraints import operations
from structures.ExprArg import JoinArg
from visitors import VisitorTemplate, Visitor, CreateBracketedConstraints
import visitors


class CheckForGoals(VisitorTemplate.VisitorTemplate):
    '''
    :var cfr: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    
    
    def __init__(self, cfr):
        '''
        :param cfr: The Clafer model.
        :type cfr: :class:`~common.ClaferModel`
        '''
        self.cfr = cfr

    '''
    may need to fix for 3..*
    '''
    
    def goalVisit(self, element):
        bracketedConstraintsVisitor = CreateBracketedConstraints.CreateBracketedConstraints(self)
        op = element.exp.iExp[0].operation
        if op == "min":
            op = Common.METRICS_MINIMIZE
        else:
            op = Common.METRICS_MAXIMIZE
        expr = bracketedConstraintsVisitor.objectiveVisit(element.exp.iExp[0].elements[0])
        if isinstance(expr[0], JoinArg):
            expr = operations.Join.computeJoin(expr)
        mask = expr[0][1]
        valueList = [i for i in mask.values()]
        self.cfr.objectives.append((op, SMTLib.SMT_Sum(valueList)))
    

            

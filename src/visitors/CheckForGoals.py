'''
Created on Jan 13, 2014

@author: ezulkosk
'''
from common import Common, SMTLib
from constraints import operations
from structures.ExprArg import JoinArg
from visitors import VisitorTemplate, CreateBracketedConstraints


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
        bracketedConstraintsVisitor = CreateBracketedConstraints.CreateBracketedConstraints(self.cfr)
        op = element.exp.iExp[0].operation
        if op == "min":
            op = Common.METRICS_MINIMIZE
        else:
            op = Common.METRICS_MAXIMIZE
        expr = bracketedConstraintsVisitor.objectiveVisit(element.exp.iExp[0].elements[0])
        if isinstance(expr[0], JoinArg):
            #TODO cache stuff here too (pass cfr into computeJoin if caching
            expr = operations.Join.computeJoin(expr)
        valueList = [SMTLib.createIf(c, i, SMTLib.SMT_IntConst(0)) for (i,c) in expr.getInts()]
        self.cfr.objectives.append((op, SMTLib.createSum(valueList)))
    

            

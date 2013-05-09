'''
Created on May 1, 2013

@author: ezulkosk
'''
from constraints import Constraint
from jinja2.nodes import Const
from z3 import Exists, Distinct, And, Not, IntSort, Consts

class CardinalityConstraint(Constraint.Constraint):
    '''
    :var claferSort: (:mod:`~common.ClaferSort`) The Sort that will be constrained.
    :var lower: (int) The lower cardinality bound.
    :var upper: (int) The upper cardinality bound.
    
    
    Creates very simple cardinality constraints for each clafer
    I suspect this will probably need to change in the future
    '''
    
    def __init__(self, claferSort, card):
        '''
        :param claferSort: ClaferSort for a given Clafer object from AST
        :type claferSort: :mod:`~common.ClaferSort`
        :param card: contains the lower and upper bounds, stored in lower and upper
        :type card: :mod:`~ast.IntegerLiteral`, :mod:`~ast.IntegerLiteral`
        '''
        (self.lower,self.upper) = card
        self.lower = self.lower.value
        self.upper = self.upper.value
        claferSort.addConsts(self.upper+1)
        self.claferSort = claferSort
        
    def generateConstraint(self):
        '''
        *see* :mod:`constraints.Constraint`
        '''
        #lower bound
        #"there exists lower.value distinct values for the given sort"
        '''
        return And(Exists(self.claferSort.consts[:self.lower], \
                       Distinct(*self.claferSort.consts[:self.lower])), \
                       #upper bound
                       #"there does not exist (upper.value+1) distinct values 
                       #  for the given sort"
                       Not(Exists(self.claferSort.consts[:self.upper+1], \
                       Distinct(*self.claferSort.consts[:self.upper+1])))) 
        ''' 
        #return Distinct(*self.claferSort.consts[:self.lower]) 
        x,y= Consts('a b',IntSort())
        return Exists(x, Distinct(x))
        
    @property
    def comment(self):
        '''
        *see* :mod:`constraints.Constraint`
        '''
        return "Bounds for " + self.claferSort.id + " === " +\
            self.stringValue
            
    @property
    def stringValue(self):
        '''
        *see* :mod:`constraints.Constraint`
        '''
        return "Exists(["+\
            ",".join([self.claferSort.id + str(x) for x in range(self.lower)])+\
            "],Distinct(" +\
            ",".join([self.claferSort.id + str(x) for x in range(self.lower)])+\
            ")) && " +\
            "Not(Exists(["+\
            ",".join([self.claferSort.id + str(x) for x in range(self.upper+1)])+\
            "],Distinct(" +\
            ",".join([self.claferSort.id + str(x) for x in range(self.upper+1)])+\
            "))"
        
    def __str__(self):
        return self.comment
'''
Created on May 1, 2013

@author: ezulkosk
'''
from constraints import Constraint

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
        claferSort.addConsts(self.upper.value+1)
        self.claferSort = claferSort
        
    def generateConstraint(self):
        '''
        *see* :mod:`constraints.Constraint`
        '''
        #lower bound
        #"there exists lower.value distinct values for the given sort"

        #value = ...

        #upper bound
        #"there does not exist (upper.value+1) distinct values 
        #  for the given sort"
        
        #value2 = ...
        
        #And(value1, value2)
        pass
        
        
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
            ",".join([self.claferSort.id + str(x) for x in range(self.lower.value)])+\
            "],Distinct(" +\
            ",".join([self.claferSort.id + str(x) for x in range(self.lower.value)])+\
            ")) && " +\
            "Not(Exists(["+\
            ",".join([self.claferSort.id + str(x) for x in range(self.upper.value+1)])+\
            "],Distinct(" +\
            ",".join([self.claferSort.id + str(x) for x in range(self.upper.value+1)])+\
            "))"
        
    def __str__(self):
        return self.comment
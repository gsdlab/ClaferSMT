'''
Created on May 1, 2013

@author: ezulkosk
'''
from constraints import Constraint

class CardinalityConstraint(Constraint.Constraint):
    '''
    Creates very simple cardinality constraints for each clafer
    I suspect this will probably need to change in the future
    Fields:
        claferSort (ClaferSort)
        lower (int): lower bound for the Clafer
        upper (int): upper bound for the Clafer
    '''
    
    
    '''
    Parameters:
        claferSort: ClaferSort for a given Clafer object from AST
        card: Pair of IntegerLiterals defining upper/lower bounds
    '''
    def __init__(self, claferSort, card):
        (self.lower,self.upper) = card
        claferSort.addConsts(self.upper.value+1)
        self.claferSort = claferSort
        
    def generateConstraint(self):
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
        return "Bounds for " + self.claferSort.id + " === " +\
            self.stringValue
            
    @property
    def stringValue(self):
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
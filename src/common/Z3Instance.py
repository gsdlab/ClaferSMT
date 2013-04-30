'''
Created on Apr 30, 2013

@author: ezulkosk
'''
import common


class Z3Instance(object):
    '''
    z3_constraints([]): contains ALL constraints that will be fed into z3,
                        holds Constraint objects
    z3_sorts([]): defines the sorts for each clafer
    '''
    z3_constraints = []
    z3_sorts = {}
    
    ###############################
    # accessors/modifiers         #
    ###############################
    def getConstraints(self):
        return self.z3_constraints
        
    def addConstraint(self, constraint):
        self.z3_constraints.append(constraint)
    
    '''
    Creates very simple cardinality constraints for each clafer
    I suspect this will probably need to change in the future
    Parameters:
        sortID: sortID for a given Clafer object from AST
        card: Pair of integers defining upper/lower bounds
    '''
    def addCardinalityConstraints(self, sortID, card):
        (lower,upper) = card
        
    def getSorts(self):
        return self.z3_sorts
        
    def addSort(self, sort):
        self.z3_sorts[sort] = common.ClaferSort.ClaferSort(sort)
    ###############################
    # end accessors/modifiers     # 
    ###############################
    
    
    
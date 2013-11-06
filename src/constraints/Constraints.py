'''
Created on Oct 3, 2013

@author: ezulkosk
'''
from common import Common
from common.Common import debug_print
from z3 import Bool, Implies, simplify, And, Not



class Constraints():
    """
    Adds a generated constraint to the solver.
    If in debug mode, add a Boolean tracker for the constraint, to obtain possible UNSAT cores.
    """
    def assertConstraint(self, constraint, z3):
        if Common.FLAG:
            #z3.solver.add(And(constraint, Not(constraint)))
            print(simplify(constraint))
        if Common.MODE != Common.DEBUG: 
            z3.solver.add(constraint)
        if Common.MODE == Common.DEBUG:
            p = Bool(str(self.assertID) + "_" + str(Common.getConstraintUID()))
            z3.unsat_core_trackers.append(p)
            z3.unsat_map[str(p)] = constraint
            z3.solver.add(Implies(p, constraint))

class GenericConstraints(Constraints): 
    def __init__(self, ident):
        self.constraints = []
        self.assertID = ident
        
    def addConstraint(self, c):
        self.constraints.append(c)
    
    def addAll(self, c):
        for i in c:
            self.constraints.append(i)    
    
    def assertConstraints(self, z3):
        '''
        Used to add all constraints to the solver.
        '''
        for i in self.constraints:
            self.assertConstraint(i,z3)
            
    def __str__(self):
        return str(self.ident)
            
    def debug_print(self):
        for i in self.constraints:
            debug_print(i)
            debug_print("")

class ClaferConstraints(Constraints):
    def __init__(self, claferSort):
        self.claferSort = claferSort
        self.assertID = str(self.claferSort.element.uid)
        self.instance_constraints = []
        self.card_constraints = []
        self.group_card_constraints = []
        self.inheritance_constraints = []
        self.ref_constraints = []
    
    def addInstanceConstraint(self,c):
        self.instance_constraints.append(c)
    
    def addCardConstraint(self,c):
        self.card_constraints.append(c)
        
    def addGroupCardConstraint(self,c):
        self.group_card_constraints.append(c)
        
    def addInheritanceConstraint(self,c):
        self.inheritance_constraints.append(c)
        
    def addRefConstraint(self,c):
        self.ref_constraints.append(c)
    
    def __str__(self):
        return str(self.claferSort.element.uid)
    
    def assertConstraints(self, z3):
        '''
        Used to add all constraints associated with this clafer to the solver.
        Can turn off different lists for debugging purposes.
        '''
        constraints = [
                       self.instance_constraints,
                       self.card_constraints,
                       self.group_card_constraints,
                       self.inheritance_constraints,
                       self.ref_constraints
                       ]   
        [self.assertConstraint(j,z3) for i in constraints for j in i]
    
    def debug_print(self):
        constraints = [
                       self.instance_constraints,
                       self.card_constraints,
                       self.group_card_constraints,
                       self.inheritance_constraints,
                       self.ref_constraints
                       ]   
        for i in constraints:
            for j in i:
                debug_print(j)
                debug_print("")

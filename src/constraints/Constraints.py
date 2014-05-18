'''
Created on Oct 3, 2013

@author: ezulkosk
'''
from common import Common, Options, SMTLib
from converters import Converters




class Constraints():
    """
    Adds a generated constraint to the solver.
    If in debug mode, add a Boolean tracker for the constraint, to obtain possible UNSAT cores.
    """
    
    def assertConstraint(self, constraint, z3):
        if Common.FLAG:
            #z3.solver.add(And(con
        # straint, Not(constraint)))
            from z3 import simplify
            print(simplify(constraint))
        
        if Options.PRODUCE_UNSAT_CORE:
            p = SMTLib.SMT_Bool(str(self.assertID) + "_" + str(Common.getConstraintUID()))
            z3.unsat_core_trackers.append(p)
            z3.unsat_map[str(p)] = constraint
            if Options.GOAL:
                z3.goal.add(SMTLib.SMT_Implies(p, constraint).convert(z3.solver_converter))
            else:
                z3.solver.add(SMTLib.SMT_Implies(p, constraint).convert(z3.solver_converter))
        else: 
            if Options.GOAL:
                z3.goal.add(constraint.convert(z3.solver_converter))
            else:
                print(constraint)
                z3.solver.add(constraint.convert(z3.solver_converter))
        
    def convert(self, f_n, constraint):
        #print("#####")
        #print(constraint)
        f_n.write(Converters.obj_to_string(constraint) + "\n")

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
            print(i)
            print("")
            
    def z3str_print(self, f_n):
        for i in self.constraints:
            self.convert(f_n, i)
            

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
        for i in constraints:
            for j in i:
                self.assertConstraint(j,z3)
    
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
                print(j)
                print("")
                
    def z3str_print(self,f_n):
        constraints = [
                       self.instance_constraints,
                       self.card_constraints,
                       self.group_card_constraints,
                       self.inheritance_constraints,
                       self.ref_constraints
                       ]   
        for i in constraints:
            for j in i:
                self.convert(f_n, j)

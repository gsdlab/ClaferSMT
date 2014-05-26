'''
Created on Oct 3, 2013

@author: ezulkosk
'''
from common import Common, Options, SMTLib
from solvers import Converters




class Constraints():
    """
    Adds a generated constraint to the solver.
    If in debug mode, add a Boolean tracker for the constraint, to obtain possible UNSAT cores.
    """
    
    def assertConstraint(self, constraint, cfr):
        if Common.FLAG:
            SMTLib.toStr(constraint)

        if Options.PRODUCE_UNSAT_CORE:
            
            #p = SMTLib.SMT_Bool(str(self.assertID) + "_" + str(Common.getConstraintUID()))
            p = SMTLib.SMT_Bool("bool" + "_" + str(Common.getConstraintUID()))
            cfr.unsat_core_trackers.append(cfr.solver.convert(p))
            cfr.unsat_map[str(p)] = constraint
            cfr.solver.add(SMTLib.SMT_Implies(p, constraint))
        else:
            cfr.solver.add(constraint)
        
    def convert(self, f_n, constraint):
        #print("#####")
        #print(constraint)
        f_n.write(Converters.obj_to_string(constraint) + "\n")

class GenericConstraints(Constraints): 
    def __init__(self, ident):
        self.constraints = []
        self.assertID = ident
        
    def addConstraint(self, c):
        #SMTLib.toStr(c)
        self.constraints.append(c)
    
    def addAll(self, c):
        for i in c:
            self.constraints.append(i)    
    
    def assertConstraints(self, cfr):
        '''
        Used to add all constraints to the solver.
        '''
        for i in self.constraints:
            self.assertConstraint(i,cfr)
            
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

    def addConstraint(self, list, c):
        #print("A")
        #SMTLib.toStr(c)
        list.append(c)

    def addInstanceConstraint(self,c):
        #print("B")
        self.addConstraint(self.instance_constraints, c)
    
    def addCardConstraint(self,c):
        #print("C")
        self.addConstraint(self.card_constraints, c)
        
    def addGroupCardConstraint(self,c):
        self.addConstraint(self.group_card_constraints, c)
        
    def addInheritanceConstraint(self,c):
        self.addConstraint(self.inheritance_constraints, c)
        
    def addRefConstraint(self,c):
        self.addConstraint(self.ref_constraints, c)

    def __str__(self):
        return str(self.claferSort.element.uid)
    
    def assertConstraints(self, cfr):
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
                self.assertConstraint(j,cfr)
    
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

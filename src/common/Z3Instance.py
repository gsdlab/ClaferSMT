'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from common import Common
from common.Common import debug_print, standard_print
from gi.overrides.keysyms import m
from visitors import Visitor, CreateSorts, CreateHierarchy, \
    CreateBracketedConstraints, ResolveClaferIds, PrintHierarchy
from z3 import *
import common

class Z3Instance(object):
    ''' 
    :var module: The Clafer AST
    :var z3_constraints: ([:mod:`constraints.Constraint`]) Contains ALL constraints that will be fed into z3.
    :var z3_sorts: ({str, :mod:`common.ClaferSort`}) Holds the Sorts for each clafer, 
        mapped by the clafer's ID.
    :var solver: (Z3_Solver) The actual Z3 solver. 
    :var scope: (int) The number of allowed clafers in the model.

    Stores and instantiates all necessary constraints for the ClaferZ3 model.
    '''
    def __init__(self, module):
        if(Common.MODE == Common.TEST):
            Common.reset()
        self.module = module
        self.model_count = 0
        self.z3_constraints = []
        self.z3_bracketed_constraints = []
        self.z3_sorts = {}
        self.unsat_core_trackers = []
        self.unsat_map = {}
        self.setOptions()
        self.solver = Solver() 
        self.solver.set(unsat_core=True)
        #self.solver.help()
        self.createCommonFunctions()
    
    def createGroupCardConstraints(self):
        for i in self.z3_sorts.values():
            i.addGroupCardConstraints()
            
    def createRefConstraints(self):
        for i in self.z3_sorts.values():
            i.addRefConstraints()
            
    def createCardinalityConstraints(self):
        for i in self.z3_sorts.values():
            i.createCardinalityConstraints()
    
    def mapColonClafers(self):
        for i in self.z3_sorts.values():
            if i.superSort:
                i.indexInSuper = i.superSort.addSubSort(i)     
    
    def assertConstraint(self, constraint):
        if Common.MODE != Common.DEBUG: 
            self.solver.add(constraint)
        if Common.MODE == Common.DEBUG:
            p = Bool("p" + str(Common.getConstraintUID()))
            self.unsat_core_trackers.append(p)
            self.unsat_map[str(p)] = constraint
            self.solver.add(Implies(p, constraint))
            #print(Implies(p, constraint))
        
    def createCommonFunctions(self):
        Common.bool2Int = Function("bool2Int", BoolSort(), IntSort())
        self.z3_constraints.append(Common.bool2Int(True) == 1)
        self.z3_constraints.append(Common.bool2Int(False) == 0)               
    
    def setOptions(self):
        set_option(max_depth=1000)
        set_option(max_args=1000)
        #set_option(max_width=1000)
        if Common.MODE == Common.DEBUG:
            set_option(auto_config=False)
    
    def run(self):
        '''
        :param module: The Clafer AST
        :type module: Module
        
        Converts Clafer constraints to Z3 constraints and computes models.
        '''
        Visitor.visit(CreateSorts.CreateSorts(self), self.module)
        Visitor.visit(ResolveClaferIds.ResolveClaferIds(self), self.module)
        Visitor.visit(CreateHierarchy.CreateHierarchy(self), self.module)
        
        debug_print("Creating cardinality constraints.")
        self.createCardinalityConstraints()
        
        debug_print("Mapping colon clafers.")
        self.mapColonClafers()
        
        #FIX for abstracts
        debug_print("Creating group cardinality constraints.")
        self.createGroupCardConstraints()
        
        debug_print("Creating ref constraints.")
        self.createRefConstraints()
                
        debug_print("Creating bracketed constraints.")
        Visitor.visit(CreateBracketedConstraints.CreateBracketedConstraints(self), self.module)
           
        self.assertConstraints()        
        
        #if(Common.MODE == Common.DEBUG):
        #    self.printConstraints()
        
        #for i in self.solver.assertions():
        #    print(i)
        #    print()
        
        #debug_print(self.solver.check(self.unsat_core_trackers))
        #core = self.solver.unsat_core()
        #debug_print(len(core))
        #debug_print(self.solver.unsat_core())
        debug_print("Getting models.")    
        models = self.get_models(-1)
        return len(models)
        
    def printVars(self, model):
        self.model_count = self.model_count + 1
        standard_print("###########################")
        standard_print("# Model: " + str(self.model_count))    
        standard_print("###########################")
        Visitor.visit(PrintHierarchy.PrintHierarchy(self, model), self.module)
        standard_print("")
    
    def assertConstraints(self):
        for i in self.z3_sorts.values():
            for j in i.constraints:
                self.assertConstraint(j)
        for i in self.z3_constraints:
            self.assertConstraint(i)
        for i in self.z3_bracketed_constraints:
            self.assertConstraint(i)
    
    def printConstraints(self):
        for i in self.z3_sorts.values():
            for j in i.constraints:
                debug_print(j)
        for i in self.z3_constraints:
            debug_print(i)
        for i in self.z3_bracketed_constraints:
            debug_print(i)
    
    #this is not my method, some stackoverflow or z3.codeplex.com method. Can't remember, should find it.
    def get_models(self, desired_number_of_models):
        result = []
        count = 0
        while True:
            
            if (Common.MODE != Common.DEBUG and self.solver.check() == sat and count != desired_number_of_models) or \
                (Common.MODE == Common.DEBUG and self.solver.check(self.unsat_core_trackers) == sat and count != desired_number_of_models):
                m = self.solver.model()
                #if count ==0:
                #    print(m)
                result.append(m)
                # Create a new constraint the blocks the current model
                block = []
                for d in m:
                    # d is a declaration
                    if d.arity() > 0:
                        continue #raise Z3Exception("uninterpreted functions are not supported")
                    # create a constant from declaration
                    c = d()
                    if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                        raise Z3Exception("arrays and uninterpreted sorts are not supported")
                    block.append(c != m[d])
                    #print(str(d) + " = " + str(m[d]))
                self.solver.add(Or(block))
                self.printVars(m)
                count += 1
            else:
                if Common.MODE == Common.DEBUG and count == 0:
                    debug_print(self.solver.check(self.unsat_core_trackers))
                    core = self.solver.unsat_core()
                    debug_print(len(core))
                    for i in core:
                        print(self.unsat_map[str(i)])
                        print()
                    return result
                if count == 0:
                    standard_print("UNSAT")
                return result
   
        
    ###############################
    # accessors                   #
    ###############################
    def getConstraints(self):
        ''''
        :returns: z3_constraints
        '''
        return self.z3_constraints
    
    def getSort(self, uid):
        return self.z3_sorts.get(uid)
        
    def getSorts(self): 
        '''
        :returns: z3_sorts
        '''
        return self.z3_sorts.values()
    
    ###############################
    # end accessors               # 
    ###############################
    
    ###############################
    # adders                      #
    ###############################
    def addConstraint(self, constraint):
        '''
        :param constraint: A constraint.
        :type constraint: :mod:`constraints.Constraint`
        '''
        self.z3_constraints.append(constraint)
        
    def addSort(self, sortID, sort):
        '''
        :param sortID: The uid of the Clafer
        :type sortID: str
        :param sort: A ClaferSort.
        :type sort: :mod:`common.ClaferSort`
        '''
        self.z3_sorts[sortID] = sort
        

    ###############################
    # end adders                  #
    ###############################
    
    def __str__(self):
        return (str(self.getSorts())) + "\n" +\
            ("\n".join(map(str,self.getConstraints())))
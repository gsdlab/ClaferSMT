'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from common import Common, Options, Clock
from common.Common import debug_print, standard_print
from constraints import Constraints, IsomorphismConstraint
from lxml.builder import basestring
from visitors import Visitor, CreateSorts, CreateHierarchy, \
    CreateBracketedConstraints, ResolveClaferIds, PrintHierarchy
from z3 import *
import common
import time


class Z3Instance(object):
    ''' 
    :var module: The Clafer AST

    Stores and instantiates all necessary constraints for the ClaferZ3 model.
    '''
    def __init__(self, module):
        if(Common.MODE == Common.TEST):
            Common.reset()
        self.module = module
        self.model_count = 0
        self.z3_bracketed_constraints = []
        self.z3_sorts = {}
        self.solver = Solver()
        self.setOptions()
        self.clock = Clock.Clock()
        #print(self.solver.help())
        #print(get_version_string())
        
        """ Create simple objects used to store Z3 constraints. """
        self.join_constraints = Constraints.GenericConstraints("Z3Instance")
        
        """ 
        Used to map constraints in the UNSAT core to Boolean variables.
        Will eventually be used to map UNSAT core back to the Clafer model.
        """
        self.unsat_core_trackers = []
        self.unsat_map = {}
        
        """ Create simple functions and constraints, that may be used in many places. """
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
         
    def createCommonFunctions(self):
        self.common_function_constraints = Constraints.GenericConstraints("Common")
        #self.common_function_constraints.addConstraint(Common.bool2Int(True) == 1)
        #self.common_function_constraints.addConstraint(Common.bool2Int(False) == 0)               
    
    def setOptions(self):
        """
        Sets basic options for the Z3 solver.
        Adds additional options for better pretty-printing, if debugging.
        """
        self.solver.set(unsat_core=True)
        
        if Common.MODE == Common.DEBUG:
            #set_option(max_width=2)
            set_option(max_depth=1000)
            set_option(max_args=1000)
            set_option(auto_config=False)
    
    def run(self):
        '''
        :param module: The Clafer AST
        :type module: Module
        
        Converts Clafer constraints to Z3 constraints and computes models.
        '''
        
        self.clock.tick("translation")
        
        """ Create a ClaferSort associated with each Clafer. """  
        Visitor.visit(CreateSorts.CreateSorts(self), self.module)
        
        """ Resolve any 'parent' or 'this' ClaferID's. """
        Visitor.visit(ResolveClaferIds.ResolveClaferIds(self), self.module)
        
        """ Add subclafers to the *fields* variable in the corresponding parent clafer. """
        Visitor.visit(CreateHierarchy.CreateHierarchy(self), self.module)
        
        debug_print("Creating cardinality constraints.")
        self.createCardinalityConstraints()
        
        debug_print("Creating ref constraints.")
        self.createRefConstraints()
        
        debug_print("Mapping colon clafers.")
        self.mapColonClafers()
        
        debug_print("Creating group cardinality constraints.")
        self.createGroupCardConstraints()
        
        debug_print("Creating bracketed constraints.")
        Visitor.visit(CreateBracketedConstraints.CreateBracketedConstraints(self), self.module)
           
        debug_print("Asserting constraints.")
        self.assertConstraints()     
        
        debug_print("Printing constraints.") 
        self.printConstraints()
    
        debug_print("Getting models.")  
        self.clock.tock("translation")
        models = self.get_models(Options.NUM_INSTANCES)
        
        self.clock.printEvents()
        
        return len(models)
        
    def printVars(self, model):
        self.clock.tick("printing")
        self.model_count = self.model_count + 1
        standard_print("###########################")
        standard_print("# Model: " + str(self.model_count))    
        standard_print("###########################")
        Visitor.visit(PrintHierarchy.PrintHierarchy(self, model), self.module)
        standard_print("")
        self.clock.tack("printing")
    
    def assertConstraints(self):
        for i in self.z3_sorts.values():
            i.constraints.assertConstraints(self)
        self.common_function_constraints.assertConstraints(self)
        self.join_constraints.assertConstraints(self)
        for i in self.z3_bracketed_constraints:
            i.assertConstraints(self)
    
    def printConstraints(self):
        if not (Common.MODE == Common.DEBUG and Options.PRINT_CONSTRAINTS):
            return
        for i in self.z3_sorts.values():
            i.constraints.print()
        self.join_constraints.print()
        for i in self.z3_bracketed_constraints:
            i.print()
        
    #this is not my method, some stackoverflow or z3.codeplex.com method. Can't remember, should find it.
    # i no longer need this method, if i implement the isomorphism detection
    def get_models(self, desired_number_of_models):
        result = []
        count = 0
        #print(self.solver.sexpr())
        self.clock.tick("first model")
        while True:
            self.clock.tick("unsat")
            if (Common.MODE != Common.DEBUG and self.solver.check() == sat and count != desired_number_of_models) or \
                (Common.MODE == Common.DEBUG and self.solver.check(self.unsat_core_trackers) == sat and count != desired_number_of_models):
                if count == 0:
                    self.clock.tock("first model")
                m = self.solver.model()
                #if count ==0:
                #print(m)
                result.append(m)
                #print(self.solver.statistics())
                # Create a new constraint the blocks the current model
                block = []
                for d in m:
                    # d is a declaration
                    if d.arity() > 0:
                        continue #raise Z3Exception("uninterpreted functions are not supported")
                    # create a constant from declaration
                    c = d()
                    if (str(c)).startswith("z3name!"):
                        continue
                    if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                        raise Z3Exception("arrays and uninterpreted sorts are not supported")
                    block.append(c != m[d])
                    #print(str(d) + " = " + str(m[d]))
                self.solver.add(Or(block))
                if not Common.MODE == Common.TEST:
                    self.printVars(m)
                if Options.GET_ISOMORPHISM_CONSTRAINT:
                    IsomorphismConstraint.IsomorphismConstraint(self, m).createIsomorphicConstraint()
                    self.printConstraints()
                    self.z3_bracketed_constraints.pop().assertConstraints(self)
                count += 1
            else:
                self.clock.tock("unsat")
                if Common.MODE == Common.DEBUG and count == 0:
                    debug_print(self.solver.check(self.unsat_core_trackers))
                    core = self.solver.unsat_core()
                    debug_print(len(core))
                    for i in core:
                        print(str(i) + " ==> " + str(self.unsat_map[str(i)]))
                        print()
                    return result
                if count == 0:
                    standard_print("UNSAT")
                return result
    
    def getSort(self, uid):
        return self.z3_sorts.get(uid)
        
    def getSorts(self): 
        '''
        :returns: z3_sorts
        '''
        return self.z3_sorts.values()
        
    def addSort(self, sortID, sort):
        '''
        :param sortID: The uid of the Clafer
        :type sortID: str
        :param sort: A ClaferSort.
        :type sort: :mod:`common.ClaferSort`
        '''
        self.z3_sorts[sortID] = sort
    
    def __str__(self):
        return (str(self.getSorts())) + "\n" +\
            ("\n".join(map(str,self.getConstraints())))
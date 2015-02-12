'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from ast.IntegerLiteral import IntegerLiteral
from common import Common, Options, Clock, Alloy
from common.Exceptions import UnusedAbstractException
from common.Options import debug_print, standard_print
from constraints import Translator, Constraints
from visitors import Visitor, CreateSorts, CreateHierarchy, ResolveClaferIds, PrintHierarchy, Initialize, \
    SetScopes, AdjustAbstracts, CheckForGoals
from z3 import Solver, set_option, sat, is_array, Or, Real, And, is_real, Int, \
    Goal, tactics, tactic_description, Tactic, SolverFor
from z3consts import Z3_UNINTERPRETED_SORT
from z3types import Z3Exception
import sys
import time
import z3



class UnscopedInstance(object):
    
    ''' 
    :var module: The Clafer AST

    Stores and instantiates all necessary constraints for the ClaferZ3 model.
    '''
    def __init__(self, module):
        Common.reset() #resets variables if in test mode
        self.EMPTYSTRING = Int("EMPTYSTRING")
        self.module = module
        self.cfr_bracketed_constraints = []
        self.cfr_sorts = {}
        self.relations = {}
        self.constraints = []
        #self.solver = SolverFor("QF_LIA")
        self.solver = z3.Solver()#z3.Then('simplify', 'qe', 'smt').solver()
        self.setOptions()
        self.clock = Clock.Clock()
        self.objectives = []
        self.goal = Goal()
        self.translator = Translator.Translator(self)
        
        """ Create simple objects used to store Z3 constraints. """
        self.join_constraints = Constraints.GenericConstraints("Z3Instance")
        
        """ 
        Used to map constraints in the UNSAT core to Boolean variables.
        Will eventually be used to map UNSAT core back to the Clafer model.
        """
        self.unsat_core_trackers = []
        self.unsat_map = {}
    
    def createGroupCardConstraints(self):
        for i in self.cfr_sorts.values():
            i.addGroupCardConstraints()
            
    def createRefConstraints(self):
        for i in self.cfr_sorts.values():
            i.addRefConstraints()
            
    def createCardinalityConstraints(self):
        for i in self.cfr_sorts.values():
            i.createCardinalityConstraints()
    
    def mapColonClafers(self):
        for i in self.cfr_sorts.values():
            if i.superSort:
                i.superSort.addSubSort(i)     
    
    def addSubSortConstraints(self):
        for i in self.cfr_sorts.values():
            if i.superSort:
                i.superSort.addSubSortConstraints(i)     
    
    def getScope(self, sort):
        if sort.element.isAbstract:
            summ = 0
            for i in sort.subs:
                summ = summ + self.getScope(i)
            return summ
        else:
            (_, upper) = sort.element.glCard
            return upper.value#sort.numInstances 
    
    def findUnusedAbstracts(self):
        for i in self.cfr_sorts.values():
            if i.element.isAbstract:
                summ = 0
                for j in i.subs:
                    summ = summ + self.getScope(j)
                if summ == 0:
                    raise UnusedAbstractException(i.element.uid)
    
    def setOptions(self):
        """
        Sets basic options for the Z3 solver.
        Adds additional options for better pretty-printing, if debugging.
        """
        self.solver.set(unsat_core=True)
        self.solver.set(model_completion=True)
        #self.solver.set('qi.eager_threshold',100)
        #self.solver.set('qi.lazy_threshold',100)
        #self.solver.set(produce_models=True)
        #set_option(auto_config=False)
        #set_option(candidate_models=True)
        if Options.MODE == Common.DEBUG:
            #these may not be necessary
            set_option(max_width=100)
            set_option(max_depth=1000)
            set_option(max_args=1000)
        set_option(auto_config=False)
    
    def run(self):
        '''
        :param module: The Clafer AST
        :type module: Module
        
        Converts Clafer constraints to Z3 constraints and computes models.
        '''
        try:
            self.clock.tick("translation")
            
            """ Create a ClaferSort associated with each Clafer. """  
            Visitor.visit(CreateSorts.CreateSorts(self), self.module)
            
            """ Resolve any 'parent' or 'this' ClaferID's. """
            Visitor.visit(ResolveClaferIds.ResolveClaferIds(self), self.module)
            
            """ Add subclafers to the *fields* variable in the corresponding parent clafer. Also handles supers and refs. """
            Visitor.visit(CreateHierarchy.CreateHierarchy(self), self.module)
            
            debug_print("Mapping colon clafers.")
            self.mapColonClafers()
          
            debug_print("Scopeless Initialization")
            Visitor.visit(Initialize.Scopeless_Initialize(self), self.module)
            
            #no overlapping subs
            for i in self.cfr_sorts.values():      
                if i.subs:
                    Alloy.noOverlappingSubs(self, i)

            debug_print("Asserting constraints.")
            self.assertConstraints()  
            start = time.clock()
            print("Solving")
            #print(self.solver.assertions())
            #print(self.solver.param_descrs())
            print(self.solver.check())
            stop = time.clock()
            print(stop - start)
            if self.solver.check() != sat:
                print(self.solver.unsat_core())
                return
            m = self.solver.model()
            #print(m)
            for i in self.cfr_sorts.values():
                if not i.superSort:
                    print(str(i) + " : " + str(m[i.sort]))

        except UnusedAbstractException as e:
            print(str(e))
            return 0
        
    
    def assertConstraints(self):
        for i in range(len(self.constraints)):
            #print(self.constraints[i])
            self.solver.assert_and_track(self.constraints[i], "p" + str(i))
            #self.solver.add(self.constraints[i])
        for i in self.cfr_sorts.values():
            i.constraints.assertConstraints(self)
        self.join_constraints.assertConstraints(self)
        for i in self.cfr_bracketed_constraints:
            i.assertConstraints(self)
    
    def getSort(self, uid):
        return self.cfr_sorts.get(uid)
        
    def getSorts(self): 
        ''' 
        :returns: z3_sorts
        '''
        return self.cfr_sorts.values()
        
    def addSort(self, sortID, sort):
        '''
        :param sortID: The uid of the Clafer
        :type sortID: str
        :param sort: A ClaferSort.
        :type sort: :mod:`common.ClaferSort`
        '''
        self.cfr_sorts[sortID] = sort
    
    def __str__(self):
        return (str(self.getSorts())) + "\n" +\
            ("\n".join(map(str,self.getConstraints())))

'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from ast.IntegerLiteral import IntegerLiteral
from common import Common, Options, Clock, SMTLib
from common.Common import preventSameModel, load, METRICS_MAXIMIZE
from common.Exceptions import UnusedAbstractException
from common.Options import debug_print, standard_print
from constraints import Constraints
from front import Z3Str, ModelStats
from gia.npGIAforZ3 import GuidedImprovementAlgorithmOptions, \
    GuidedImprovementAlgorithm
from parallel import ParSolver
from solvers import Z3Solver, Converters, BaseSolver
from visitors import Visitor, CreateSorts, CreateHierarchy, \
    CreateBracketedConstraints, ResolveClaferIds, PrintHierarchy, Initialize, \
    SetScopes, AdjustAbstracts, CheckForGoals
import sys
import traceback


class TracePrints(object):
    def __init__(self):    
        self.stdout = sys.stdout
    def write(self, s):
        self.stdout.write("Writing %r\n" % s)
        traceback.print_stack(file=self.stdout)

class ClaferModel(object):
    ''' 
    :var module: The Clafer AST

    Stores and instantiates all necessary constraints for the ClaferZ3 model.
    '''
    def __init__(self, module):
        Common.reset() #resets variables if in test mode
        self.EMPTYSTRING = SMTLib.SMT_Int("EMPTYSTRING")
        self.module = module
        self.smt_bracketed_constraints = []
        self.cfr_sorts = {}
        self.solver = BaseSolver.getSolver()
        self.setOptions()
        self.clock = Clock.Clock()
        self.objectives = []
        self.delimeter_count = 0
        
        """ Create simple objects used to store Z3 constraints. """
        self.join_constraints = Constraints.GenericConstraints("ClaferModel")
        
        """ 
        Used to map constraints in the UNSAT core to Boolean variables.
        """
        self.unsat_core_trackers = []
        self.low_level_unsat_core_trackers = {}
        self.unsat_map = {}
        self.translate()
    
    def createGroupCardConstraints(self):
        for i in self.cfr_sorts.values():
            i.addGroupCardConstraints()
            
    def createRefConstraints(self):
        for i in self.cfr_sorts.values():
            i.addRefConstraints()
            
    def createCardinalityConstraints(self):
        for i in self.cfr_sorts.values():
            i.createCardinalityConstraints()
    
    def createInstancesConstraintsAndFunctions(self):
        for i in self.cfr_sorts.values():
            i.getInstanceRanges()
        for i in self.cfr_sorts.values():
            if not i.beneathAnAbstract:
                i.computeKnownPolarities()
        for i in self.cfr_sorts.values():
            if i.element.isAbstract:
                i.fixAbstractExtraConstraints()
        for i in self.cfr_sorts.values():
            i.createInstancesConstraintsAndFunctions()
    
    def mapColonClafers(self):
        for i in self.cfr_sorts.values():
            if i.superSort:
                i.superSort.addSubSort(i)     
    
    def fixSubSortIndices(self):
        for i in self.cfr_sorts.values():
            i.currentSubIndex = 0
            for sub in i.subs:
                i.setSubSortIndex(sub)
    
    def addSubSortConstraints(self):
        for i in self.cfr_sorts.values():
            if i.superSort:
                i.superSort.addSubSortConstraints(i)     
                
    def setTopLevelIndices(self):
        for i in self.cfr_sorts.values():
            i.indexInHighestSuper = i.indexInSuper
            sup = i.superSort
            while sup:
                i.indexInHighestSuper = i.indexInHighestSuper + sup.indexInSuper
                i.highestSuperSort = sup
                sup = sup.superSort

    def setScopes(self):
        if Options.SCOPE_FILE != "" or Options.SCOPE_MAP_FILE != "":
            if Options.SCOPE_FILE == "" or Options.SCOPE_MAP_FILE == "":
                sys.exit("--scopemapfile requires --scopefile, and vice versa.")
            scopeJSON = Common.readJSONFile(Options.SCOPE_FILE)
            scopeDict = {}
            for i in scopeJSON:
                scopeDict[i["lpqName"]] = i["scope"]
            scopeMapJSON = Common.readJSONFile(Options.SCOPE_MAP_FILE)
            scopeMapDict = {}
            for i in scopeMapJSON:
                scopeMapDict[i["uid"]] = i["lpqName"]
            for i in self.cfr_sorts.values():
                uid = i.element.uid
                scope = scopeDict.get(scopeMapDict[uid],1)
                (glower, _) = i.element.glCard
                i.element.glCard = (glower, IntegerLiteral(scope))
        else:
            Visitor.visit(SetScopes.SetScopes(self), self.module)
            AdjustAbstracts.adjustAbstractsFixedPoint(self)
          
            
    def getScope(self, sort):
        if sort.element.isAbstract:
            summ = 0
            for i in sort.subs:
                summ = summ + self.getScope(i)
            return summ
        else:
            (_, upper) = sort.element.glCard
            return upper.value
    
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
        self.solver.setOptions()


    def isUsed(self, element):
        ab = self.cfr_sorts.get(str(element))
        if (not ab.element.isAbstract) or ab.scope_summ != 0:# self.cfr_sorts.get(str(element)):
            return True
        return False
    
    
    def translate(self):
        '''
        Converts Clafer constraints to Z3 constraints.
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
          
            debug_print("Adjusting instances for scopes.")
            self.setScopes()
            
            """ Initializing ClaferSorts and their instances. """
            Visitor.visit(Initialize.Initialize(self), self.module)
            self.fixSubSortIndices()
            self.createInstancesConstraintsAndFunctions()
              
            #for i in self.cfr_sorts.values():
            #    standard_print(str(i) + " : "+ str(i.numInstances))
            
            debug_print("Creating cardinality constraints.")
            self.createCardinalityConstraints()
            
            debug_print("Creating ref constraints.")
            self.createRefConstraints()
            
            debug_print("Adding subsort constraints.")
            self.addSubSortConstraints()
            self.setTopLevelIndices()
            
            debug_print("Creating group cardinality constraints.")
            self.createGroupCardConstraints()
                        
            debug_print("Creating bracketed constraints.")
            Visitor.visit(CreateBracketedConstraints.CreateBracketedConstraints(self), self.module)
            
            debug_print("Checking for goals.")
            if not Options.IGNORE_GOALS:
                Visitor.visit(CheckForGoals.CheckForGoals(self), self.module)
            
            self.clock.tock("translation")
            
        except UnusedAbstractException as e:
            print(str(e))
            return 0
    
    def run(self):
        '''
        :param module: The Clafer AST
        :type module: Module
        
         and computes models.
        '''
        
        if Options.MODE == Common.PRELOAD:
            return 0
    
        if Options.MODE == Common.MODELSTATS:
            ModelStats.run(self, self.module)
            return 0
    
        if Options.STRING_CONSTRAINTS:
            Converters.printZ3StrConstraints(self)
            Z3Str.clafer_to_z3str("z3str_in")
            return 1
        
        #for i in self.smt_bracketed_constraints:
        #    for j in i.constraints:
        #        print(SMTLib.toStr(j))
        
        #for i in self.cfr_sorts.values():
        #    print(i)
        #    print(i.instanceRanges)
        
        debug_print("Printing constraints.") 
        self.printConstraints()
        
        #sys.exit("DONE")
        self.clock.tick("Asserting Constraints")
        debug_print("Asserting constraints.")
        self.assertConstraints()     
        self.clock.tock("Asserting Constraints")
        print("Cache Hits: " + str(self.solver.converter.num_hit))
        print("Cache Misses: " + str(self.solver.converter.num_miss))
        
        if Options.SOLVER == "smt2":
            self.solver.printConstraints()
            sys.exit()
        
        
        #sys.exit()
        
        debug_print("Getting models.")  
        self.clock.tick("Get Models")
        models = self.get_models(Options.NUM_INSTANCES)
        self.clock.tock("Get Models")
        print(self.clock)
        self.num_models = len(models)
        
        if Options.LEARNING_ENVIRONMENT == "sharcnet":
            print(Options.SPLIT + str(Options.NUM_SPLIT))
            sys.exit("FIX SHARCNET")
             
        return self.num_models
        
    def printStartDelimeter(self):
        if Options.DELIMETER == Common.STANDARD_DELIMETER:
            standard_print("=== Instance " + str(self.delimeter_count+1) + " Begin ===")
            
            standard_print("")
        else:
            standard_print(Options.DELIMETER)
    
    def printEndDelimeter(self):
        if Options.DELIMETER == Common.STANDARD_DELIMETER:
            standard_print("--- Instance " + str(self.delimeter_count+1) + " End ---")
        self.delimeter_count = self.delimeter_count + 1
            
    def printVars(self, model):
        self.clock.tick("printing")
        self.printStartDelimeter()
        ph = PrintHierarchy.PrintHierarchy(self, model)
        Visitor.visit(ph, self.module)
        ph.printTree()
        standard_print("")
        self.printEndDelimeter()
        standard_print("")
        self.clock.tack("printing")
    
    def assertConstraints(self):
        self.clock.tick("Asserting basic constraints")
        for i in self.cfr_sorts.values():
            i.constraints.assertConstraints(self)
        self.join_constraints.assertConstraints(self)
        self.clock.tock("Asserting basic constraints")
        self.clock.tick("Asserting bracketed constraints")
        for i in self.smt_bracketed_constraints:
            i.assertConstraints(self)
        self.clock.tock("Asserting bracketed constraints")
    
    def printConstraints(self):
        if not (Options.MODE == Common.DEBUG and Options.PRINT_CONSTRAINTS):
            return
        #print(self.solver.sexpr())
        for i in self.cfr_sorts.values():
            i.constraints.debug_print()
        self.join_constraints.debug_print()
        for i in self.smt_bracketed_constraints:
            i.debug_print()
        print("Num lines of print: " + str(SMTLib.numCalls))
        
    def print_repl_help(self): 
        print("n -- get next model")
        print("r -- reset")
        print("i [num] -- increase (or decrease) the global scope by num (default=+1)")
        print("s num -- set scope to num")
        print("h -- help")
        print("q -- quit")
        
        
    def check_repl_input(self, args):
        if len(args) == 2 and args[0] in ['s', 'i'] and str(int(args[1])) == args[1]:
            return True
        else:
            print("Type h for help")
            return False
        
    def get_models(self, desired_number_of_models):
        if Options.MODE == Common.REPL:
            self.repl()
        elif Options.CORES == 1 and not self.objectives:
            return self.standard_get_models(desired_number_of_models)
        else:
            return self.GIA(desired_number_of_models)
        
    
    def GIA(self, desired_number_of_models):
        metrics_objective_direction = []
        metrics_variables = []

        for i in self.objectives:
            (pol, var) = i
            metrics_objective_direction.append(pol)
            metrics_variables.append(var)

        # Non-Parallel    
        GIAOptionsNP = GuidedImprovementAlgorithmOptions(verbosity=0, \
            incrementallyWriteLog=False, \
            writeTotalTimeFilename="timefile.csv", \
            writeRandomSeedsFilename="randomseed.csv", useCallLogs=False, num_models=desired_number_of_models, magnifying_glass=Options.MAGNIFYING_GLASS)    
        if Options.CORES == 1:
            GIAAlgorithmNP = GuidedImprovementAlgorithm(self, self.solver, metrics_variables, \
                    metrics_objective_direction, [], options=GIAOptionsNP) 
            '''featurevars instead of []'''
            outfilename = str("giaoutput").strip()#"npGIA_" + str(sys.argv[1]).strip() + ".csv"
    
            ParetoFront = GIAAlgorithmNP.ExecuteGuidedImprovementAlgorithm(outfilename)
            if not Options.SUPPRESS_MODELS:
                if not ParetoFront:
                    standard_print("UNSAT")
                for i in ParetoFront:
                    self.printVars(i)
            #count = count + 1
            return ParetoFront
        else:
            parSolver = ParSolver.ParSolver(self, self.module, self.solver, metrics_variables, metrics_objective_direction)
            ParetoFront = parSolver.run()   
            for i in ParetoFront:
                self.printStartDelimeter()
                standard_print(i)
                standard_print("")
                self.printEndDelimeter()
            return ParetoFront
            
    
    def standard_get_models(self, desired_number_of_models):
        result = []
        count = 0
        #print(self.solver.sexpr())
        self.clock.tick("first model")
        #for i in self.solver.assertions():
        #    print(i)
        while True:
            self.clock.tick("unsat")
            #print("AAAAA" + str(self.unsat_core_trackers))
            #print( self.solver.check(self.unsat_core_trackers) )
            #print(self.solver.check())
            #print(self.solver.solver.unsat_core())
            if (Options.MODE != Common.DEBUG and not(Options.PRODUCE_UNSAT_CORE) and self.solver.check() == Common.SAT and count != desired_number_of_models) or \
                (Options.MODE != Common.DEBUG and Options.PRODUCE_UNSAT_CORE and self.solver.check(self.unsat_core_trackers) == Common.SAT and count != desired_number_of_models) or \
                (Options.MODE == Common.DEBUG and self.solver.check(self.unsat_core_trackers) == Common.SAT and count != desired_number_of_models):
                if count == 0:
                    self.clock.tock("first model")
                m = self.solver.model()
                #if count ==0:
                #print(m)
                result.append(m)
                # Create a new constraint that blocks the current model
                #print(m)
                if not Options.SUPPRESS_MODELS:
                    self.printVars(m)
                preventSameModel(self, self.solver, m)
                count += 1
            else:
                if count == 0 and Options.PRODUCE_UNSAT_CORE:# Options.MODE == Common.DEBUG and count == 0:
                    self.clock.tock("unsat")
                    #debug_print(self.solver.check(self.unsat_core_trackers))
                    debug_print("UNSAT")
                    core = self.solver.unsat_core()
                    debug_print(str(len(core)) + " constraints in unsat core: \n")
                    for i in core:
                        print(Constraints.interpretUnsatCore(self, str(i)))
                        print()
                    return result
                elif count == 0:
                    standard_print("UNSAT")
                return result
    
    def repl(self):
        if Common.FIRST_REPL_LOOP:
            models = self.standard_get_models(1)
            if not models:
                print("No more instances")
        while True:
            ch = input("ClaferZ3 > ")
            #print(ch)
            ch = ch.strip()
            if ch == 'n':
                models = self.standard_get_models(1)
                if not models:
                    print("No more instances")
            elif ch == 'r':
                load(Options.FILE)
            elif ch.startswith('i'):
                args = ch.split()
                if self.check_repl_input(args):
                    inc = int(args[1])
                    Options.GLOBAL_SCOPE = Options.GLOBAL_SCOPE + inc
                    print("Global scope increased to " + str(Options.GLOBAL_SCOPE))
                    Common.FIRST_REPL_LOOP = False
                    load(Options.FILE)
            elif ch.startswith('s'):
                args = ch.split()
                if self.check_repl_input(args):
                    scope = int(args[1])
                    Options.GLOBAL_SCOPE = scope
                    print("Global scope set to " + str(Options.GLOBAL_SCOPE))
                    Common.FIRST_REPL_LOOP = False
                    load(Options.FILE)
            elif ch == 'q':
                sys.exit()
            elif ch == 'h':
                self.print_repl_help()
            else:
                print("Type h for help")
    
    
    def getSort(self, uid):
        return self.cfr_sorts.get(uid)
        
    def getSorts(self): 
        '''
        :returns: cfr_sorts
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

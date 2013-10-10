'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from common import Common, Options
from common.Common import debug_print, standard_print
from constraints import Constraints
from gi.overrides.keysyms import m
from lxml.builder import basestring
from visitors import Visitor, CreateSorts, CreateHierarchy, \
    CreateBracketedConstraints, ResolveClaferIds, PrintHierarchy, \
    IsomorphismConstraint
from z3 import *
import common
import time

class Z3Instance(object):
    ''' 
    :var module: The Clafer AST
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
        self.common_function_constraints = Constraints.GenericConstraints()
        self.join_constraints = Constraints.GenericConstraints()
        self.z3_bracketed_constraints = []
        self.z3_sorts = {}
        
        self.unsat_core_trackers = []
        self.unsat_map = {}
        self.setOptions()
        self.solver = Solver()
        self.solver.set(unsat_core=True)
        #self.solver.help()
        #print(get_version_string())
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
         
    #BROKEN but dont need
    def createTopologicalSort(self):
        '''
        TopSort over the DAG constructed by reference clafers
        Simplified algorithm due to the structure of Clafer 
        Note that we want the topsort in REVERSED order
        '''
        allSorts = list(self.getSorts())
        S = list(self.getSorts())
        for i in allSorts:
            if i.refSort and i.refSort in S:
                S.remove(i.refSort)
        #S -- nodes not pointed to
        L = [] #outputted top sort
        while S:
            n = S.pop()
            allSorts.remove(n)
            if n.refSort:
                flag = True
                for i in allSorts:
                    if i.refSort and i.refSort == n.refSort:
                        flag = False
                if flag:
                    S.append(n.refSort)    
            L.append(n)
        L.reverse()
        self.topological_sort = L
        print(self.topological_sort)

    def isOn(self, inst, sort):
        return int(str(inst)) != sort.parentInstances

    def getIsomorphicConstraint(self, model):
        assert isinstance(model, ModelRef)
        sorts = self.getSorts()
        instsMap = {}
        someStrings = []
        topCardStrings = []
        otherConstraints = []
        refConstraints = []
        #create the (some's
        for i in sorts:
            insts = []
            for j in range(len(i.instances)):
                ev = model.eval(i.instances[j])
                if self.isOn(ev, i):
                    insts.append(str(i) + "_" + str(j))
            currSome = "(some "
            instsMap[i.element.uid] = insts
            for j in range(len(insts) - 1):
                currSome = currSome + insts[j] + " ; "
            currSome = currSome + insts[-1] + " : " + i.element.nonUniqueID() + " | "
            someStrings.append(currSome)
        #handle top-level clafer cardinalities
        for i in sorts:
            if i.isTopLevel:
                insts = instsMap[i.element.uid]
                topCardStrings.append("#" + i.element.nonUniqueID() + " = " + str(len(insts)))
        #handle non-top level clafer cardinalities
        for i in sorts:
            for j in range(len(i.instances)):
                ev = model.eval(i.instances[j])
                if self.isOn(ev, i):
                    for k in i.fields:
                        currChildren = []
                        for l in range(len(k.instances)):
                            if str(model.eval(k.instances[l])) == str(j):
                                child = str(k) + "_" + str(l) 
                                currChildren.append(child)
                                otherConstraints.append(child \
                                      + " in " + str(i) + "_" + str(j) + "." \
                                      + k.element.nonUniqueID())
                        otherConstraints.append("#" + str(i) + "_" + str(j) + "." + k.element.nonUniqueID()\
                              + " = " + str(len(currChildren)))
                        for l in currChildren:
                            for m in currChildren:
                                if l != m:
                                    otherConstraints.append(l + " != " + m)
        #handle ref constraints
        for i in sorts: 
            if i.refSort:
                for j in range(len(i.instances)):
                    if self.isOn(model.eval(i.instances[j]), i):
                        if isinstance(i.refSort, basestring) and i.refSort == "integer":
                            refConstraints.append(str(i) + "_" + str(j) + ".ref = " + str(model.eval(i.refs[j])))
                        else:
                            refConstraints.append(str(i) + "_" + str(j) + ".ref = " + str(i.refSort) + "_" + str(model.eval(i.refs[j])))
        print("[ !(")
        for i in topCardStrings:
            print(i + " &&")
        for i in someStrings:
            print(i)
        print(" &&\n".join(otherConstraints + refConstraints))
        print(")"*(len(someStrings) + 1))
        print("]")
        
    def createCommonFunctions(self):
        return
        self.common_function_constraints.addConstraint(Common.bool2Int(True) == 1)
        self.common_function_constraints.addConstraint(Common.bool2Int(False) == 0)               
    
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
        if Options.PROFILING:
            self.initTime = time.clock()
        Visitor.visit(CreateSorts.CreateSorts(self), self.module)
        Visitor.visit(ResolveClaferIds.ResolveClaferIds(self), self.module)
        Visitor.visit(CreateHierarchy.CreateHierarchy(self), self.module)
        
        debug_print("Creating cardinality constraints.")
        self.createCardinalityConstraints()
        
        debug_print("Creating ref constraints.")
        self.createRefConstraints()
        
        debug_print("Mapping colon clafers.")
        self.mapColonClafers()
        
        #FIX for abstracts
        debug_print("Creating group cardinality constraints.")
        self.createGroupCardConstraints()
        
        debug_print("Creating bracketed constraints.")
        Visitor.visit(CreateBracketedConstraints.CreateBracketedConstraints(self), self.module)
           
        self.assertConstraints()        
        self.printConstraints()
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
        if Options.PROFILING:
            self.endTranslationTime = time.clock()  
        models = self.get_models(Options.NUM_INSTANCES)
        #print("Ticks: " + str(self.initTime) + " " + str(self.endTranslationTime) + " " + str(self.endOfFirstInstanceTime))
        if Options.PROFILING:
            print("Translation time:" + str(self.endTranslationTime - self.initTime))
            print("First Model time:" + str(self.endOfFirstInstanceTime - self.endTranslationTime))
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
            i.constraints.assertConstraints(self)
        self.common_function_constraints.assertConstraints(self)
        self.join_constraints.assertConstraints(self)
        for i in self.z3_bracketed_constraints:
            i.assertConstraints(self)
    
    def printConstraints(self):
        if not Common.MODE == Common.DEBUG:
            return
        for i in self.z3_sorts.values():
            i.constraints.print()
        self.join_constraints.print()
        for i in self.z3_bracketed_constraints:
            i.print()
        
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
                if Options.GET_ISOMORPHISM_CONSTRAINT:
                    self.getIsomorphicConstraint(m)
                if count == 0 and Options.PROFILING:
                    self.endOfFirstInstanceTime = time.clock()
                count += 1
            else:
                if Options.PROFILING:
                    self.endOfFirstInstanceTime = time.clock()
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
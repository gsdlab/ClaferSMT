'''
Created on Apr 30, 2013

@author: ezulkosk
'''


import sys
import time

from z3 import set_option, sat
import z3

from common import Common, Options, Clock, Alloy
from common.Exceptions import UnusedAbstractException
from constraints import Translator, Constraints
from jsir.IR import Abstract



INDENT="  "

class UnscopedInstance(object):
    
    ''' 
    :var module: The Clafer AST

    Stores and instantiates all necessary constraints for the ClaferZ3 model.
    '''
    def __init__(self, model):
        Common.reset() #resets variables if in test mode
        self.model = model
        self.cfr_bracketed_constraints = []
        #self.solver = SolverFor("QF_LIA")
        self.solver = z3.Solver()#z3.Then('simplify', 'qe', 'smt').solver()
        self.setOptions()
        self.clock = Clock.Clock()
        self.objectives = []
        self.translator = Translator.Translator(self)
        
        
        """ Create simple objects used to store Z3 constraints. """
        self.join_constraints = Constraints.GenericConstraints("Z3Instance")


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
    
    
    
    
    def print_children(self, m, p, i, indent = 0):
        for c in p.children:
            rname = Alloy.getRelationName(c, p)
            r = self.model.relations[rname]
            for ci in m[Alloy.T(c).sort]:
                if str(m.eval(r(ci,i))) == "True":
                    print(INDENT*indent + str(c.name+ "$" + str(c.print_count)))
                    c.print_count += 1
                    self.print_children(m, c, ci, indent+1)
                    
    
    def print_instance_h(self, m, c):
        for i in m[Alloy.T(c).sort]:
            if str(m.eval(c.isName(i))) == "True":
                print(c.name + "$" + str(c.print_count))
                c.print_count += 1
                self.print_children(m, c, i, indent=1)
             
    
    def print_instance(self, m):
        print("\nINSTANCE\n")
        for c in self.model.clafers:
            if not c.parent and not isinstance(c, Abstract):
                self.print_instance_h(m, c)
                
                
                    #print(m[Alloy.T(c).sort])
        return       
        sys.exit()
        
        for r in self.model.relations.values():
            print(m[r])
            domains = []
            for i in range(r.arity()):
                domains.append(r.domain(i))
            print(domains)
            for i in m[domains[0]]:
                print(i)
            
            sys.exit()
            
            print(m[i])
        pass
    
    def run(self):
        '''
        :param module: The Clafer AST
        :type module: Module
        
        Converts Clafer constraints to Z3 constraints and computes models.
        '''
        try:
            self.clock.tick("translation")
            
            '''
            Declares sort if top level,
            Creates isName and isA,
            Creates 2 consts per sort
            No child wo/parent
            '''
            for i in self.model.clafers:
                i.scopeless_initialize(self.model)
            
            '''
            No overlapping subs 
            '''
            for i in self.model.clafers:      
                if i.subs and len(i.subs) >= 2:
                    Alloy.noOverlappingSubs(self.model, i)
                    
            for i in self.model.clafers:
                Alloy.setCard(self.model, i)

            for i in self.model.assertions:
                #print(i)
                self.solver.add(i)
            
            #self.assertConstraints()  
            
            
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
            
            self.print_instance(m)
            #print(m)
            

                

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

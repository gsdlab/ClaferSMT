'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from visitors import Visitor, CreateSorts, CreateHierarchy, \
    CreateBracketedConstraints, CreateCardinalityConstraints
from z3 import *
import common

class Z3Instance(object):
    ''' 
    :var module: The Clafer AST
    :var z3_constraints: ([:mod:`constraints.Constraint`]) Contains ALL constraints that will be fed into z3.
    :var z3_sorts: ({str, :mod:`common.ClaferSort`}) Holds the Sorts for each clafer, 
        mapped by the clafer's ID.
    :var z3_datatypes: ({:mod:`common.ClaferSort`, :mod:`common.ClaferDatatype`}) 
        Maps each ClaferSort to its Datatype.
    :var solver: (Z3_Solver) The actual Z3 solver. 
    :var scope: (int) The number of allowed clafers in the model.

    Stores and instantiates all necessary constraints for the ClaferZ3 model.
    '''
    count = 1
    z3_constraints = []
    z3_sorts = {}
    z3_datatypes = {}
    
    def run(self, module, __DEBUG__ = False):
        '''
        :param __DEBUG__: Prints out debug statements if true.
        :type __DEBUG__: (bool (o)) 
        :param module: The Clafer AST
        :type module: Module
        
        Runs the Z3Instance.
        '''
        self.__DEBUG__ = __DEBUG__
        self.module = module
        self.scope = 20
        
        #Visitor.visit(PrettyPrint.PrettyPrint(), module)
        Visitor.visit(CreateSorts.CreateSorts(self), module)
        Visitor.visit(CreateHierarchy.CreateHierarchy(self), module)
        Visitor.visit(CreateBracketedConstraints.CreateBracketedConstraints(self), module)
        #Visitor.visit(CreateCardinalityConstraints.CreateCardinalityConstraints(self), module)
        
        self.solver = Solver()
        #self.instantiateSorts()
        #self.instantiateDatatypes()
        #self.instantiateConsts()
        #self.instantiateConstraints()
        #self.solver.add(axioms)
        
        self.addConstraints()
        #print(self.solver.sexpr())
        #print(self.solver.check())
        #self.model = self.solver.model()
        #self.printVars(self.model)
        models = self.get_models(self.solver, -1)
        #for i in models:
        #    self.printVars(i)

    
    def printVars(self, model):
        print("Model: " + str(self.count))
        self.count = self.count + 1
        for i in self.z3_sorts.values():
            for j in i.bits:
                if str(model.eval(j)) == "1":
                    print(j, model.eval(j))
        print("\n")
    
    def addConstraints(self):
        for i in self.z3_sorts.values():
            for j in i.constraints:
                self.solver.add(j)
    
    def get_models(self, s, M):
        result = []
        count = 0
        #s = Solver()
        #s.add(F)
        while True:
            if s.check() == sat and count != M:
                m = s.model()
                result.append(m)
                
                # Create a new constraint the blocks the current model
                block = []
                for d in m:
                    # d is a declaration
                    if d.arity() > 0:
                        raise Z3Exception("uninterpreted functions are not suppported")
                    # create a constant from declaration
                    c = d()
                    if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                        raise Z3Exception("arrays and uninterpreted sorts are not supported")
                    block.append(c != m[d])
                s.add(Or(block))
                self.printVars(m)
                count += 1
            else:
                return result
    
    def instantiateSorts(self):
        '''
        Declares z3 sorts.
        '''
        for i in self.z3_sorts.values():
            i.sort = DeclareSort(i.id)
        if(self.__DEBUG__):
            print("Sorts:")
            for i in self.z3_sorts.values():
                print("\t" + i.id)
    
    
    def instantiateDatatypes(self):
        '''
        Instantiates a Datatype for each ClaferSort, which will be used
            to create the Clafer hierarchy.
        '''
        for i in self.z3_datatypes.values():
            i.generateDatatype()
        if(self.__DEBUG__):
            print("Datatypes:")
            for i in self.z3_datatypes.values():
                print("\t" + str(i))
        self.instantiateDatatypes_h()
    
    def instantiateDatatypes_h(self):
        '''
        Creates all Z3 Datatypes at the same time. After invoking this method,
            each ClaferDatatype.datatype contains a pointer to the
            DataTypeSortRef, rather than the Datatype definition.
        '''
        datatypesList = list(CreateDatatypes(*[i.datatype for i in self.z3_datatypes.values()]))
        for claferDatatype, datatype in zip(self.z3_datatypes.values(), datatypesList):
            claferDatatype.datatype = datatype
    
    def instantiateConsts(self):
        '''
        Instantiate the necessary number of consts for each ClaferDatatype.
        '''
        for i in self.z3_sorts.values():
            i.consts = [Const(i.id+str(x),self.z3_datatypes[i].datatype) for x in range(i.numConsts)]
            
        if(self.__DEBUG__):
            print("Consts:")
            for i in self.z3_sorts.values():
                print("\t" + str(i.consts))
    
           
    def instantiateConstraints(self):
        '''
        Calls :meth:`generateConstraint` from each constraint.
        '''  
        for i in self.z3_constraints:
            self.solver.add(i.generateConstraint())
        if(self.__DEBUG__):
            print("Constraints:")
            for i in self.z3_constraints:
                print("\t" + i.comment)
                
    
        
    ###############################
    # accessors                   #
    ###############################
    def getConstraints(self):
        ''''
        :returns: z3_constraints
        '''
        return self.z3_constraints
        
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
        
    def addDatatype(self, claferSort, claferDatatype):
        '''
        :param claferSort: A ClaferSort.
        :type claferSort: :mod:`common.ClaferSort`
        :param claferDatatype: A ClaferDatatype.
        :type claferDatatype: :mod:`common.ClaferDatatype`
        
        Maps the given ClaferSort to the ClaferDatatype in z3_datatypes.
        '''
        self.z3_datatypes[claferSort] = claferDatatype
    ###############################
    # end adders                  #
    ###############################
    
    def __str__(self):
        return (str(self.getSorts())) + "\n" +\
            ("\n".join(map(str,self.getConstraints())))
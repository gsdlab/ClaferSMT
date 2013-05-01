'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from z3 import *
import common

class Z3Instance(object):
    '''
    z3_constraints([]): contains ALL constraints that will be fed into z3,
                        holds BracketedConstraint objects
    z3_sorts(map(str,ClaferSort)): defines the sorts for each clafer, 
                             mapped by the clafer's ID (str)
    z3_datatypes(map(ClaferSort,ClaferDatatype)): maps each ClaferSort to its
                                                  datatype
    solver (Solver): the actual Z3 solver
    '''
    z3_constraints = []
    z3_sorts = {}
    z3_datatypes = {}
    
    
    '''
    runs the z3 instance
    DONT FORGET TO INSTANTIATE EVERYTHING
    __DEBUG__ (optional bool): prints out debug statements if true
    '''
    def run(self, __DEBUG__ = False):
        self.__DEBUG__ = __DEBUG__
        
        self.instantiateSorts()
        self.instantiateConsts()
        self.instantiateDatatypes()
        self.instantiateConstraints()
        
        self.solver = Solver()
        #self.solver.add(axioms)
        print(self.solver.check())
        print(self.solver.model())
            
    '''
    declares z3 sorts
    '''
    def instantiateSorts(self):
        for i in self.z3_sorts.values():
            i.sort = DeclareSort(i.id)
        if(self.__DEBUG__):
            print("Sorts:")
            for i in self.z3_sorts.values():
                print("\t" + i.id)
    
    '''
    instantiate the necessary number of
    consts for each Sort
    '''
    def instantiateConsts(self):
        for i in self.z3_sorts.values():
            i.consts = [Const(i.id+str(x),i.sort) for x in range(i.numConsts)]
        if(self.__DEBUG__):
            print("Consts:")
            for i in self.z3_sorts.values():
                print("\t" + str(i.consts))
    
    '''
    calls generateConstraint() on each constraint
    '''         
    def instantiateConstraints(self):
        #for i in self.z3_constraints:
        #    generateConstraint(i)
        if(self.__DEBUG__):
            print("Constraints:")
            for i in self.z3_constraints:
                print("\t" + i.comment)
                
    def instantiateDatatypes(self):
        for i in self.z3_datatypes.values():
            i.generateDatatype()
        if(self.__DEBUG__):
            print("Datatypes:")
            for i in self.z3_datatypes.values():
                print("\t" + str(i))
        
    
    ###############################
    # accessors                   #
    ###############################
    def getConstraints(self):
        return self.z3_constraints
        
    def getSorts(self):
        return self.z3_sorts
    ###############################
    # end accessors               # 
    ###############################
    
    ###############################
    # adders                      #
    ###############################
    def addConstraint(self, constraint):
        self.z3_constraints.append(constraint)
        
    def addSort(self, sortID, sort):
        self.z3_sorts[sortID] = sort
        
    def addDatatype(self, claferSort, claferDatatype):
        self.z3_datatypes[claferSort] = claferDatatype
    ###############################
    # end adders                  #
    ###############################
    
    def __str__(self):
        return (str(self.getSorts())) + "\n" +\
            ("\n".join(map(str,self.getConstraints())))
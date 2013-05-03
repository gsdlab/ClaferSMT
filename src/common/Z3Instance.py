'''
Created on Apr 30, 2013

@author: ezulkosk
'''

from z3 import *
import common

class Z3Instance(object):
    ''' 
    :var z3_constraints: ([:mod:`constraints.Constraint`]) Contains ALL constraints that will be fed into z3.
    :var z3_sorts: ({str, :mod:`common.ClaferSort`}) Holds the Sorts for each clafer, 
        mapped by the clafer's ID.
    :var z3_datatypes: ({:mod:`common.ClaferSort`, :mod:`common.ClaferDatatype`}) 
        Maps each ClaferSort to its Datatype.
    :var solver: (Z3_Solver) The actual Z3 solver. 

    Stores and instantiates all necessary constraints for the ClaferZ3 model.
    '''
    
    z3_constraints = []
    z3_sorts = {}
    z3_datatypes = {}
    
    
    
    def run(self, __DEBUG__ = False):
        '''
        :param __DEBUG__: Prints out debug statements if true.
        :type __DEBUG__: (bool (o)) 
        
        Runs the Z3Instance.
        '''
        self.__DEBUG__ = __DEBUG__
        
        self.instantiateSorts()
        self.instantiateConsts()
        self.instantiateDatatypes()
        self.instantiateConstraints()
        
        self.solver = Solver()
        #self.solver.add(axioms)
        print(self.solver.check())
        print(self.solver.model())
            
    
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
    
    
    def instantiateConsts(self):
        '''
        Instantiate the necessary number of consts for each ClaferSort.
        '''
        for i in self.z3_sorts.values():
            i.consts = [Const(i.id+str(x),i.sort) for x in range(i.numConsts)]
        if(self.__DEBUG__):
            print("Consts:")
            for i in self.z3_sorts.values():
                print("\t" + str(i.consts))
    
           
    def instantiateConstraints(self):
        '''
        Calls :meth:`generateConstraint` from each constraint.
        '''  
        for i in self.z3_constraints:
            i.generateConstraint()
        if(self.__DEBUG__):
            print("Constraints:")
            for i in self.z3_constraints:
                print("\t" + i.comment)
                
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
        return self.z3_sorts
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
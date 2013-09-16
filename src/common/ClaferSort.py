'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from z3 import IntVector, Function, IntSort, If, BoolSort, Implies

class  ClaferSort(object):
    '''
    :var fields: ([:class:`~common.ClaferSort`]) List of all immediate subclafers.
    :var bits: ([BitVec]) List of 1-bit elements with total size equal to the global cardinality.
    :var partitions: (int) The number of "splits" in the bits list, such that
        >>> partitions  = glcard[1] / partitionSize
    :var partitionSize: (int) Essentially an alias to the clafer's upper cardinality constraint.
    :var constraints: contains all Z3 constraints associated with this clafer
    :var parentStack: The stack of parent clafers.
    :var refs:
    
    Contains necessary information for each clafer.
    
    '''
    
    
    def __init__(self, element, z3, stack):
        '''
        :param element: The clafer from the AST.
        :type name: Clafer
        :param z3: The Z3 instance
        :type z3: Z3Instance
        :param stack: The stack of parent clafers.
        :type stack: [ClaferSort]
        '''
        
        self.element = element
        self.z3 = z3
        self.parentStack = stack[:]
        self.fields = []
        self.constraints = []
        self.summs = []
        self.numInstances = int(self.element.glCard[1].value)
        self.instances = IntVector(self.element.uid.split("_",1)[1],self.numInstances)
        self.addInstancesConstraints()
        self.super = self.checkSuper()
        if(self.super != "clafer"):
            self.addRef()
        else:
            self.refs = []
        #self.removeIsomorphism()
        
        
        #for i in self.constraints:
        #   print(str(i) + "\n\n")
       
       
    def addGroupCardConstraints(self):
        if(len(self.fields) == 0):
            return
        #lower bounds
        upperGCard = self.element.gcard.interval[1].value
        lowerGCard = self.element.gcard.interval[0].value
        for i in range(self.numInstances):
            bigSumm = 0
            for j in self.fields:
                bigSumm = bigSumm +  j.summs[i]
            self.constraints.append(bigSumm >= lowerGCard)
            if upperGCard != -1:
                self.constraints.append(bigSumm <= upperGCard)
        
    def checkSuper(self):
        #assumes that "supers" can only have one element
        supers = self.element.supers
        return str(supers.elements[0].iExp[0].id)
        
    def addRef(self):
        pass
    
    def addField(self, claferSort):
        self.fields.append(claferSort)
    
    
    def addInstancesConstraints(self):
        #lower and upper bounds
        lowerCardConstraint = self.element.card[0].value
        upperCardConstraint = self.element.card[1].value
        
        #gets the upper card bound of the parent clafer
        if not self.parentStack:
            parent = None
            self.parentUpper = 1
            self.parentInstances = 1
        else:
            parent = self.parentStack[-1]
            self.parentUpper = parent.element.card[1].value
            self.parentInstances = len(parent.instances)
        
        for i in range(self.numInstances):
            #parent pointer is > 0
            self.constraints.append(self.instances[i] >= 0) 
            #parent pointer is < upper card of parent           
            self.constraints.append(self.instances[i] <= self.parentInstances)
            #sorted parent pointers
            if i != self.numInstances - 1:
                self.constraints.append(self.instances[i] <= self.instances[i+1])    
        
        #masks the instances that do not have the current parent 
        #mask(i,j): i == the parent number, j == the value of the child
        #outputs 1 if equal to parent, 0 otherwise
        self.mask = Function(self.element.uid + "_mask", IntSort(), IntSort(), IntSort())
        for i in range(self.parentInstances):    
            for j in range(self.numInstances):
                #print(str(i) + " " + str(j))
                self.constraints.append(self.mask(i, j) == If(i == self.instances[j], 1, 0))
        #mask should be replaced by this
        #self.correctMask = Function(self.element.uid + "_correctmask", IntSort(), IntSort(), IntSort())
        #for i in range(self.numInstances):
        #    for
        #self.constraints.append(ForAll([x,y], self.correctMask(x, y) == If(x == y, y, self.parentInstances)))
        #function that returns 1 for all instances that are on
        self.full = Function(self.element.uid + "_full", IntSort(), BoolSort())
        for i in range(self.numInstances):    
            self.constraints.append(self.full(i) == If(self.instances[i] != self.parentInstances, True, False))   
        #cardinality constraints
        for i in range(self.parentInstances):
            summ = 0;
            for j in range(self.numInstances):
               
                summ = summ +  self.mask(i, j)#self.instances[j])
            if parent:
                self.constraints.append(Implies(parent.instances[i] != parent.parentUpper,summ >= lowerCardConstraint))
                if upperCardConstraint != -1:
                    self.constraints.append(Implies(parent.instances[i] != parent.parentUpper,summ <= upperCardConstraint))
            else:
                self.constraints.append(summ >= lowerCardConstraint)
                if upperCardConstraint != -1:
                    self.constraints.append(summ <= upperCardConstraint)
            self.summs.append(summ)
        
        if not parent:
            return 
        #if the parent is not live, then no child can point to it  
        for i in range(parent.numInstances):
            for j in range(self.numInstances):
                self.constraints.append(Implies(parent.instances[i] == parent.parentUpper, self.instances[j] != i)) 
                
    
    
    def __str__(self):
        return self.element.uid + "_sort"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
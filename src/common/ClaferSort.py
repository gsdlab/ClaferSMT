'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from z3 import IntVector, Function, IntSort, If, BoolSort, Implies, And

class  ClaferSort(object):
    '''
    Conversion of clafer to z3 constraints.
    '''
    
    
    def __init__(self, element, z3, stack):
        self.element = element
        self.z3 = z3
        self.parentStack = stack[:]
        self.fields = []
        self.constraints = []
        self.summs = []
        self.numInstances = int(self.element.glCard[1].value)
        self.instances = IntVector(self.element.uid.split("_",1)[1],self.numInstances)
        self.refs = []
        self.subs = []
        self.indexInSuper = 0
        self.currentSubIndex = 0
        self.checkSuperAndRef()
        if(self.superSort):
            pass
        #gets the upper card bound of the parent clafer
        if not self.parentStack:
            self.parent = None
            self.parentUpper = 1
            self.parentInstances = 1
        else:
            self.parent = self.parentStack[-1]
            self.parentUpper = self.parent.element.card[1].value
            self.parentInstances = len(self.parent.instances)
        #lower and upper cardinality bounds
        self.lowerCardConstraint = self.element.card[0].value
        self.upperCardConstraint = self.element.card[1].value
        self.createInstancesConstraintsAndFunctions()
    
    def createInstancesConstraintsAndFunctions(self):
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
                self.constraints.append(self.mask(i, j) == If(i == self.instances[j], 1, 0))           
        #function that returns True for all instances that are on
        self.full = Function(self.element.uid + "_full", IntSort(), BoolSort())
        for i in range(self.numInstances):    
            self.constraints.append(self.full(i) == If(self.instances[i] != self.parentInstances, True, False)) 
        if not self.parent:
            return 
        #if the parent is not live, then no child can point to it  
        for i in range(self.parent.numInstances):
            for j in range(self.numInstances):
                self.constraints.append(Implies(self.parent.instances[i] == self.parent.parentUpper, self.instances[j] != i))    
        
        
    def createCardinalityConstraints(self):
        for i in range(self.parentInstances):
            summ = 0;
            for j in range(self.numInstances):
                summ = summ +  self.mask(i, j)
            if self.parent:
                self.constraints.append(Implies(self.parent.instances[i] != self.parent.parentUpper,summ >= self.lowerCardConstraint))
                if self.upperCardConstraint != -1:
                    self.constraints.append(Implies(self.parent.instances[i] != self.parent.parentUpper,summ <= self.upperCardConstraint))
            else:
                self.constraints.append(summ >= self.lowerCardConstraint)
                if self.upperCardConstraint != -1:
                    self.constraints.append(summ <= self.upperCardConstraint)
            self.summs.append(summ)
        
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
    
    def checkSuperAndRef(self):
        #assumes that "supers" can only have one element
        supers = self.element.supers
        if(supers.elements[0].iExp[0].id != "clafer"):
            if(supers.elements[0].type == "Ref"):
                self.refSort = self.z3.getSort(supers.elements[0].iExp[0].id)
                self.superSort = None
            else:
                self.refSort = None
                self.superSort = self.z3.getSort(supers.elements[0].iExp[0].id)
        else:
            self.superSort = None
            self.refSort = None
        
    def addRef(self):
        pass
    
    def addSubSort(self, sub):
        self.subs.append(sub)
        oldSubIndex = self.currentSubIndex
        self.currentSubIndex = self.currentSubIndex + sub.numInstances
        #the super cannot exist without the sub, and vice-versa
        for i in range(sub.numInstances):
            self.constraints.append(And(Implies(self.instances[i + oldSubIndex] != self.parentInstances, sub.instances[i] != sub.parentInstances),
                                         Implies(sub.instances[i] != sub.parentInstances,self.instances[i + oldSubIndex] != self.parentInstances)))
        return oldSubIndex
    
    def addField(self, claferSort):
        self.fields.append(claferSort)
    
    def __str__(self):
        return self.element.uid + "_sort"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.element.uid == other.element.uid
    
    def __hash__(self):
        return hash(self.id)
    
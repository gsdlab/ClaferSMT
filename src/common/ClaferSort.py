'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Common, Options
from constraints import Constraints
from lxml.builder import basestring
from z3 import IntVector, Function, IntSort, If, BoolSort, Implies, And, Bool



class  ClaferSort(object):
    '''
    :var element: The IR clafer.
    :var z3: The Z3Instance.
    :var parentStack: Used to determine the parent of the clafer, and if the clafer is top level.
    :var isTopLevel: True if the clafer is at the top level of indentation.
    :var fields: The direct subclafer ClaferSorts.
    :var constraints: The set of Z3 constraints associated with this clafer.
    :var summs: List containing useful information for processing cardinality constraints.
    :var numInstances: The number of Z3-Int instances used to represent this Clafer.
    :var instances: List of Z3-Ints representing the clafer. 
        An instance is *on* if it is not equal to the number of parentInstances.
    :var refs: List of Z3-ints representing the reference clafers that instances of this clafer point.
    :var subs: The list of ClaferSorts that directly inherit from this clafer.
    :var indexInSuper: Used to map a subinstance to the correct instances in the super. 
    
    Class representing a clafer in Z3 constraints. Clafers are represented as a list of 
    Z3-Int with a length equal to its global cardinality (for now). 
    The integers in the list represent which parent instance the corresponding instance
    points to. The range of the integers in the list is in [0,parentInstances]. An instance in this 
    list is considered *on* (that is, will appear in the outputted model), if it is not equal
    to parentInstances. If a clafer is top level, then an instance is on if it equals 0, else it is
    off. For example:
    
    >>> A 1..2 //A has global cardinality of 2
    >>>    B 1..3 //B has global cardinality 6
    >>> 
    >>> Instances for A: [0, 1]
    >>> Instances for B: [0, 0, 2, 2, 2, 2]
    >>> 
    >>> Corresponding output:
    >>>   A0
    >>>     B0
    >>>     B1
    
    Instance A0 is on because the first instance of A is 0. Instances B0 and B1 fall under
    A0 because the first and second instances are 0, that is, their parent pointers are 0.
    Instances B2-B5 are off because parentInstances for B is 2 (since there are 2 A's).
    '''
    def __init__(self, element, z3, stack):
        self.element = element
        self.z3 = z3
        self.parentStack = stack[:]
        if(not self.parentStack):
            self.isTopLevel = True
        else:
            self.isTopLevel = False
        self.fields = []
        self.constraints = Constraints.ClaferConstraints(self)
        self.summs = []
        self.numInstances = int(self.element.glCard[1].value)
        if(self.numInstances == -1):
            self.numInstances = Options.GLOBAL_SCOPE
        self.instances = IntVector(self.element.uid.split("_",1)[1],self.numInstances)
        self.refs = []
        self.subs = []
        self.indexInSuper = 0
        self.currentSubIndex = 0
        
        #gets the upper card bound of the parent clafer
        if not self.parentStack:
            self.parent = None
            self.parentUpper = 1
            self.parentInstances = 1
        else:
            self.parent = self.parentStack[-1]
            self.parentUpper = self.parent.element.card[1].value
            if self.parentUpper == -1:
                self.parentUpper = Options.GLOBAL_SCOPE
            self.parentInstances = len(self.parent.instances)
        #lower and upper cardinality bounds
        self.lowerCardConstraint = self.element.card[0].value
        self.upperCardConstraint = self.element.card[1].value
        #this eventually has to change
        if(self.upperCardConstraint == -1):
            self.upperCardConstraint = Options.GLOBAL_SCOPE
        self.createInstancesConstraintsAndFunctions()
    
    
    def getUnmaskedInstances(self, boolArray):
        '''
        Used in tandem with the new approach to splits and joins
        no use yet
        '''
        pass
    
    def getUnmaskedCount(self, boolArray):
        '''
        Used in tandem with the new approach to splits and joins
        '''
        count = 0
        for i in boolArray:
            if i:
                count = count + 1
        return count        
    
     
    def addRefConstraints(self):
        self.checkSuperAndRef()
        if(self.refSort):
            self.refs = IntVector(self.element.uid.split("_",1)[1] + "_ref",self.numInstances)
        if not self.refSort:
            return  
        if not isinstance(self.refSort, basestring):
            for i in range(self.numInstances):
                #refs pointer is >= 0
                self.constraints.addRefConstraint(self.refs[i] >= 0) 
                #ref pointer is <= upper card of ref parent           
                self.constraints.addRefConstraint(self.refs[i] <= self.refSort.numInstances)
        #if integer refs, zero out refs that do not have live parents,
        #if clafer refs, set equal to ref.parentInstances if not live   
        for i in range(self.numInstances):
            if isinstance(self.refSort, basestring):
                if self.refSort == "integer":
                    self.constraints.addRefConstraint(Implies(self.instances[i] == self.parentInstances, self.refs[i] == 0))    
            else:
                self.constraints.addRefConstraint(If(self.instances[i] == self.parentInstances
                                           , self.refs[i] == self.refSort.numInstances
                                           , self.refs[i] != self.refSort.numInstances))    
                #the clafer that the reference points to must be "on"
                self.constraints.addRefConstraint(Implies(self.refs[i] != self.refSort.numInstances
                                                     , self.refSort.full(self.refs[i]) == True))
                
    
    def createInstancesConstraintsAndFunctions(self):
        for i in range(self.numInstances):
            #parent pointer is >= 0
            self.constraints.addInstanceConstraint(self.instances[i] >= 0) 
            #parent pointer is <= upper card of parent           
            self.constraints.addInstanceConstraint(self.instances[i] <= self.parentInstances)
            #sorted parent pointers
            if(not self.element.isAbstract):
                if i != self.numInstances - 1:
                    self.constraints.addInstanceConstraint(self.instances[i] <= self.instances[i+1])    
        #masks the instances that do not have the current parent 
        #mask(i,j): i == the parent number, j == the value of the child
        #outputs 1 if equal to parent, 0 otherwise
        self.mask = Function(self.element.uid + "_mask", IntSort(), IntSort(), IntSort())
        for i in range(self.parentInstances):    
            for j in range(self.numInstances):
                self.constraints.addInstanceConstraint(self.mask(i, j) == If(i == self.instances[j], 1, 0))           
        #function that returns True for all instances that are on
        self.full = Function(self.element.uid + "_full", IntSort(), BoolSort())
        for i in range(self.numInstances):    
            self.constraints.addInstanceConstraint(self.full(i) == If(self.instances[i] != self.parentInstances, True, False)) 
        if not self.parent:
            return 
        #if the parent is not live, then no child can point to it  
        for i in range(self.parent.numInstances):
            for j in range(self.numInstances):
                self.constraints.addInstanceConstraint(Implies(self.parent.instances[i] == self.parent.parentUpper, self.instances[j] != i))    
        
        
    def createCardinalityConstraints(self):
        for i in range(self.parentInstances):
            summ = 0;
            for j in range(self.numInstances):
                summ = summ +  self.mask(i, j)
            if self.parent:
                self.constraints.addCardConstraint(Implies(self.parent.instances[i] != self.parent.parentUpper,summ >= self.lowerCardConstraint))
                if self.upperCardConstraint != -1:
                    self.constraints.addCardConstraint(Implies(self.parent.instances[i] != self.parent.parentUpper,summ <= self.upperCardConstraint))
            else:
                self.constraints.addCardConstraint(summ >= self.lowerCardConstraint)
                if self.upperCardConstraint != -1:
                    self.constraints.addCardConstraint(summ <= self.upperCardConstraint)
            self.summs.append(summ)
        
    def addGroupCardConstraints(self):
        if(len(self.fields) == 0 and ((not self.superSort) or self.superSort.fields == 0)):
            return
        #lower bounds
        upperGCard = self.element.gcard.interval[1].value
        lowerGCard = self.element.gcard.interval[0].value
        for i in range(self.numInstances):
            bigSumm = 0
            for j in self.fields:
                bigSumm = bigSumm +  j.summs[i]
            #don't include inherited fields for now
            #if self.superSort:
            #    for j in self.superSort.fields:
            #        bigSumm = bigSumm +  j.summs[i + self.indexInSuper]
            self.constraints.addGroupCardConstraint(bigSumm >= lowerGCard)
            if upperGCard != -1:
                self.constraints.addGroupCardConstraint(bigSumm <= upperGCard)
        
    
    def checkSuperAndRef(self):
        #assumes that "supers" can only have one element
        supers = self.element.supers
        if(supers.elements[0].iExp[0].id != "clafer"):
            if(supers.elements[0].type == "Ref"):
                ref_id = supers.elements[0].iExp[0].id
                if ref_id == "integer":
                    self.refSort = ref_id
                else:
                    self.refSort = self.z3.getSort(ref_id)
                self.superSort = None
            else:
                self.refSort = None
                self.superSort = self.z3.getSort(supers.elements[0].iExp[0].id)
        else:
            self.superSort = None
            self.refSort = None
       
    #mask all but the "current" instance for 'this' constraints   
    def maskForThis(self):
        instances = []
        for i in range(self.numInstances):
            instances.append([self.parentInstances if i != j else self.instances[j] 
                              for j in range(self.numInstances)])
        return instances
    
    def maskForOne(self, integer):
        return [self.parentInstances if integer != j else self.instances[j] 
                              for j in range(self.numInstances)]
     
    def addRef(self):
        pass
    
    def addSubSort(self, sub):
        self.subs.append(sub)
        oldSubIndex = self.currentSubIndex
        self.currentSubIndex = self.currentSubIndex + sub.numInstances
        #the super cannot exist without the sub, and vice-versa
        for i in range(sub.numInstances):
            self.constraints.addInheritanceConstraint(And(Implies(self.instances[i + oldSubIndex] != self.parentInstances, sub.instances[i] != sub.parentInstances),
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
    
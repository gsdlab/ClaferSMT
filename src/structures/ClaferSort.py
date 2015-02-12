'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Common, Options, SMTLib, Alloy
from common.Common import mOr, mAnd
from common.Options import standard_print
from constraints import Constraints
from z3 import IntVector, If, Implies, And, Or, Sum, Not, RealVector, Int, \
    Function, ForAll, Exists
import math
import operator
import sys
import z3







class  ClaferSort(object):
    '''
    :var element: The IR clafer.
    :var cfr: The Z3Instance.
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
    def __init__(self, element, cfr, stack):
        self.element = element
        self.cfr = cfr
        self.parentStack = stack[:]
        (_,upper) = self.element.card
        if upper.value == -1:
            self.unbounded = True
        else:
            self.unbounded = False
        if(not self.parentStack):
            self.isTopLevel = True
        else:
            self.isTopLevel = False
        self.fields = []
        self.constraints = Constraints.ClaferConstraints(self)
        self.summs = []
        self.refs = []
        self.subs = []
        self.full = None
        self.instanceRanges = []
        self.indexInSuper = 0
        self.currentSubIndex = 0
        self.myid = str(self.element)
        self.T = None
        self.scope_summ = -1
        self.numInstances = int(self.element.glCard[1].value)
        if(self.numInstances == -1):
            newScope = Options.GLOBAL_SCOPE
            self.numInstances = newScope
        #lower and upper cardinality bounds
        self.lowerCardConstraint = self.element.card[0].value
        self.upperCardConstraint = self.element.card[1].value
        #this eventually has to change
        #if(self.upperCardConstraint == -1):
        #    self.upperCardConstraint = Options.GLOBAL_SCOPE
        if not self.parentStack:
            self.parent = None
            self.parentInstances = 1
        else:
            self.parent = self.parentStack[-1]
            self.parentInstances = self.parent.numInstances
    
    
    def getConsts(self, count):
        t = Alloy.T(self)
        if len(t.consts) < count:
            for i in range(len(t.consts), count):
                t.consts.append(z3.Const(str(t.element) + '_' + str(i), t.sort))
        return t.consts[0:count]
    
    def getNewConst(self):
        t = Alloy.T(self)
        c = z3.Const(str(t.element) + '_' + str(len(t.consts)), t.sort)
        t.consts.append(c)
        return c

    def scopeless_initialize(self):
        #see Alloy-SMT paper, Integer Fig
        self.sort = Alloy.declareSort(self)
        #(self.sort, self.bounded_consts) = Alloy.declareBoundedSort(self)
        #self.isOn = Alloy.isOn(self)
        self.consts = []
        if self.sort:
            self.consts.append(z3.Const(str(self.element) + '_0', self.sort))
            self.consts.append(z3.Const(str(self.element) + '_1', self.sort))
        
        self.isName = Alloy.isName(self)
        
        if self.superSort:
            Alloy.isA(self.cfr, self, self.superSort)
            
        #no child wo/ parent
        if self.parent:
            Alloy.relation(self.cfr, self, self.parent, lone=True, some=True)
        
        
        
        #Alloy.setCard(self.cfr, self)
    
    '''
    def scopeless_initialize(self):
        #print(str(self.element))
        
        #see Alloy-SMT paper, Integer Fig
        self.sort = z3.DeclareSort(str(self.element))
        if self.superSort:
            self.T = self.superSort.sort
        else:
            self.T = self.sort
        self.consts = []
        self.consts.append(z3.Const(str(self.element) + '_0', self.sort))
        self.consts.append(z3.Const(str(self.element) + '_1', self.sort))
        self.is_sort = Function('is_' + str(self.element), self.sort, z3.BoolSort())
        self.card = Int('crd_' + str(self.element))
        self.ord = Function('ord_' + str(self.element), self.sort, z3.IntSort())
        self.inv = Function('inv_' + str(self.element), z3.IntSort(), self.sort)
        self.trig = Function('trig_' + str(self.element), z3.IntSort(), z3.BoolSort())
        xi = self.consts[0]
        i = z3.Int('i')
        self.constraints.addCardConstraint(And(self.card >= 0, Implies(self.card == 0, ForAll([xi], Not(self.is_sort(xi)))))) #5
        self.constraints.addCardConstraint(ForAll([xi], And(1 <= self.ord(xi), self.ord(xi) <= self.card))) #6
        self.constraints.addCardConstraint(ForAll([xi], self.inv(self.ord(xi)) == xi)) #7
        self.constraints.addCardConstraint(ForAll([i], Implies(And(1 <= i, i <= self.card), self.ord(self.inv(i)) == i))) #8
        self.constraints.addCardConstraint(ForAll([i], Implies(And(1 <= i, i <= self.card), self.is_sort(self.inv(i))), patterns=[self.trig(i)])) #9
        for j in range(3):
            k = max(1, 20*j)
            self.constraints.addCardConstraint(ForAll([i], Implies(0 < self.card, self.trig(k)))) #10
        self.constraints.addCardConstraint(ForAll([i], Implies(And(1 <= i, i < self.card), self.trig(i+1)),patterns=[self.trig(i)])) #11
        if self.isTopLevel:
            self.constraints.addCardConstraint(And(self.lowerCardConstraint <= self.card, self.card <= self.upperCardConstraint))
        
        #self.constraints.addCardConstraint(self.card == 28) #5
        #no child wo/ parent
        if self.parent:
            #todo
            #create card constraints for the relation...generalize alloysmt
            self.z3.translator.addParentChildRelation(self, self.parent, self.lowerCardConstraint, self.upperCardConstraint, self.parent.sort, self.sort)
    '''
        
    
    def initialize(self):
        (_, upper) = self.element.glCard
        self.numInstances = upper.value
        self.instances = SMTLib.SMT_IntVector(self.element.uid,self.numInstances, 
                                              bits=self.getBits(self.parentInstances+1))
        #gets the upper card bound of the parent clafer
        if not self.parentStack:
            self.parent = None
            self.parentInstances = 1
        else:
            self.parent = self.parentStack[-1]
            self.parentInstances = self.parent.numInstances
        self.createInstancesConstraintsAndFunctions()
    
    def addRefConstraints(self):
        if not self.refSort:
            return 
        elif isinstance(self.refSort, PrimitiveType) and self.refSort.type == "real":
            self.refs = SMTLib.SMT_RealVector(self.element.uid + "_ref",self.numInstances)
        elif isinstance(self.refSort, PrimitiveType):
            self.refs = SMTLib.SMT_IntVector(self.element.uid + "_ref",self.numInstances)
        else:
            self.refs = SMTLib.SMT_IntVector(self.element.uid + "_ref",self.numInstances, 
                                              bits=self.getBits(self.refSort.parentInstances+1))
         
        if not isinstance(self.refSort, PrimitiveType):
            for i in range(self.numInstances):
                #refs pointer is >= 0
                self.constraints.addRefConstraint(SMTLib.SMT_GE(self.refs[i], SMTLib.SMT_IntConst(0)))
                #ref pointer is <= upper card of ref parent           
                self.constraints.addRefConstraint(SMTLib.SMT_LE(self.refs[i], SMTLib.SMT_IntConst(self.refSort.numInstances)))
        #if integer refs, zero out refs that do not have live parents,
        #if clafer refs, set equal to ref.parentInstances if not live   
        
        
        #reference symmetry breaking
        if not self.element.isAbstract:
            for i in range(self.numInstances - 1):
                for j in range(i+1, self.numInstances):
                    if isinstance(self.refSort, PrimitiveType):
                        self.constraints.addRefConstraint(SMTLib.SMT_Implies(SMTLib.SMT_EQ(self.instances[i],self.instances[j]),
                                                              SMTLib.SMT_LE(self.refs[i], self.refs[j])))
                    else:
                        self.constraints.addRefConstraint(SMTLib.SMT_Implies(mAnd(SMTLib.SMT_NE(self.refs[i], SMTLib.SMT_IntConst(self.refSort.numInstances)),
                                                                                  SMTLib.SMT_EQ(self.instances[i], self.instances[j])),
                                                              SMTLib.SMT_LE(self.refs[i], self.refs[j])))

        
        for i in range(self.numInstances):
            if isinstance(self.refSort, PrimitiveType):
                if self.refSort == "integer":
                    self.constraints.addRefConstraint(SMTLib.SMT_Implies(self.isOff(i),
                                                                         SMTLib.SMT_EQ(self.refs[i], SMTLib.SMT_IntConst(0))),
                                                      self.canBeOff(i))
                elif self.refSort == "string":
                    if Options.STRING_CONSTRAINTS:
                        self.constraints.addRefConstraint(SMTLib.SMT_Implies(self.isOff(i), SMTLib.SMT_EQ(self.refs[i], self.cfr.EMPTYSTRING)),
                                                          self.canBeOff(i))
                    else:
                        self.constraints.addRefConstraint(SMTLib.SMT_Implies(self.isOff(i), SMTLib.SMT_EQ(self.refs[i], SMTLib.SMT_IntConst(0))),
                                                          self.canBeOff(i))
                else: 
                    self.constraints.addRefConstraint(SMTLib.SMT_Implies(self.isOff(i), SMTLib.SMT_EQ(self.refs[i], SMTLib.SMT_IntConst(0))),
                                                          self.canBeOff(i))
                    #sys.exit(str(self.refSort) + " not supported yet")
            else:
                if self.canBeOff(i):
                    self.constraints.addRefConstraint(SMTLib.SMT_If(self.isOff(i)
                                               , SMTLib.SMT_EQ(self.refs[i], SMTLib.SMT_IntConst(self.refSort.numInstances))
                                               , SMTLib.SMT_NE(self.refs[i], SMTLib.SMT_IntConst(self.refSort.numInstances))))
                else:
                    self.constraints.addRefConstraint(SMTLib.SMT_NE(self.refs[i], SMTLib.SMT_IntConst(self.refSort.numInstances)))
                #if refsort.full does not exist, create it
                if not self.refSort.full:
                    self.refSort.full = lambda x:mOr(*[SMTLib.SMT_And(SMTLib.SMT_EQ(x, SMTLib.SMT_IntConst(i)), self.refSort.isOn(i)) for i in range(self.refSort.numInstances)])
                #the clafer that the reference points to must be "on"
                self.constraints.addRefConstraint(SMTLib.SMT_Implies(SMTLib.SMT_NE(self.refs[i], SMTLib.SMT_IntConst(self.refSort.numInstances)),
                                                      self.refSort.full(self.refs[i])))
             
    
    def isOn(self, index):
        '''
        index is either an int or SMT-Int
        Returns a Boolean Constraint stating whether or not the instance at the given index is *on*.
        An instance is on if it is not set to self.parentInstances.
        '''
        #print(index)
        try:
            return SMTLib.SMT_NE(self.instances[index], SMTLib.SMT_IntConst(self.parentInstances))
        except:
            return SMTLib.SMT_NE(index, SMTLib.SMT_IntConst(self.parentInstances))
    
    def isOff(self, index):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given index is *off*.
        An instance is off if it is set to self.parentInstances.
        '''
        try:
            return SMTLib.SMT_EQ(self.instances[index], SMTLib.SMT_IntConst(self.parentInstances))
        except:
            return SMTLib.SMT_EQ(index, SMTLib.SMT_IntConst(self.parentInstances))
        
    def canBeOff(self, index):
        '''
        Used to determine if a particular instance may be absent from the model. 
        Used to simplify translation to SMT.
        '''
        try:
            (l,h,off) = self.instanceRanges[index]
            return off or h == self.parentInstances
        except:
            return True
    
       
       
    def getInstanceRange(self, index):
        '''
        Restricts the bounds of each instance.
        Returns (lower, upper, extraAbsenceConstraint), where 
        lower and upper are the bounds, and extraAbsenceConstraint
        is true if the instance may be absent from the model, AND is
        not covered by the upper bound.
        '''
        if not self.cfr.isUsed(self.element):
            return (0,0,False)
        
        if self.lowerCardConstraint == 0:
            upper = self.parentInstances # this is new upper = self.numInstances
        else:
            upper = index // self.lowerCardConstraint
        upper = min(upper, self.parentInstances)
        if self.upperCardConstraint == -1:
            lower = 0
        else:
            lower = index // self.upperCardConstraint
        
        if lower > upper:
            return (self.parentInstances, self.parentInstances, False)
           
        extraAbsenceConstraint = False
        #look at parentStack lower bounds, the loop computes the MINIMUM number of instances
        # of this clafer that MUST be in the model
        #essentially used to determine if the current instance may be out of the model
        if self.parentStack:
            parentCardBound = self.lowerCardConstraint #used to be 1
            for i in self.parentStack:
                parentCardBound = parentCardBound * i.lowerCardConstraint
            if parentCardBound - 1 < index and upper != self.parentInstances: 
                if upper + 1 == self.parentInstances:
                    upper = upper + 1
                else:
                    extraAbsenceConstraint = True
        return (lower, upper, extraAbsenceConstraint)
    
    def createInstancesConstraintsAndFunctions(self):
        self.instanceRanges = [self.getInstanceRange(i) for i in range(self.numInstances)]
        for i in range(self.numInstances):
            (lower, upper, extraAbsenceConstraint) = self.instanceRanges[i]
            
            #lower == upper case (simpler)
            if lower == upper:
                constraint = SMTLib.SMT_EQ(self.instances[i], SMTLib.SMT_IntConst(upper))
                if extraAbsenceConstraint:
                    self.constraints.addInstanceConstraint(SMTLib.SMT_Or(self.isOff(i), constraint))
                else:
                    self.constraints.addInstanceConstraint(constraint)
            else:
                #parent pointer is >= lower
                self.constraints.addInstanceConstraint(SMTLib.SMT_GE(self.instances[i],SMTLib.SMT_IntConst(lower)))
                constraint = SMTLib.SMT_LE(self.instances[i], SMTLib.SMT_IntConst(upper))
                if extraAbsenceConstraint: 
                    #parent pointer is <= upper , or equal to parentInstances
                    self.constraints.addInstanceConstraint(SMTLib.SMT_Or(self.isOff(i), constraint))        
                else:
                    #parent pointer is <= upper
                    self.constraints.addInstanceConstraint(constraint)
            
            #sorted parent pointers (only consider things that are not part of an abstract)
            if(not self.element.isAbstract and not (True in [(p.element.isAbstract) for p in self.parentStack])):
                #print(self.element)
                if i != self.numInstances - 1:
                    self.constraints.addInstanceConstraint(SMTLib.SMT_LE(self.instances[i],self.instances[i+1]))    
        if not self.parent:
            return 
        #if the parent is not live, then no child can point to it  
        for i in range(self.parent.numInstances):
            for j in range(self.numInstances):
                self.constraints.addInstanceConstraint(SMTLib.SMT_Implies(self.parent.isOff(i),
                                                                          SMTLib.SMT_NE(self.instances[j], SMTLib.SMT_IntConst(i))),
                                                       self.parent.canBeOff(i))
        
    
    def createCardinalityConstraints(self):
        if not self.cfr.isUsed(self.element):
            return
        self.summs = [[] for i in range(self.parentInstances+1)]
        for i in range(self.numInstances):
            (lower, upper, _) = self.getInstanceRange(i)
            for j in range(lower, upper + 1):
                self.summs[j].append(SMTLib.SMT_If(SMTLib.SMT_EQ(self.instances[i], SMTLib.SMT_IntConst(j)),
                                                   SMTLib.SMT_IntConst(1),
                                                   SMTLib.SMT_IntConst(0)))
        for i in range(len(self.summs)):
            if self.summs[i]:
                self.summs[i] = SMTLib.SMT_Sum(*[self.summs[i]])
            else:
                self.summs[i] = SMTLib.SMT_IntConst(0)
        for i in range(self.parentInstances):
            if self.parent:
                self.constraints.addCardConstraint(SMTLib.SMT_Implies(self.parent.isOn(i),
                                                                      SMTLib.SMT_GE(self.summs[i], SMTLib.SMT_IntConst(self.lowerCardConstraint))))
                if self.upperCardConstraint != -1:
                    self.constraints.addCardConstraint(SMTLib.SMT_Implies(self.parent.isOn(i),
                                                                          SMTLib.SMT_LE(self.summs[i], SMTLib.SMT_IntConst(self.upperCardConstraint))))
            else:
                self.constraints.addCardConstraint(SMTLib.SMT_GE(self.summs[i], SMTLib.SMT_IntConst(self.lowerCardConstraint)))
                if self.upperCardConstraint != -1:
                    self.constraints.addCardConstraint(SMTLib.SMT_LE(self.summs[i], SMTLib.SMT_IntConst(self.upperCardConstraint)))
        
    def addGroupCardConstraints(self):
        #print(str(self) + str(self.element.gcard.interval))
        self.upperGCard = self.element.gcard.interval[1].value
        self.lowerGCard = self.element.gcard.interval[0].value
        if(len(self.fields) == 0 and ((not self.superSort) or self.superSort.fields == 0)):
            return
        #lower bounds
        if not self.fields:
            return # front end is broken imo...
        if self.lowerGCard == 0 and self.upperGCard == -1:
            return
        for i in range(self.numInstances):
            
            bigSumm = SMTLib.SMT_IntConst(0)
            for j in self.fields:
                bigSumm = SMTLib.SMT_Plus(bigSumm, j.summs[i])
            #**** LEAVE THIS CODE ****
            #don't include inherited fields for now 
            #if self.superSort:
            #    for j in self.superSort.fields:
            #        print("found " + str(j))
            #        bigSumm = bigSumm +  j.summs[i + self.indexInSuper]
            if self.lowerGCard != 0:
                    self.constraints.addGroupCardConstraint(SMTLib.SMT_Implies(self.isOn(i),
                                                                               SMTLib.SMT_GE(bigSumm, SMTLib.SMT_IntConst(self.lowerGCard))))
            if self.upperGCard != -1:
                self.constraints.addGroupCardConstraint(SMTLib.SMT_Implies(self.isOn(i),
                                                                           SMTLib.SMT_LE(bigSumm, SMTLib.SMT_IntConst(self.upperGCard))))
            #print(str(self) +  " " + str(lowerGCard) + " " + str(upperGCard) + str(bigSumm))
        
    
    def checkSuperAndRef(self):
        #THIS IS A HACK BECAUSE THE IR IS NOW BROKEN.
        supers = self.element.supers
        ID = supers.elements[0].iExp[0].id
        TYPE = supers.elements[0].type
        if(ID != "clafer"):
            if(not TYPE):
                ref_id = supers.elements[0].iExp[0].id
                if ref_id == "int":
                    ref_id = "integer"
                if ref_id == "integer" or ref_id == "string" or ref_id == "real":
                    self.refSort = PrimitiveType(ref_id)
                else:
                    self.refSort = self.cfr.getSort(ref_id)
                self.superSort = None
            else:
                self.refSort = None
                self.superSort = self.cfr.getSort(supers.elements[0].iExp[0].id)
        else:
            self.superSort = None
            self.refSort = None
     
    def addRef(self):
        pass
    
    
    def addSubSortConstraints(self, sub):
        #the super cannot exist without the sub, and vice-versa
        oldSubIndex = self.currentSubIndex
        sub.indexInSuper = oldSubIndex
        self.currentSubIndex = self.currentSubIndex + sub.numInstances
        for i in range(sub.numInstances):
            self.constraints.addInheritanceConstraint(SMTLib.SMT_And(SMTLib.SMT_Implies(self.isOn(i + sub.indexInSuper), sub.isOn(i)),
                                         SMTLib.SMT_Implies(sub.isOn(i),self.isOn(i + sub.indexInSuper))))
    
    def addSubSort(self, sub):
        self.subs.append(sub)
        
        
    def addField(self, claferSort):
        self.fields.append(claferSort)
    
    def __str__(self):
        return self.element.uid + "_sort"
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        return str(self) <  str(other)
    
    def __eq__(self, other):
        return self.element.uid == other.element.uid
    
    def __hash__(self):
        return hash(self.id)
    
    

    
class PrimitiveType():
    def __init__(self, type):
        self.type = type
        
    def __eq__(self, other):
        return self.type == other
    
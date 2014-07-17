'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Common, Options, SMTLib
from common.Common import mOr, mAnd
from common.Options import standard_print
from constraints import Constraints
import math
import operator
import sys




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
        self.marked = False
        self.instanceRanges = []
        self.knownPolarities = []
        self.indexInSuper = 0
        self.indexInHighestSuper = 0
        self.highestSuperSort = self
        self.currentSubIndex = 0
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
        self.beneathAnAbstract = self.element.isAbstract or (True in [(p.element.isAbstract) for p in self.parentStack])
    
    
    #should get longest numInstances for getBits
    def getBits(self, instances):
        if Options.USE_BITVECTORS:
            bits = math.ceil(math.log(instances,2))
            sys.exit("GetBits is still hacked")
            
            return bits + 3
        return None
    
    def initialize(self):
        #TODO this should just use the current value of numInstances...
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
                                                      self.known_polarity(i, local=True) != Common.DEFINITELY_ON)
                elif self.refSort == "string":
                    if Options.STRING_CONSTRAINTS:
                        self.constraints.addRefConstraint(SMTLib.SMT_Implies(self.isOff(i), SMTLib.SMT_EQ(self.refs[i], self.cfr.EMPTYSTRING)),
                                                          self.known_polarity(i, local=True) != Common.DEFINITELY_ON)
                    else:
                        self.constraints.addRefConstraint(SMTLib.SMT_Implies(self.isOff(i), SMTLib.SMT_EQ(self.refs[i], SMTLib.SMT_IntConst(0))),
                                                          self.known_polarity(i, local=True) != Common.DEFINITELY_ON)
                else: 
                    self.constraints.addRefConstraint(SMTLib.SMT_Implies(self.isOff(i), SMTLib.SMT_EQ(self.refs[i], SMTLib.SMT_IntConst(0))),
                                                          self.known_polarity(i, local=True) != Common.DEFINITELY_ON)
                    #sys.exit(str(self.refSort) + " not supported yet")
            else:
                if self.known_polarity(i, local=True) != Common.DEFINITELY_ON:
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
        
    def known_polarity(self, index, local=False):
        '''
        Used to determine if a particular instance may be absent from the model. 
        Used to simplify translation to SMT.
        
        local= if set to true, do not consider subsorts
        '''
        try:
            (l,h,off) = self.instanceRanges[index]
            #if sub is definitely on, so is super => if still unknown, check polarity of sub at that index
            if off or h == self.parentInstances:
                if l != self.parentInstances:
                    if self.subs and not local:
                        for sub in self.subs:
                            if sub.indexInSuper <= index and index < sub.indexInSuper + sub.numInstances:
                                return sub.known_polarity(index - sub.indexInSuper)
                    return Common.UNKNOWN
                else:
                    return Common.DEFINITELY_OFF
            else:
                return Common.DEFINITELY_ON
        except:
            sys.exit("Bug in known_polarity")
            return Common.UNKNOWN   
       
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
            upper = self.parentInstances 
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
    
   
    def fixAbstractFields(self):
        for i in range(self.numInstances):
            (l,h,_) = self.instanceRanges[i]
            polarity = Common.DEFINITELY_OFF
            all_on_flag = True
            for j in range(l,min(self.parentInstances,h+1)):
                par_polarity = self.parent.knownPolarities[j]
                if not par_polarity == Common.DEFINITELY_ON:
                    all_on_flag = False
                if par_polarity == Common.UNKNOWN:
                    polarity = Common.UNKNOWN
            if all_on_flag:
                polarity = Common.DEFINITELY_ON
            self.knownPolarities.append(polarity)
            if polarity == Common.DEFINITELY_ON:
                if h == self.parentInstances:
                    h = h - 1
                self.instanceRanges[i] = (l,h,False)
        for f in self.fields:
            f.fixAbstractFields()
        
    def fixAbstractExtraConstraints(self):
        #sets the known_polarities of abstracts and their fields, and patches extraAbsenceConstraints
        self.knownPolarities = [0 for i in range(self.numInstances)]
        for sub in self.subs:
            if not sub.knownPolarities:
                sub.fixAbstractExtraConstraints()
            for i in range(sub.numInstances):
                sub_pol = sub.knownPolarities[i]
                currIndexInSuper = sub.indexInSuper + i
                self.knownPolarities[currIndexInSuper] = sub_pol
                (l,h,e) = self.instanceRanges[currIndexInSuper]
                if sub_pol == Common.DEFINITELY_ON:
                    if h == self.parentInstances:
                        h = h - 1
                    self.instanceRanges[currIndexInSuper] = (l,h,False)
        for f in self.fields:
            f.fixAbstractFields()
        
    def computeKnownPolarities(self):
        self.knownPolarities = [self.known_polarity(i) for i in range(self.numInstances)]
    
    def getInstanceRanges(self):
        self.instanceRanges = [self.getInstanceRange(i) for i in range(self.numInstances)]
    
    def createInstancesConstraintsAndFunctions(self):
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
            if not self.beneathAnAbstract:
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
                                                       self.parent.known_polarity(i, local=True) != Common.DEFINITELY_ON)
        
    
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
        
        for i in range(sub.numInstances):
            self.constraints.addInheritanceConstraint(SMTLib.SMT_And(SMTLib.SMT_Implies(self.isOn(i + sub.indexInSuper), sub.isOn(i)),
                                         SMTLib.SMT_Implies(sub.isOn(i),self.isOn(i + sub.indexInSuper))))
    
    def addSubSort(self, sub):
        self.subs.append(sub)
        oldSubIndex = self.currentSubIndex
        sub.indexInSuper = oldSubIndex
        self.currentSubIndex = self.currentSubIndex + sub.numInstances
        
        
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
        return hash(self.element.uid)
    
    
class BoolSort():
    
    def isOn(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given arg is *on*.
        '''
        return arg
    
    def isOff(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given index is *off*.
        '''
        return SMTLib.SMT_Not(self.isOn(arg))
    
    def __lt__(self, other):
        return not isinstance(other, BoolSort())
        
    
    def __eq__(self, other):
        return isinstance(other, BoolSort())
    
    def __str__(self):
        return "BoolSort"
    
    def __repr__(self):
        return self.__str__()
    

class StringSort():
    
    def __init__(self):
        from structures.ExprArg import Mask
        self.cardinalityMask = Mask()
        self.index = 0
        self.indexInHighestSuper = 0
        self.highestSuperSort = self
        
    def isOn(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given arg is *on*.
        '''
        return self.cardinalityMask.get(arg)
    
    def isOff(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given index is *off*.
        '''
        return not self.isOn(arg)
    
    def getNextIndex(self):
        self.index = self.index + 1
        return self.index - 1
    
    def getCardinalityMask(self):
        return self.cardinalityMask
    
    def __lt__(self, other):
        return not (isinstance(other, IntSort) or isinstance(other, BoolSort) or isinstance(other, StringSort))
        
    
    def __eq__(self, other):
        return isinstance(other, StringSort)
    
    def __str__(self):
        return "StringSort"
    
    def __repr__(self):
        return self.__str__()    

    def __hash__(self):
        return hash("stringsort")
    
class IntSort():
    
    def __init__(self):
        from structures.ExprArg import Mask
        self.cardinalityMask = Mask()
        self.index = 0
        self.indexInHighestSuper = 0
        self.highestSuperSort = self
        
    def isOn(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given arg is *on*.
        '''
        return self.cardinalityMask.get(arg)
    
    def isOff(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given index is *off*.
        '''
        return SMTLib.SMT_Not(self.isOn(arg))
    
    def getNextIndex(self):
        self.index = self.index + 1
        return self.index - 1
    
    def getCardinalityMask(self):
        return self.cardinalityMask
    
    def __lt__(self, other):
        return not (isinstance(other, IntSort) or isinstance(other, BoolSort))
        
    
    def __eq__(self, other):
        return isinstance(other, IntSort)
    
    def __hash__(self):
        return hash("intsort")
    
    
class RealSort():
    
    def __init__(self):
        from structures.ExprArg import Mask
        self.cardinalityMask = Mask()
        self.index = 0
        self.indexInHighestSuper = 0
        self.highestSuperSort = self
        
    def isOn(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given arg is *on*.
        '''
        return self.cardinalityMask.get(arg)
    
    def isOff(self, arg):
        '''
        Returns a Boolean Constraint stating whether or not the instance at the given index is *off*.
        '''
        return SMTLib.SMT_Not(self.isOn(arg))
    
    def getNextIndex(self):
        self.index = self.index + 1
        return self.index - 1
    
    def getCardinalityMask(self):
        return self.cardinalityMask
    
    def __lt__(self, other):
        return not (isinstance(other, IntSort) or isinstance(other, BoolSort) or isinstance(other, StringSort))
        
    
    def __eq__(self, other):
        return isinstance(other, IntSort)
    
    
    def __str__(self):
        return "RealSort"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash("realsort")
    
class PrimitiveType():
    '''
    corresponds to 'ref' and 'parent'
    '''
    def __init__(self, type):
        self.type = type
        
    def __eq__(self, other):
        return self.type == other
    
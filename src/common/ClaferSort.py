'''
Created on Apr 29, 2013

@author: ezulkosk
'''

from z3 import *
import math

#FIXME stack needs to be changed to only the IMMEDIATE parent of the clafer
def live(index, glcard, stack):
    #if stack is empty, top level clafer (MAYBE), exit
    if not stack:
        return True
    mult = glcard
    #stack.reverse()
    bits = BitVecVal(1,1)
    for i in [stack[-1]]:#stack: 
        mult = int(mult / i.element.card[1].value)
        bits &= i.bits[int(index/mult)]
        index -= int(index/mult) * mult 
    return bits == 1

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
        self.parentStack = stack
        self.fields = []
        self.constraints = []
        self.setCardinalityConstraints()
        self.super = self.checkSuper()
        if(self.super != "clafer"):
            self.addRef()
        else:
            self.refs = []
        #self.removeIsomorphism()
        
        
        #for i in self.constraints:
        #   print(str(i) + "\n\n")
        
    def checkSuper(self):
        #assumes that "supers" can only have one element
        supers = self.element.supers
        return str(supers.elements[0].iExp[0].id)
        
    def addRef(self):
        self.refs = [ Int(str(i) + "_ref") for i in self.bits ]
        self.constraints.extend([Implies(i == 0, j == 0) for i,j in zip(self.bits, self.refs)])
        #print(self.refs)        
        
    
    def addField(self, claferSort):
        '''
        :param claferSort: ClaferSort for a given Clafer object from AST
        :type claferSort: :mod:`~common.ClaferSort`
        
        A new field is added for every child of the given clafer. Fields will 
        become parameters for the Datatype constructor when generated.
        '''
        self.fields.append(claferSort)
    
    
    def setCardinalityConstraints(self):
        gl_div_upper = int(self.element.glCard[1].value / self.element.card[1].value)
        self.partitions = gl_div_upper #if gl_div_upper != 1 else self.element.glCard[1].value
        self.partitionSize = self.element.card[1].value#self.element.glCard[1].value   
        #print(self.partitions , self.partitionSize)
        
        self.bits = [BitVec(self.element.uid.split("_",1)[1] + "$"+str(i), 1) \
                     for i in range(self.partitions * self.partitionSize)]#(self.z3.scope*self.z3.scope)]#self.element.glCard[1].value)]
        
        self.zeroExt = int(1 + math.log(len(self.bits),2))
        #sets lower and upper cardinality bound on each partition
        for i in range(self.partitions):
            #lower
            self.constraints.append(Implies(live(int(i*self.partitionSize/self.partitions), self.element.glCard[1].value ,self.parentStack), \
                                            Sum([ZeroExt(self.zeroExt,self.bits[(i*self.partitionSize+j)]) for j in range(self.partitionSize)]) \
                                        >= self.element.card[0].value))
            #upper
            self.constraints.append(Implies(live(int(i*self.partitionSize/self.partitions), self.element.glCard[1].value, self.parentStack), \
                                            Sum([ZeroExt(self.zeroExt,self.bits[(i*self.partitionSize+j)]) for j in range(self.partitionSize)]) \
                                        <= self.element.card[1].value))
            #if the superclafer is zero, the subs are all zero
            if self.parentStack:
                self.constraints.append(Implies(Not(live(int(i*self.partitionSize/self.partitions), self.element.glCard[1].value, self.parentStack)), \
                                            Sum([ZeroExt(self.zeroExt,self.bits[(i*self.partitionSize+j)]) for j in range(self.partitionSize)]) \
                                        == 0))            
    
    def removeIsomorphism(self):
        #isomorphism problem
        #essentially a bitvector "sorting", kind of...
        for i in range(len(self.bits)):
            orlist = [[j*self.partitionSize + k \
                    for j in range(i // self.partitionSize + 1)] \
                    for k in range(i % self.partitionSize)]
            list2 = [Or(*[self.bits[l2] == 1 for l2 in l])  for l in orlist]
            if not list2: 
                continue
            else:
                self.constraints.append(Implies(self.bits[i] == 1, And(*list2)))
    
    def __str__(self):
        return self.element.uid + "_sort"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
'''
Created on Oct 21, 2013

@author: ezulkosk
'''


from common import SMTLib, Common
from common.Common import mOr
import sys


class ExprArg():
    def __init__(self, instances = None, nonsupered=False):
        '''
        :param instanceSorts: The list of sorts that are actually in instances.
        :type instancesSorts: [(:class:`~common.ClaferSort`, Mask)]
        
        Struct used to hold information as a bracketed constraint is traversed. 
        '''
        #key: (highestSuperSort, indexInHighestSuper), if supered (see below)
        #value: ([BoolSort b], polarity), b evaluates to true if the instance is on, list needs to be converted to OR
        #polarity: a *PYTHON* int, either DEFINITELY_ON, DEFINITELY_OFF, UNKNOWN
        if not instances:
            self.clafers = {}
        else:
            self.clafers = instances
        self.ints = []
        self.reals = []
        self.bool = None
        self.cardinalityMask = []
        #if true, contains clafer instances that are possibly not represented by their highest ancestor (so joins aren't broken)
        if nonsupered:
            self.hasBeenSupered = False
        else:
            self.hasBeenSupered = True 
        #TODO expand to reals, strings
    
    
    def add(self, key, expr):
        self.clafers[key] = expr
    
    def addBasedOnPolarity(self, sort, index, expr):
        #DOES NOT SUPER
        polarity = sort.known_polarity(index)
        if polarity == Common.DEFINITELY_ON:
            self.clafers[(sort,index)] = (SMTLib.SMT_BoolConst(True), polarity)
        elif polarity == Common.UNKNOWN:
            self.clafers[(sort,index)] = (expr, polarity)
        else:
            #if definitely off, do not add
            return
    
    def isPrimitive(self):
        return False
    
    def flattenJoin(self, joinList):
        #only used when reifying joins
        return [self]
        
    def getInstances(self, nonsupered=False):
        if nonsupered or self.hasBeenSupered:
            return self.clafers
        else:
            newClafers = {}
            for (sort, index) in self.clafers.keys():
                (expr, polarity) = self.clafers[(sort,index)]
                if polarity == Common.DEFINITELY_OFF:
                    continue
                key = (sort.highestSuperSort, sort.indexInHighestSuper + index)
                if polarity == Common.DEFINITELY_ON:
                    newClafers[key] = (SMTLib.SMT_BoolConst(True), Common.DEFINITELY_ON)
                    continue
                (currEntry, currPolarity) = newClafers.get(key, (SMTLib.SMT_BoolConst(False), Common.DEFINITELY_OFF))
                currEntry = mOr(currEntry, expr)
                newClafers[key] = (currEntry, Common.aggregate_polarity(currPolarity, polarity))
            self.clafers = newClafers
            self.hasBeenSupered = True 
        return self.clafers
    
    def getInts(self):
        return self.ints
          
    def __str__(self):
        return (str(self.getInstances(nonsupered=True)) + str(self.ints)) 
     
    def __repr__(self):
        return (str(self.getInstances(nonsupered=True)) + str(self.ints)) 

class PrimitiveArg(ExprArg): 
    '''
    only used to hold 'ref' or 'parent'
    '''
    def __init__(self, val):
        self.value = val
    
    def isPrimitive(self):
        return True
    
    def flattenJoin(self, joinList):
        #only used when reifying joins
        return [self]
    
    def getValue(self):
        return self.value
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.__str__()
               
class IntArg(ExprArg):
    def __init__(self, instance):
        '''
        Convenience class that extends ExprArg and holds an integer instance.
        '''
        ExprArg.__init__(self)
        self.ints = [(instance, True)]
    
    def getInts(self):
        return self.ints
    
    def getInstances(self):
        return {}
    
    def __str__(self):
        return (str(self.ints)) 
     
    def __repr__(self):
        return (str(self.ints)) 
        
        
class BoolArg(ExprArg):
    def __init__(self, instance):
        '''
        Convenience class that extends ExprArg and holds a boolean instance.
        '''
        ExprArg.__init__(self)
        self.bool = instance
        
    def getValue(self):
        return self.instanceSorts[0][1].get(0)
    
    def __str__(self):
        return (str(self.bool)) 
     
    def __repr__(self):
        return (str(self.bool)) 
    
    def getBool(self):
        return self.bool
 


class JoinArg(ExprArg):
    def __init__(self, left, right, cfr=None):
        self.left = left
        self.right = right
        self.cfr = cfr
        #self.instances = None
        ExprArg.__init__(self, nonsupered=True)
    
    def checkIfJoinIsComputed(self, nonsupered=False, getAllKeys = False):
        import constraints.operations.Join as Join
        if not self.clafers:
            joinList = self.flattenJoin()
            if getAllKeys:
                #TODO CLEAN
                (exprArg,all_keys) = Join.computeJoin(joinList, self.cfr, getAllKeys)
            else:
                exprArg = Join.computeJoin(joinList, self.cfr, getAllKeys)
            self.ints = [i for i in exprArg.ints]
            self.clafers = exprArg.getInstances(nonsupered)
            if not nonsupered:
                self.hasBeenSupered = True
        if getAllKeys:
            #print(all_keys)
            return all_keys
    
    def getInstances(self, nonsupered=False):
        self.checkIfJoinIsComputed(nonsupered=False)
        if not nonsupered and not self.hasBeenSupered:
            super(JoinArg, self).getInstances()
        return self.clafers
       
    def flattenJoin(self, joinList=[]):
        return self.left.flattenJoin([]) + joinList + self.right.flattenJoin([])
    
    def getInts(self):
        self.checkIfJoinIsComputed()
        return self.ints#getInts()

    def __str__(self):
        return (str(self.getInstances(nonsupered=True)) + str(self.ints)) 
    
    def __repr__(self):
        return (str(self.getInstances(nonsupered=True)) + str(self.ints)) 

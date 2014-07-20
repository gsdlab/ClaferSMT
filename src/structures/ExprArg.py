'''
Created on Oct 21, 2013

@author: ezulkosk
'''
from common import Assertions, SMTLib, Common
from common.Common import mOr
from structures.ClaferSort import BoolSort, IntSort, PrimitiveType, RealSort, \
    StringSort
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
        self.bool = None
        self.cardinalityMask = []
        #if true, contains clafer instances that are possibly not represented by their highest ancestor (so joins aren't broken)
        if nonsupered:
            self.hasBeenSupered = False
        else:
            self.hasBeenSupered = True
        
        #TODO expand to reals, strings
    
    
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
    
    def getInt(self):
        #print(self)
        return self.ints[0][0]
      
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
    
    def getValue(self):
        return self.value
               
class IntArg(ExprArg):
    def __init__(self, instance):
        '''
        Convenience class that extends ExprArg and holds an integer instance.
        '''
        ExprArg.__init__(self)
        self.ints = [(instance, True)]
        #self.cardinalityMask.append(SMTLib.SMT_IntConst(1))
    
    def getInt(self):
        return self.ints[0][0]    
    
    def getInts(self):
        return self.ints
    
    def getInstances(self):
        return {}
    
    def __str__(self):
        return (str(self.ints)) 
     
    def __repr__(self):
        return (str(self.ints)) 
        
class RealArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds an integer instance.
        '''
        sys.exit("TODO realarg")
        sort = RealSort()
        for i in range(len(instances)):
            sort.cardinalityMask.put(i, SMTLib.SMT_IntConst(1))
        #self.instanceSorts = [(sort, Mask.createIntMask(instances))]
        
        
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
 
class StringArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds an integer instance.
        '''
        #TODO
        sort = StringSort()
        for i in range(len(instances)):
            sort.cardinalityMask.put(i, SMTLib.SMT_IntConst(1))
        #self.instanceSorts = [(sort, Mask.createIntMask(instances))]

class JoinArg(ExprArg):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.instances = []
        ExprArg.__init__(self)
    
    def checkIfJoinIsComputed(self):
        import constraints.operations.Join as Join
        if not self.instances:
            joinList = self.flattenJoin()
            return Join.computeJoin(joinList)
    
    def getInstances(self, nonsupered=False):
        exprArg = self.checkIfJoinIsComputed()
        return exprArg.getInstances(nonsupered)
        #return self.instances
       
    def flattenJoin(self, joinList=[]):
        return self.left.flattenJoin([]) + joinList + self.right.flattenJoin([])
    
    def getInt(self):
        exprArg = self.checkIfJoinIsComputed()
        return exprArg.getInt()
    
    def getInts(self):
        exprArg = self.checkIfJoinIsComputed()
        return exprArg.getInts()
        
        

      
    def __str__(self):
        return (str(self.getInstances(nonsupered=True)) + str(self.ints)) 
        #return ("join: " + str(self.left.getInstanceSorts())+ str(self.right.getInstanceSorts()))
    
    def __repr__(self):
        return (str(self.getInstances(nonsupered=True)) + str(self.ints)) 
        #return ("join: " + str(self.getInstanceSorts())+ str(self.getInstanceSorts()))
    

       
       
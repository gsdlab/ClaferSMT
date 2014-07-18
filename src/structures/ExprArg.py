'''
Created on Oct 21, 2013

@author: ezulkosk
'''
from common import Assertions, SMTLib, Common
from structures.ClaferSort import BoolSort, IntSort, PrimitiveType, RealSort, \
    StringSort
import sys



class ExprArg():
    def __init__(self, instances = {}, nonsupered=True):
        '''
        :param instanceSorts: The list of sorts that are actually in instances.
        :type instancesSorts: [(:class:`~common.ClaferSort`, Mask)]
        
        Struct used to hold information as a bracketed constraint is traversed. 
        '''
        #key: (highestSuperSort, indexInHighestSuper), if supered (see below)
        #value: ([BoolSort b], polarity), b evaluates to true if the instance is on, list needs to be converted to OR
        #polarity: a *PYTHON* int, either DEFINITELY_ON, DEFINITELY_OFF, UNKNOWN
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
            sys.exit("getInstances not yet")
            newClafers = {}
            for (sort, index, polarity) in self.clafers:
                #TODO if the currPolarity is already DEFINITELY_ON, don't add anything new
                if polarity == Common.DEFINITELY_OFF:
                    continue
                key = (sort.highestSuperSort, sort.indexInHighestSuper + index)
                (currEntryList, currPolarity) = self.clafers.get(key, ([], Common.DEFINITELY_OFF))
                currEntryList.append((sort,index))
                newClafers[key] = (currEntryList, Common.aggregate_polarity(currPolarity, polarity))
            self.clafers = newClafers
            self.hasBeenSupered = True 
        return self.clafers
    
    
    def finish(self):
        return self.instanceSorts[0][1].get(0)
      
    def __str__(self):
        return (str(self.getInstances(nonsupered=True))) 
     
    def __repr__(self):
        return (str(self.getInstances(nonsupered=True))) 

class PrimitiveArg(): 
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
        self.ints = [instance]
        self.cardinalityMask.append(SMTLib.SMT_IntConst(1))
        
    def getInstances(self):
        return self.ints
    
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
        self.instanceSorts = []
    
    def checkIfJoinIsComputed(self):
        import constraints.operations.Join as Join
        if not self.instanceSorts:
            joinList = self.flattenJoin()
            self.instanceSorts = Join.computeJoin(joinList)
    
    def getInstanceSorts(self):
        self.checkIfJoinIsComputed()
        return self.instanceSorts
    
    def getInstanceSort(self, index):
        self.checkIfJoinIsComputed()
        return self.instanceSorts[index]
       
    def flattenJoin(self, joinList=[]):
        return self.left.flattenJoin([]) + joinList + self.right.flattenJoin([])
    
    
    def clone(self):
        if not self.instanceSorts:
            return JoinArg(self.left.clone(), self.right.clone())
        newInstanceSorts = []
        for i in self.instanceSorts:
            if isinstance(i, PrimitiveType):
                newInstanceSorts.append(i)
            else:    
                (sort, mask) = i
                newInstanceSorts.append((sort, mask.copy()))
        return ExprArg([], newInstanceSorts)
      
    def __str__(self):
        return ("join: " + str(self.left.getInstanceSorts())+ str(self.right.getInstanceSorts()))
    
    def __repr__(self):
        return ("join: " + str(self.getInstanceSorts())+ str(self.getInstanceSorts()))
    

       
       
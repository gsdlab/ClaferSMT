'''
Created on Oct 21, 2013

@author: ezulkosk
'''
from bintrees.avltree import AVLTree
from common.Common import mOr
from common import Common
from lxml.builder import basestring
from z3 import And, If
import sys

class ExprArg():
    def __init__(self, instanceSorts):
        '''
        :param joinSorts: The list of sorts used to determine which ClaferSorts to join.
        :type joinSorts: [:class:`~common.ClaferSort`]
        :param instanceSorts: The list of sorts that are actually in instances.
        :type instancesSorts: [:class:`~common.ClaferSort`]
        :param instances: The set of Z3-int expressions associated with the bracketed constraint up to this point.
        :type instances: [Int()]
        
        Struct used to hold information as a bracketed constraint is traversed. 
        '''
        self.instanceSorts = instanceSorts
    
    def flattenJoin(self, joinList):
        #only used when reifying joins
        return [self]
        
    def getInstanceSorts(self):
        return self.instanceSorts
    
    def getInstanceSort(self, index):
        return self.instanceSorts[index]
    
    def modifyInstances(self, newInstances):
        '''
        :param newInstances:
        :type newInstances: [Int()]
        :returns: :class:`~ExprArg`
        
        Returns the old ExprArg, with its instances changed to **newInstances**.
        '''
        return ExprArg(self.instanceSorts[:])
    
    def finish(self):
        return self.instanceSorts[0][1].get(0)
    
    def clone(self):
        newInstanceSorts = []
        for i in self.instanceSorts:
            if isinstance(i, basestring):
                newInstanceSorts.append(i)
            else:    
                (sort, mask) = i
                newInstanceSorts.append((sort, mask.copy()))
        return ExprArg(newInstanceSorts)
      
    def __str__(self):
        return (str(self.getInstanceSorts())) 
     
    def __repr__(self):
        return (str(self.getInstanceSorts())) 
               
class IntArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds an integer instance.
        '''
        self.instanceSorts = [("int", Mask.createIntMask(instances))]
        
class BoolArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds a boolean instance.
        '''
        self.joinSorts = ["bool"]
        self.instanceSorts = [("bool", Mask.createBoolMask(instances))]
 

class JoinArg(ExprArg):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.instanceSorts = []
    
    def getInstanceSorts(self):
        if not self.instanceSorts:
            self.computeJoin()
        return self.instanceSorts
    
    def getInstanceSort(self, index):
        if not self.instanceSorts:
            self.computeJoin()
        return self.instanceSorts[index]
       
    def flattenJoin(self, joinList):
        return self.left.flattenJoin([]) + joinList + self.right.flattenJoin([])
    
    
    ''' 
    #######################################################################
    # JOIN COMPUTATIONS   
    #######################################################################
    '''
    
    @staticmethod
    def alreadyExists(key, instanceSorts):
        for i in instanceSorts:
            (sort, mask) = i
            if key == sort:
                return mask
        return None
    
    @staticmethod
    def joinWithSuper(sort, mask):
        '''
        :param sort:
        :type sort: :class:`~common.ClaferSort`
        :returns: (:class:`~common.ClaferSort`, [Int()]) 
        
        Maps each instance of the subclafer **sort** to the corresponding super instance. Returns the super sort and its instances.
        '''
        newMask = Mask()
        for i in mask.keys():
            #ClaferSort.addSubSort(self, sub), is somewhat related 
            newMask.put(i + sort.indexInSuper,
                        If(mask.get(i) != sort.parentInstances, 
                           sort.superSort.instances[i + sort.indexInSuper], 
                           sort.superSort.parentInstances))
        return(sort.superSort, newMask)

    @staticmethod
    def joinWithParent(arg):
        newInstanceSorts = []
        for i in arg.instanceSorts:
            (sort, mask) = i
            newMask = JoinArg.alreadyExists(sort.parent, newInstanceSorts)
            if not newMask:
                newMask = Mask()
            for j in mask.keys():
                (lower,upper,_) = sort.instanceRanges[j]
                for k in range(lower, upper + 1):
                    if k == sort.parentInstances:
                        break
                    prevClause = newMask.get(k)
                    newMask.put(k, mOr(prevClause, mask.get(j) == k))
            newInstanceSorts.append((sort.parent, newMask))
        for i in newInstanceSorts:
            (sort, mask) = i
            for j in mask.keys():
                mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
        #for i in newMask.keys():
        #    newMask.put(i, If(newMask.get(i), sort.parent.instances[i], sort.parent.parentInstances))
        return ExprArg(newInstanceSorts)
    
    @staticmethod
    def joinWithPrimitive(arg):
        newInstanceSorts = []
        for i in arg.getInstanceSorts():
            (sort, mask) = i
            if sort.refSort == "integer" or sort.refSort == "string": #change for string soon
                newMask = Mask()
                for i in mask.keys():
                    newMask.put(i, If(mask.get(i) != sort.parentInstances, sort.refs[i], 0))
                newInstanceSorts.append(("int", newMask)) #should change the "int", but not sure how yet
            else:
                print("Error on: " + sort.refSort + ", refs other than int (e.g. double) unimplemented")
                sys.exit()
        return ExprArg(newInstanceSorts)
        
    @staticmethod
    def joinWithClaferRef(arg):
        newInstanceSorts = []
        for i in arg.getInstanceSorts():
            (sort, mask) = i
            tempRefs = []
            newMask = JoinArg.alreadyExists(sort.refSort, newInstanceSorts)
            if not newMask:
                newMask = Mask()
            for j in mask.keys():
                tempRefs.append(If(mask.get(j) != sort.parentInstances,
                                   sort.refs[j], sort.refSort.numInstances))
            for j in range(sort.refSort.numInstances):
                clause = mOr(*[k == j for k in tempRefs])
                newMask.put(j, mOr(newMask.get(j), clause))
            newInstanceSorts.append((sort.refSort, newMask))
        for i in newInstanceSorts:
            (sort, mask) = i
            for j in mask.keys():
                mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
        return ExprArg(newInstanceSorts)
        
    @staticmethod
    def joinWithRef(arg): 
        (sort, _) = arg.instanceSorts[0]
        if isinstance(sort.refSort, basestring):
            return JoinArg.joinWithPrimitive(arg)
        else: 
            #join on ref sort
            #needs to be more robust for multiple instanceSorts
            return JoinArg.joinWithClaferRef(arg)
    
    @staticmethod
    def joinWithClafer(left, right):
        newInstanceSorts = []
        for l in left.getInstanceSorts():
            (left_sort, left_mask) = l
            for r in right.getInstanceSorts():
                (right_sort, right_mask) = r
                noMatch = False
                while not(right_sort in left_sort.fields):
                    if not left_sort.superSort:
                        noMatch = True
                        break
                    (left_sort, left_mask) = JoinArg.joinWithSuper(left_sort, left_mask)
                if noMatch:
                    break
                zeroedVal = right_sort.parentInstances
                newMask = JoinArg.alreadyExists(right_sort, newInstanceSorts)
                if not newMask:
                    newMask = Mask()
                for i in right_mask.keys():
                    (lower, upper, _) = right_sort.instanceRanges[i]
                    for j in range(lower, upper + 1): 
                        #only possibly join with things that are in left
                        if left_mask.get(j):
                            prevClause = newMask.get(i)
                            newMask.put(i, mOr(prevClause, And(left_mask.get(j) != left_sort.parentInstances, 
                                                            right_sort.instances[i] == j)))
                newInstanceSorts.append((right_sort, newMask))
        for i in newInstanceSorts:
            (sort, mask) = i
            for j in mask.keys():
                mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
        return ExprArg(newInstanceSorts)
    
    def computeJoin(self):
        #can be optimized... a lot...
        joinList = self.flattenJoin([])
        left = joinList.pop(0) 
        while joinList:
            right = joinList.pop(0)
            rightJoinPoint = right.getInstanceSort(0)
            if isinstance(rightJoinPoint, basestring):
                if rightJoinPoint == "parent":
                    left = JoinArg.joinWithParent(left)
                elif rightJoinPoint == "ref":
                    left = JoinArg.joinWithRef(left)
            else:
                left = self.joinWithClafer(left, right)
        self.instanceSorts = left.getInstanceSorts()
      
    ''' 
    #######################################################################
    # END JOINS   
    #######################################################################
    '''        
    def clone(self):
        if not self.instanceSorts:
            return JoinArg(self.left.clone(), self.right.clone())
        newInstanceSorts = []
        for i in self.instanceSorts:
            if isinstance(i, basestring):
                newInstanceSorts.append(i)
            else:    
                (sort, mask) = i
                newInstanceSorts.append((sort, mask.copy()))
        return ExprArg([], newInstanceSorts)
      
    def __str__(self):
        return ("join: " + str(self.left.getInstanceSorts())+ str(self.right.getInstanceSorts()))
    
    def __repr__(self):
        return ("join: " + str(self.getInstanceSorts())+ str(self.getInstanceSorts()))
    
class Mask():
    '''
    Wrapper for AVLTree to keep track of which instances are *on*.
    '''
    def __init__(self, sort=None, instances=[], copy=False):
        if copy:
            #sort holds a copy of the AVLTree from the previous Mask
            self.tree = sort
        newInstances = []
        if not sort:
            self.tree = AVLTree()
        elif instances:
            newInstances = [(i, sort.instances[i]) for i in (instances)]
            self.tree = AVLTree(newInstances)
        elif sort:
            self.tree = AVLTree(sort)
        elif not instances and not sort:
            self.tree = AVLTree()
       
    @staticmethod
    def createIntMask(instances):
        return Mask([(i, instances[i]) for i in range(len(instances))])

    @staticmethod
    def createBoolMask(instances):
        return Mask([(i, instances[i]) for i in range(len(instances))])
    
    def difference(self, keyset):
        return self.tree.difference(keyset)
    
    def intersection(self, keyset):
        return self.tree.intersection(keyset)
    
    def copy(self):
        return Mask(self.tree.copy(), instances=[], copy=True)
    
    def pop_value(self):
        (_, value) = self.tree.pop_item()
        return value
    
    def getTree(self):
        return self.tree
    
    def size(self):
        return self.tree.count
    
    def keys(self):
        return self.tree.keys()
    
    def values(self):
        return self.tree.values()
    
    def put(self, key, value):
        return self.tree.insert(key, value)
    
    def get(self, index):
        return self.tree.get(index)
    
    def __str__(self):
        return (str(self.tree)) 
     
    def __repr__(self):
        return (str(self.tree))    

    def __lt__(self, other):
        #dummy sorting for now
        return True
    def __eq__(self, other):
        return not self<other and not other<self
    def __ne__(self, other):
        return self<other or other<self
    def __gt__(self, other):
        return other<self
    def __ge__(self, other):
        return not self<other
    def __le__(self, other):
        return not other<self
       
       
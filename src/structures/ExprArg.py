'''
Created on Oct 21, 2013

@author: ezulkosk
'''
from bintrees.avltree import AVLTree
from lxml.builder import basestring


class ExprArg():
    def __init__(self, instanceSorts):
        '''
        :param instanceSorts: The list of sorts that are actually in instances.
        :type instancesSorts: [:class:`~common.ClaferSort`]
        
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
        self.instanceSorts = [("bool", Mask.createBoolMask(instances))]
 

class JoinArg(ExprArg):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.instanceSorts = []
    
    def checkIfJoinIsComputed(self):
        import constraints.Operations as Ops
        if not self.instanceSorts:
            joinList = self.flattenJoin()
            self.instanceSorts = Ops.computeJoin(joinList)
    
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
       
       
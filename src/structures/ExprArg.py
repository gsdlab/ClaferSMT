'''
Created on Oct 21, 2013

@author: ezulkosk
'''
from bintrees.avltree import AVLTree
from lxml.builder import basestring
class ExprArg():
    def __init__(self, joinSorts, instanceSorts):
        '''
        :param joinSorts: The list of sorts used to determine which ClaferSorts to join.
        :type joinSorts: [:class:`~common.ClaferSort`]
        :param instanceSorts: The list of sorts that are actually in instances.
        :type instancesSorts: [:class:`~common.ClaferSort`]
        :param instances: The set of Z3-int expressions associated with the bracketed constraint up to this point.
        :type instances: [Int()]
        
        Struct used to hold information as a bracketed constraint is traversed. 
        '''
        self.joinSorts = joinSorts
        self.instanceSorts = instanceSorts
        
    def modifyInstances(self, newInstances):
        '''
        :param newInstances:
        :type newInstances: [Int()]
        :returns: :class:`~ExprArg`
        
        Returns the old ExprArg, with its instances changed to **newInstances**.
        '''
        return ExprArg(self.joinSorts[:], self.instanceSorts[:], newInstances)
    
    def getInstanceMask(self, sort):
        for i in self.instanceSorts:
            (curr_sort, mask) = i
            if sort == curr_sort:
                return mask
    
    def getUnmaskedInstances(self, boolArray):
        '''
        Used in tandem with the new approach to splits and joins
        no use yet
        '''
        pass
    
    @staticmethod
    def getUnmaskedCount(boolArray):
        '''
        Used in tandem with the new approach to splits and joins
        '''
        count = 0
        for i in boolArray:
            if i:
                count = count + 1
        return count        
    
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
        return ExprArg(self.joinSorts[:], newInstanceSorts)
      
    def __str__(self):
        return (str(self.instanceSorts)) 
     
    def __repr__(self):
        return (str(self.instanceSorts)) 
               
class IntArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds an integer instance.
        '''
        self.joinSorts = ["int"]
        self.instanceSorts = [("int", Mask.createIntMask(instances))]
        
class BoolArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds a boolean instance.
        '''
        self.joinSorts = ["bool"]
        self.instanceSorts = [("bool", Mask.createBoolMask(instances))]
        
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
       
       
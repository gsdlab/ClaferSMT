'''
Created on Nov 1, 2013

@author: ezulkosk
'''
from common import Common
from common.Common import mOr, mAnd
from lxml.builder import basestring
from structures.ClaferSort import BoolSort, IntSort
from structures.ExprArg import Mask, ExprArg, JoinArg, IntArg, BoolArg
from z3 import If, And, Sum, Not, Implies, Xor, Or, IntVector
import sys


''' 
#######################################################################
# JOIN COMPUTATIONS   
#######################################################################
'''

def alreadyExists(key, instanceSorts):
    '''
    Determines if the sort is already in the list of instanceSorts
    '''
    for i in instanceSorts:
        (sort, mask) = i
        if key == sort:
            return mask
    return Mask()

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
                    If(sort.isOn(mask.get(i)), 
                       sort.superSort.instances[i + sort.indexInSuper], 
                       sort.superSort.parentInstances))
    return(sort.superSort, newMask)

def joinWithParent(arg):
    newInstanceSorts = []
    for i in arg.instanceSorts:
        (sort, mask) = i
        newMask = alreadyExists(sort.parent, newInstanceSorts)
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
    return ExprArg(newInstanceSorts)


def addPrimitive(newSort, newMask, oldSort, oldMask, index):
    newIndex = newSort.getNextIndex()
    cardinalityMask = newSort.getCardinalityMask()
    constraint = And(oldSort.isOn(oldMask.get(index)), mAnd(*[oldSort.refs[index] != i for i in newMask.values()]))
    cardinalityMask.put(newIndex, If(constraint, 1, 0))
    newMask.put(newIndex, If(constraint, oldSort.refs[index], 0))


def joinWithPrimitive(arg):
    newInstanceSorts = []    
    for i in arg.getInstanceSorts():
        (sort, mask) = i
        if sort.refSort == "integer" or sort.refSort == "string": #change for string soon
            newMask = alreadyExists(IntSort(), newInstanceSorts) #check that this works!!!
            newSort = IntSort()
            for i in mask.keys():
                addPrimitive(newSort, newMask, sort, mask, i)         
            newInstanceSorts.append((newSort, newMask)) #should change the "int", but not sure how yet
        else:
            print("Error on: " + sort.refSort + ", refs other than int (e.g. double) unimplemented")
            sys.exit()
    return ExprArg(newInstanceSorts)
    
def joinWithClaferRef(arg):
    newInstanceSorts = []
    for i in arg.getInstanceSorts():
        (sort, mask) = i
        while not sort.refs:
            (sort, mask) = joinWithSuper(sort, mask)
        tempRefs = []
        newMask = alreadyExists(sort.refSort, newInstanceSorts)
        if isinstance(sort.refSort, basestring):
            return joinWithPrimitive(ExprArg([(sort, mask)]))
        for j in mask.keys():
            if isinstance(sort.refSort, basestring):
                tempRefs.append(If(sort.isOn(mask.get(j)),
                                   sort.refs[j], 0))
            else:
                tempRefs.append(If(sort.isOn(mask.get(j)),
                                   sort.refs[j], sort.refSort.numInstances))
        if isinstance(sort.refSort, basestring):
            for j in range(sort.numInstances):
                clause = mOr(*[k == j for k in tempRefs])
                newMask.put(j, mOr(newMask.get(j), clause))
        else:
            for j in range(sort.refSort.numInstances):
                clause = mOr(*[k == j for k in tempRefs])
                newMask.put(j, mOr(newMask.get(j), clause))
        newInstanceSorts.append((sort.refSort, newMask))
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
    return ExprArg(newInstanceSorts)
    
def joinWithRef(arg): 
    (sort, _) = arg.instanceSorts[0]
    if isinstance(sort.refSort, basestring):
        return joinWithPrimitive(arg)
    else: 
        #join on ref sort
        #needs to be more robust for multiple instanceSorts
        return joinWithClaferRef(arg)


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
                (left_sort, left_mask) = joinWithSuper(left_sort, left_mask)
            if noMatch:
                break
            newMask = alreadyExists(right_sort, newInstanceSorts)
            for i in right_mask.keys():
                (lower, upper, _) = right_sort.instanceRanges[i]
                for j in range(lower, upper + 1): 
                    #only possibly join with things that are in left
                    if left_mask.get(j):
                        prevClause = newMask.get(i)
                        newMask.put(i, mOr(prevClause, And(left_sort.isOn(left_mask.get(j)), 
                                                        right_sort.instances[i] == j)))
            newInstanceSorts.append((right_sort, newMask))
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
    return ExprArg(newInstanceSorts)

def computeJoin(joinList):
    #can be optimized... a lot...
    left = joinList.pop(0) 
    while joinList:
        right = joinList.pop(0)
        rightJoinPoint = right.getInstanceSort(0)
        if isinstance(rightJoinPoint, basestring):
            if rightJoinPoint == "parent":
                left = joinWithParent(left)
            elif rightJoinPoint == "ref":
                left = joinWithRef(left)
        else:
            left = joinWithClafer(left, right)
    return left.getInstanceSorts()

''' 
#######################################################################
# END JOIN COMPUTATIONS  
#######################################################################
''' 

''' 
#######################################################################
# RELATIONAL/BOOLEAN OPERATORS  
#######################################################################
''' 

def op_not(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Boolean negation of arg.
    '''
    assert isinstance(arg, ExprArg)
    (_, mask) = arg.getInstanceSort(0)
    val = mask.pop_value()
    return BoolArg([Not(val)])
    
'''
CHECKED TO HERE!!!!!!!!!@EFDSGHDHFDSFH$#RHQLEHDSUFHOUDHFUEWFHDLFHDFEWUHFDSFHEFHE
'''    
    
#need to iterate over all instancesorts, maybe not
def op_eq(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left = right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    
    #integer equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if isinstance(left_sort, IntSort) or isinstance(right_sort, IntSort):
        return BoolArg([sum(*[left_mask.values() for (_, left_mask) in left.getInstanceSorts()]) 
                        == sum(*[right_mask.values() for (_, right_mask) in right.getInstanceSorts()])])
    #clafer-set equality case
    else:
        cond = []
        while True:
            nextSorts = getNextInstanceSort(sortedL, sortedR)
            if not nextSorts:
                break
            if len(nextSorts) == 1:
                (_, (sort, l)) = nextSorts[0]
                #if only one side of the equation has elements a sort,
                #make sure none are on.
                for i in l.values():
                    cond.append(sort.isOff(i))
                    
            else:
                (_, (sort, l)) = nextSorts[0]
                (_, (_, r)) = nextSorts[1]
                for i in l.difference(r.getTree()):
                    cond.append(sort.isOff(l.get(i)))
                for i in r.difference(l.getTree()):
                    cond.append(sort.isOff(r.get(i)))
                for i in l.intersection(r.getTree()):
                    cond.append(mAnd(Implies(sort.isOn(l.get(i)),
                                              sort.isOn(r.get(i))),
                                          Implies(sort.isOff(l.get(i)),
                                              sort.isOff(r.get(i)))))
        return BoolArg([And(*cond)])
    
def op_ne(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left != right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    expr = op_eq(left, right)
    for i in expr.getInstanceSorts():
        (_, mask) = i
        for j in mask.keys():
            mask.put(j, Not(mask.get(j)))
    return expr
    
def op_lt(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left < right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([lval < rval])  
        
def op_le(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left <= right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([lval <= rval])  

def op_gt(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left > right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_lt(right, left)

def op_ge(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left >= right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_le(right, left)

def op_and(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean conjunction of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([mAnd(lval, rval)])  

def op_or(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean disjunction of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([mOr(lval, rval)])  

def op_xor(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean XOR of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([Xor(lval, rval)])  

def op_implies(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensure that if instance *i* of left is on, so is instance *i* of right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    
    #integer equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if isinstance(left_sort, BoolSort) or isinstance(right_sort, BoolSort):
        return BoolArg([Implies(left_mask.pop_value(), right_mask.pop_value())])
    #clafer-set equality case
    else:
        cond = []
        while True:
            nextSorts = getNextInstanceSort(sortedL, sortedR)
            if not nextSorts:
                break
            if len(nextSorts) == 1:
                (side, (sort, l)) = nextSorts[0]
                #if only left side of the equation has elements of a sort,
                #make sure none are on.
                if side == "l":
                    for i in l.values():
                        cond.append(sort.isOff(i))
                    
            else:
                (_, (sort, l)) = nextSorts[0]
                (_, (_, r)) = nextSorts[1]
                for i in l.difference(r.getTree()):
                    cond.append(sort.isOff(l.get(i)))
                for i in l.intersection(r.getTree()):
                    cond.append(Implies(sort.isOn(l.get(i)),
                                              sort.isOn(r.get(i))))
        return BoolArg([And(*cond)])
    #return BoolArg([mAnd(*[Implies(i,j) for i,j in zip(left.instances, right.instances)])])

def op_equivalence(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that an element of left is *on* iff it is *on* in right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg([And(op_implies(left, right), op_implies(right,left))])
    #return BoolArg([mAnd(*[mAnd(Implies(i,j), Implies(j,i)) for i,j in zip(left.instances, right.instances)])])
    
def op_ifthenelse(cond, ifExpr, elseExpr):
    '''
    :param cond:
    :type cond: :class:`~ExprArg`
    :param ifExpr:
    :type ifExpr: :class:`~ExprArg`
    :param elseExpr:
    :type elseExpr: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Returns the corresponding Z3 If-construct over the instances of the arguments.
    '''
    assert isinstance(cond, ExprArg)
    assert isinstance(ifExpr, ExprArg)
    assert isinstance(elseExpr, ExprArg)
    
    (_, cond_mask) = cond.getInstanceSort(0)
    (_, if_mask) = ifExpr.getInstanceSort(0)
    (_, else_mask) = elseExpr.getInstanceSort(0)
    
    return BoolArg([If(cond_mask.pop_value(), if_mask.pop_value(), else_mask.pop_value())])

''' 
#######################################################################
# END RELATIONAL/BOOLEAN OPERATORS  
#######################################################################
''' 


''' 
#######################################################################
# SET OPERATORS  
#######################################################################
''' 

def getNextInstanceSort(left, right):
    if left or right:
        if left and right:
            if left[0][0] < right[0][0]:
                return [("l", left.pop(0))]
            elif left[0][0] > right[0][0]:
                return [("r", right.pop(0))]
            else:
                return [("l", left.pop(0)), ("r", right.pop(0))]
        elif left:
            return [("l", left.pop(0))]
        else:
            return [("r", right.pop(0))]
    else: 
        return []

def op_join(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~JoinArg` 
    
    Returns a *lazy* join, that will only be computed when we know all of the components of the join.
    The actual join occurs when :py:func:`computeJoin` is invoked.
    
    For example, if the full clafer join is:
    
    >>> A . (B . C)
    
    and we are currently processing (B . C), we do no processing. Once we have the *full* join (A . B . C), we 
    use the associativity of well-formed joins to make processing much easier. All joins *should* be well-formed;
    bad joins should be caught by the Clafer front-end.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return JoinArg(left, right)

def op_card(arg):
    '''
    :param arg:
    :type left: :class:`~arg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns the number of instances that are *on* in arg.
    '''
    assert isinstance(arg, ExprArg)
    instances = []
    for i in arg.getInstanceSorts():
        (sort, mask) = i
        #refactor
        if isinstance(sort, IntSort):
            instances = [i for i in sort.cardinalityMask.values()]
        else:
            for j in mask.values():
                instances.append(If(sort.isOn(j), 1, 0))  
    return IntArg([Sum(instances)])

def op_union(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set union (left ++ right)
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    newInstanceSorts = []
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            (_, nextInstanceSort) = nextSorts[0]
            newInstanceSorts.append(nextInstanceSort)
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            newMask = Mask()
            for i in l.difference(r.getTree()):
                newMask.put(i, l.get(i))
            for i in r.difference(l.getTree()):
                newMask.put(i, r.get(i))
            for i in l.intersection(r.keys()):
                newMask.put(i, Common.min2(l.get(0), r.get(0)))
            newInstanceSorts.append((sort, newMask))
    return ExprArg(newInstanceSorts)
                
  
def op_intersection(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set intersection (left & right)
    '''
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    newInstanceSorts = []
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            continue
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            newMask = Mask()
            for i in l.intersection(r.keys()):
                newMask.put(i, Common.max2(l.get(0), r.get(0)))
            newInstanceSorts.append((sort, newMask))
    return ExprArg(left.joinSorts, newInstanceSorts)
    
    
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (extendedL, extendedR) = set_extend(left,right)
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.max2(extendedL.instances.pop(0), extendedR.instances.pop(0)))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)
    '''

def op_difference(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set difference (left - - right)
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    newInstanceSorts = []
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            (side, nextInstanceSort) = nextSorts[0]
            if(side == "l"):
                newInstanceSorts.append(nextInstanceSort)
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            newMask = Mask()
            for i in l.difference(r.getTree()):
                newMask.put(i, l.get(i))
            for i in l.intersection(r.getTree()):
                newMask.put(i, If(sort.isOn(r.get(i))
                                     , l.get(i)
                                     , sort.parentInstances))
            newInstanceSorts.append((sort, newMask))
    return ExprArg(left.joinSorts, newInstanceSorts)
    
def getMatch(key, my_list):
    '''
    returns the items in list with the same sort as key,
    along with the index of the instances in the supersort
    '''
    matches = []
    for i in my_list:
        (sort, _) = i
        if key == sort:
            matches.append((0,i))
        else:
            totalIndexInSuper = 0
            tempKey = key
            while tempKey.superSort:
                totalIndexInSuper = totalIndexInSuper + tempKey.indexInSuper
                tempKey = tempKey.superSort
                if tempKey == sort:
                    matches.append((totalIndexInSuper, i))
                    break
    return matches
                
def op_in(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that left is a subset of right.
    '''
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    cond = []
    for i in sortedL:
        (left_sort, left_mask) = i
        matches = getMatch(left_sort, sortedR)
        for j in matches:
            (transform, (right_sort,right_mask)) = j
            for k in left_mask.keys():
                if not right_mask.get(k + transform):
                    cond.append(left_sort.isOff(left_mask.get(k)))
                else:
                    cond.append(Implies(left_sort.isOn(left_mask.get(k)),
                                        right_sort.isOn(right_mask.get(k + transform))))
    return BoolArg([And(*cond)])
   
def op_nin(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Ensures that left is not a subset of right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    expr = op_in(left,right)
    return BoolArg([expr.pop_value()])

def op_domain_restriction(l,r):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    No idea what this does.
    '''
    pass

def op_range_restriction(l,r):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Nope.
    '''
    pass

''' 
#######################################################################
# END SET OPERATORS  
#######################################################################
''' 


''' 
#######################################################################
# ARITHMETIC
#######################################################################
''' 

def op_add(left,right):
    '''
    :param left:
    :type left: :class:`~IntArg`
    :param right:
    :type right: :class:`~IntArg`
    :returns: :class:`~IntArg` 
    
    Returns left + right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval + rval])

def op_sub(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left - right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval - rval])

def op_mul(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left * right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval * rval])

#integer division
def op_div(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left / right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval / rval]
                   if((not isinstance(lval, int)) or (not isinstance(rval, int)))
                             else [lval // rval])
    
    
def op_un_minus(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Negates arg.
    '''
    assert isinstance(arg, ExprArg)
    (_, mask) = arg.getInstanceSort(0)
    val = mask.pop_value()
    return IntArg([-(val)])
   
def op_sum(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Computes the sum of all integer instances in arg. May not match the semantics of the Alloy backend.
    '''
    assert isinstance(arg, ExprArg)
    instances = []
    for i in arg.getInstanceSorts():
        (_, mask) = i
        for j in mask.values():
            instances.append(j)
    return IntArg([Sum(instances)])

''' 
#######################################################################
# END ARITHMETIC
#######################################################################
''' 

''' 
#######################################################################
# QUANTIFIERS
#######################################################################
''' 

def getQuantifierConditionList(exprs):
    '''
    Iterates over all values in all masks, 
    and returns a list of Booleans, indicating whether
    each instance is on (or true), or not. 
    '''
    finalList = []
    for i in exprs:
        for expr in i:
            condList = []
            for k in expr.getInstanceSorts():
                (sort, mask) = k
                for l in mask.keys():
                    condList.append(sort.isOn(mask.get(l)))

            finalList.append(mOr(*condList))
    return finalList

def quant_some(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [And(i, j) for i,j in zip(ifConstraints, condList)]
    return Or(*condList)

def quant_all(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [Implies(i, j) for i,j in zip(ifConstraints, condList)]
    return And(*condList)

def quant_no(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [And(i, j) for i,j in zip(ifConstraints, condList)]
    return Not(Or(*condList))

def quant_one(exprs, ifConstraints):
    '''
    There's probably a better way to do this.
    '''
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [And(i, j) for i,j in zip(ifConstraints, condList)]
    indicatorVars = IntVector("one_" + str(Common.getConstraintUID()),len(condList))
    exprList = []
    for i in range(len(condList)):
        exprList.append(If(condList[i], indicatorVars[i] == 1, indicatorVars[i] == 0))
    return Sum(*exprList) == 1
    
def quant_lone(exprs, ifConstraints):
    return Or(quant_no(exprs, ifConstraints), quant_one(exprs, ifConstraints))

''' 
#######################################################################
# END QUANTIFIERS
#######################################################################
''' 

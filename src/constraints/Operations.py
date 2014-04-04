'''
Created on Nov 1, 2013

@author: ezulkosk
'''
from common import Common, Assertions, Options
from common.Common import mOr, mAnd
from structures.ClaferSort import BoolSort, IntSort, PrimitiveType, StringSort, \
    RealSort
from structures.ExprArg import Mask, ExprArg, JoinArg, IntArg, BoolArg
from z3 import If, And, Sum, Not, Implies, Xor, Or, IntVector, Int, ToReal
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
        #print(sort)
        #print(sort.superSort)
        #print(sort.refSort) 
        newMask.put(i + sort.indexInSuper,
                    If(sort.isOn(mask.get(i)), 
                       sort.superSort.instances[i + sort.indexInSuper], 
                       sort.superSort.parentInstances))
        Assertions.nonEmptyMask(newMask)
    return(sort.superSort, newMask)

def joinWithParent(arg):
    newInstanceSorts = []
    for i in arg.instanceSorts:
        (sort, mask) = i
        newMask = alreadyExists(sort.parent, newInstanceSorts)
        for j in mask.keys():
            (lower,upper,_) = sort.instanceRanges[j]
            for k in range(lower, upper + 1):
                if k >= sort.parentInstances:
                    break
                prevClause = newMask.get(k)
                newMask.put(k, mOr(prevClause, mask.get(j) == k))
        newInstanceSorts.append((sort.parent, newMask))
        Assertions.nonEmptyMask(newMask)
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
    return ExprArg(newInstanceSorts)


def addPrimitive(newSort, newMask, oldSort, oldMask, index, wasEmpty=False):
    newIndex = newSort.getNextIndex()
    cardinalityMask = newSort.getCardinalityMask()
    if wasEmpty:
        constraint = oldSort.isOn(oldMask.get(index))
    else:
        #only add this constraint if it is NOT the first set being added (needs to be modified to not look in the same set) (bag fix)
        constraint = And(oldSort.isOn(oldMask.get(index)), mAnd(*[oldSort.refs[index] != i for i in newMask.values()]))
    cardinalityMask.put(newIndex, If(constraint, 1, 0))
    newMask.put(newIndex, If(constraint, oldSort.refs[index], 0))
    Assertions.nonEmptyMask(newMask)


def joinWithPrimitive(arg):
    newInstanceSorts = []    
    for i in arg.getInstanceSorts():
        (sort, mask) = i
        if sort.refSort == "integer" or (sort.refSort == "string" and not Options.STRING_CONSTRAINTS):  #change for string soon
            newMask = alreadyExists(IntSort(), newInstanceSorts) #check that this works!!!
            if newMask.size() == 0:
                wasEmpty = True
            else:
                wasEmpty = False
            newSort = IntSort()
            for j in mask.keys():
                addPrimitive(newSort, newMask, sort, mask, j, wasEmpty)         
            newInstanceSorts.append((newSort, newMask)) #should change the "int", but not sure how yet
            Assertions.nonEmptyMask(newMask)
        elif sort.refSort == "string":
            '''fix this up'''
            newSort = StringSort()
            newMask = Mask()
            for i in mask.keys():
                newMask.put(i, sort.refs[i])
            newInstanceSorts.append((newSort, newMask))
        else:
            newMask = alreadyExists(RealSort(), newInstanceSorts) #check that this works!!!
            newSort = RealSort()
            for i in mask.keys():
                addPrimitive(newSort, newMask, sort, mask, i)         
            newInstanceSorts.append((newSort, newMask)) #should change the "int", but not sure how yet
            Assertions.nonEmptyMask(newMask)
    return ExprArg(newInstanceSorts)
    
def joinWithClaferRef(arg):
    newInstanceSorts = []
    for i in arg.getInstanceSorts():
        (sort, mask) = i
        while not sort.refSort:
            (sort, mask) = joinWithSuper(sort, mask)
        tempRefs = []
        newMask = alreadyExists(sort.refSort, newInstanceSorts)
        if isinstance(sort.refSort, PrimitiveType):
            return joinWithPrimitive(ExprArg([(sort, mask)]))
        for j in mask.keys():
            if isinstance(sort.refSort, PrimitiveType):
                tempRefs.append(If(sort.isOn(mask.get(j)),
                                   sort.refs[j], 0))
            else:
                tempRefs.append(If(sort.isOn(mask.get(j)),
                                   sort.refs[j], sort.refSort.numInstances))
        if isinstance(sort.refSort, PrimitiveType):
            for j in range(sort.numInstances):
                clause = mOr(*[k == j for k in tempRefs])
                newMask.put(j, mOr(newMask.get(j), clause))
        else:
            for j in range(sort.refSort.numInstances):
                clause = mOr(*[k == j for k in tempRefs])
                newMask.put(j, mOr(newMask.get(j), clause))
        newInstanceSorts.append((sort.refSort, newMask))
        Assertions.nonEmptyMask(newMask)
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
    return ExprArg(newInstanceSorts)
    
def joinWithRef(arg): 
    (sort, _) = arg.instanceSorts[0]
    if len(arg.instanceSorts) > 1:
        sys.exit("bug in join with ref, need to implement...")
    if isinstance(sort.refSort, PrimitiveType):
        return joinWithPrimitive(arg)
    else: 
        #join on ref sort
        #needs to be more robust for multiple instanceSorts
        return joinWithClaferRef(arg)


def joinWithClafer(left, right):
    newInstanceSorts = []
    for l in left.getInstanceSorts():
        (curr_left_sort, curr_left_mask) = l
        for r in right.getInstanceSorts():
            left_sort = curr_left_sort
            left_mask = curr_left_mask
            (right_sort, right_mask) = r
            noMatch = False
            while not(right_sort in left_sort.fields):
                if not left_sort.superSort:
                    noMatch = True
                    break
                (left_sort, left_mask) = joinWithSuper(left_sort, left_mask)
            if noMatch:
                continue
            newMask = alreadyExists(right_sort, newInstanceSorts)
            for i in right_mask.keys():
                (lower, upper, _) = right_sort.instanceRanges[i]
                for j in range(lower, upper + 1): 
                    #only possibly join with things that are in left
                    if left_mask.get(j):
                        prevClause = newMask.get(i)
                        newMask.put(i, mOr(prevClause, And(left_sort.isOn(left_mask.get(j)), 
                                                        right_sort.instances[i] == j)))
            '''CAREFUL!!! '''
            if newMask.size() == 0:
                #print(left)
                #print(right)
                continue
            newInstanceSorts.append((right_sort, newMask))
            Assertions.nonEmptyMask(newMask)
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, If(mask.get(j), sort.instances[j], sort.parentInstances))
    return ExprArg(newInstanceSorts)

def computeJoin(joinList):
    left = joinList.pop(0) 
    while joinList:
        right = joinList.pop(0)
        rightJoinPoint = right.getInstanceSort(0)
        if isinstance(rightJoinPoint, PrimitiveType):
            if rightJoinPoint == "parent":
                left = joinWithParent(left)
            elif rightJoinPoint == "ref":
                left = joinWithRef(left)
        else:
            left = joinWithClafer(left, right)
    for i in left.getInstanceSorts():
        (_, mask) = i
        Assertions.nonEmptyMask(mask)
    Assertions.nonEmpty(left.getInstanceSorts())
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
      
    
def getClaferMatch(key, my_list):
    '''
    returns the items in list with the same sort as key,
    along with the index of the instances in the supersort,
    along with True if the key is the subsort, else False
    '''
    matches = []
    for i in my_list:
        (sort, _) = i
        if key == sort:
            matches.append((True,0,i))
        else:
            totalIndexInSuper = 0
            tempKey = key
            while tempKey.superSort:
                totalIndexInSuper = totalIndexInSuper + tempKey.indexInSuper
                tempKey = tempKey.superSort
                if tempKey == sort:
                    matches.append((True, totalIndexInSuper, i))
                    break
            totalIndexInSuper = 0
            tempKey = sort
            while tempKey.superSort:
                totalIndexInSuper = totalIndexInSuper + tempKey.indexInSuper
                tempKey = tempKey.superSort
                if tempKey == key:
                    matches.append((False, totalIndexInSuper, i))
                    break
            
    return matches

def find(key, l):
    for i in l:
        (sort, mask) =  i
        if sort == key:
            return mask
    
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
    unmatchedL = [(sort, mask.copy()) for (sort,mask) in sortedL]
    unmatchedR = [(sort, mask.copy()) for (sort,mask) in sortedR]
    
    #integer equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if isinstance(left_sort, IntSort) or isinstance(right_sort, IntSort):
        return BoolArg([sum(*[left_mask.values() for (_, left_mask) in left.getInstanceSorts()]) 
                        == sum(*[right_mask.values() for (_, right_mask) in right.getInstanceSorts()])])
    #real equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if isinstance(left_sort, RealSort) or isinstance(right_sort, RealSort):
        return BoolArg([sum(*[left_mask.values() for (_, left_mask) in left.getInstanceSorts()]) 
                        == sum(*[right_mask.values() for (_, right_mask) in right.getInstanceSorts()])])
    #string equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if isinstance(left_sort, StringSort) or isinstance(right_sort, StringSort):
        return BoolArg([left_mask.get(0) == right_mask.get(0)])
        #return BoolArg([sum(*[left_mask.values() for (_, left_mask) in left.getInstanceSorts()]) 
        #                == sum(*[right_mask.values() for (_, right_mask) in right.getInstanceSorts()])])
    #clafer-set equality case
    else:
        cond = []
        for i in sortedL:
            (left_sort, left_mask) = i
            matches = getClaferMatch(left_sort, sortedR)
            for j in matches:
                (leftIsSub, transform, (right_sort,right_mask)) = j
                if leftIsSub:
                    sub_sort = left_sort
                    sub_mask = left_mask
                    super_mask = right_mask
                    super_sort = right_sort
                    unmatchedSub = unmatchedL
                    unmatchedSuper = unmatchedR
                else:
                    sub_sort = right_sort
                    sub_mask = right_mask
                    super_mask = left_mask
                    super_sort = left_sort
                    unmatchedSub = unmatchedR
                    unmatchedSuper = unmatchedL
                #unmatched extension
                unmatchedSubMask = find(sub_sort, unmatchedSub)
                unmatchedSuperMask = find(super_sort, unmatchedSuper)
                for i in sub_mask.keys():
                    unmatchedSubMask.remove(i)
                    unmatchedSuperMask.remove(i+transform)
                #end unmatched extension
                for k in sub_mask.keys():
                    if not super_mask.get(k + transform):
                        cond.append(sub_sort.isOff(sub_mask.get(k)))
                    else:
                        cond.append(And(Implies(sub_sort.isOn(sub_mask.get(k)),
                                            super_sort.isOn(super_mask.get(k + transform))),
                                        Implies(super_sort.isOn(super_mask.get(k + transform)),
                                            sub_sort.isOn(sub_mask.get(k)))))
        #unmatched extension
        for i in unmatchedL + unmatchedR:
            (sort, mask) = i
            for j in mask.keys():
                cond.append(sort.isOff(mask.get(j)))
        return BoolArg([mAnd(*cond)])
        
            
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
    
    #if(left_mask.size() > 1 or right_mask.size() > 1):
    #    print("bug clafer makes no sense.")
    lval = sum(left_mask.values())
    rval = sum(right_mask.values())
    #else:
    #    lval = left_mask.pop_value()
    #    rval = right_mask.pop_value()
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
    #lval = left_mask.pop_value()
    #rval = right_mask.pop_value()
    lval = sum(left_mask.values())
    rval = sum(right_mask.values())
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
    unmatchedL = [(sort, mask.copy()) for (sort,mask) in sortedL]
    
    #integer equality case
    #boolean equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if isinstance(left_sort, BoolSort) or isinstance(right_sort, BoolSort):
        return BoolArg([Implies(left_mask.pop_value(), right_mask.pop_value())])
    elif isinstance(left_sort, IntSort) or isinstance(right_sort, IntSort):
        return BoolArg([int_set_in((left_sort, left_mask), (right_sort, right_mask))])
    #clafer-set equality case
    else:
        cond = []
        for i in sortedL:
            (left_sort, left_mask) = i
            matches = getClaferMatch(left_sort, sortedR)
            for j in matches:
                (leftIsSub, transform, (right_sort,right_mask)) = j
                if leftIsSub:
                    sub_sort = left_sort
                    sub_mask = left_mask
                    super_mask = right_mask
                    super_sort = right_sort
                else:
                    sub_sort = right_sort
                    sub_mask = right_mask
                    super_mask = left_mask
                    super_sort = left_sort
                #unmatched extension
                unmatchedMask = find(left_sort, unmatchedL)
                for i in sub_mask.keys():
                    unmatchedMask.remove(i)
                    unmatchedMask.remove(i+transform)
                #end unmatched extension
                for k in sub_mask.keys():
                    if not super_mask.get(k + transform) and leftIsSub:
                        cond.append(sub_sort.isOff(sub_mask.get(k)))
                    elif leftIsSub:
                        cond.append(Implies(sub_sort.isOn(sub_mask.get(k)),
                                            super_sort.isOn(super_mask.get(k + transform))))
                    else:
                        cond.append(Implies(super_sort.isOn(super_mask.get(k + transform)),
                                            sub_sort.isOn(sub_mask.get(k))))
        #unmatched extension
        for i in unmatchedL:
            (sort, mask) = i
            for j in mask.keys():
                cond.append(sort.isOff(mask.get(j)))
        return BoolArg([mAnd(*cond)])
    '''
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
        Assertions.nonEmpty(cond)
        return BoolArg([And(*cond)])
    #return BoolArg([mAnd(*[Implies(i,j) for i,j in zip(left.instances, right.instances)])])
    '''

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
    leftcopy = left.clone()
    rightcopy = right.clone()
    leftResult = op_implies(left, right)
    rightResult = op_implies(rightcopy, leftcopy)
    lval = leftResult.getValue()
    rval = rightResult.getValue()
    cond = [And(lval, rval)]
    return BoolArg(cond)
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

def int_set_union(leftIntSort, rightIntSort):
    (_,(left_sort, left_mask)) = leftIntSort
    (_,(right_sort, right_mask)) = rightIntSort
    newMask = Mask()
    sort = IntSort()
    for i in left_mask.keys():
        sort.cardinalityMask.put(i, left_sort.cardinalityMask.get(i))
        newMask.put(i, If(left_sort.cardinalityMask.get(i) == 1, left_mask.get(i), 0))
    delta = left_mask.size()
    for i in right_mask.keys():
        constraint = And(right_sort.cardinalityMask.get(i) == 1, 
                         *[Or(left_mask.get(j) != right_mask.get(i), left_sort.cardinalityMask.get(j) == 0) for j in left_mask.keys()])
        sort.cardinalityMask.put(i + delta, If(constraint, 1, 0))
        newMask.put(i+delta, If(constraint, right_mask.get(i), 0))
    return (sort, newMask)

    

def putIfNotMatched(sort, mask, index, value, matches):
    if not matches:
        mask.put(index, value)
    else:
        cond = []
        for i in matches:
            (leftIsSub, transform, (match_sort,match_mask)) = i
            if leftIsSub:
                if match_mask.get(index + transform):
                    cond.append(match_sort.isOff(match_mask.get(index + transform)))
            else:
                if match_mask.get(index - transform):
                    cond.append(match_sort.isOff(match_mask.get(index - transform)))
        if not cond:
            mask.put(index, value)
        else:
            mask.put(index, If(mAnd(*cond), value, sort.parentInstances))
           
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
        (_, (sort,_))=nextSorts[0]
        matches = getClaferMatch(sort, newInstanceSorts)
        if len(nextSorts) == 1:
            if not matches:
                (_, nextInstanceSort) = nextSorts[0]
                newInstanceSorts.append(nextInstanceSort)
            else:
                (_, (sort, mask)) = nextSorts[0]
                newMask = Mask()
                for i in mask.keys():
                    putIfNotMatched(sort, newMask, i, mask.get(i), matches)
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            
            if isinstance(sort, IntSort):
                (sort, newMask) = int_set_union(nextSorts[0],nextSorts[1])
            
            newMask = Mask()
            for i in l.difference(r.getTree()):
                putIfNotMatched(sort, newMask, i, l.get(i), matches)
            for i in r.difference(l.getTree()):
                putIfNotMatched(sort, newMask, i, r.get(i), matches)
            for i in l.intersection(r.getTree()):
                putIfNotMatched(sort, newMask, i, Common.min2(l.get(0), r.get(0)), matches)
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
        (_, (sort,_))=nextSorts[0]
        matches = getClaferMatch(sort, newInstanceSorts)
        if len(nextSorts) == 1:
            continue
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            newMask = Mask()
            for i in l.intersection(r.keys()):
                #newMask.put(i, Common.max2(l.get(0), r.get(0)))
                putIfNotMatched(sort, newMask, i, Common.max2(l.get(0), r.get(0)), matches)
            newInstanceSorts.append((sort, newMask))
    return ExprArg(left.joinSorts, newInstanceSorts)

def int_set_difference(leftIntSort, rightIntSort):
    (_,(left_sort, left_mask)) = leftIntSort
    (_,(right_sort, right_mask)) = rightIntSort
    
    newMask = Mask()
    sort = IntSort()
    for i in left_mask.keys():
        constraint = And(left_sort.cardinalityMask.get(i) == 1, 
                         *[Or(left_mask.get(i) != right_mask.get(j), right_sort.cardinalityMask.get(j) == 0) for j in right_mask.keys()])
        sort.cardinalityMask.put(i, If(constraint, 1, 0))
        newMask.put(i, If(constraint, left_mask.get(i), 0))
    return (sort, newMask)

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
        (_, (sort,_))=nextSorts[0]
        matches = getClaferMatch(sort, newInstanceSorts)
        if len(nextSorts) == 1:
            (side, nextInstanceSort) = nextSorts[0]
            if(side == "l"):
                if not matches:
                    newInstanceSorts.append(nextInstanceSort)
                else:
                    (sort, mask) = nextInstanceSort
                    newMask = Mask()
                    for i in mask.keys():
                        putIfNotMatched(sort, newMask, i, mask.get(i), matches)
                    newInstanceSorts.append((sort, newMask))
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            
            if isinstance(sort, IntSort):
                (sort, newMask) = int_set_difference(nextSorts[0], nextSorts[1])
            else:
                newMask = Mask()
                for i in l.difference(r.getTree()):
                    #newMask.put(i, l.get(i))
                    putIfNotMatched(sort, newMask, i, l.get(i), matches)
                for i in l.intersection(r.getTree()):
                    #newMask.put(i, If(sort.isOn(r.get(i))
                    #                     , l.get(i)
                    #                     , sort.parentInstances))
                    putIfNotMatched(sort, newMask, i, If(sort.isOn(r.get(i))
                                         , l.get(i)
                                         , sort.parentInstances), matches)
            newInstanceSorts.append((sort, newMask))
    return ExprArg(newInstanceSorts)
    
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


'''
CHECKED UNDER HERE********************************************************************************************
'''         

def int_set_in(leftIntSort, rightIntSort):
    (left_sort, left_mask) = leftIntSort
    (right_sort, right_mask) = rightIntSort
    cond = []
    for i in left_mask.keys():
        constraint = Or(left_sort.cardinalityMask.get(i) == 0, 
                        Or(*[And(right_sort.cardinalityMask.get(j) == 1, 
                                 right_mask.get(j) == left_mask.get(i)) for j in right_mask.keys()]))
        cond.append(constraint)
    return(And(*cond))


def op_in(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that left is a subset of right.
    '''
    return op_implies(left,right)
    '''
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    cond = []
    for i in sortedL:
        (left_sort, left_mask) = i
        matches = getMatch(left_sort, sortedR)
        if isinstance(left_sort, IntSort):
            assert(matches) #must have ints in both sets (i think the front-end ensures this
            cond.append(int_set_in(i, matches[0][1]))
        else:
            for j in matches:
                (transform, (right_sort,right_mask)) = j
                for k in left_mask.keys():
                    if not right_mask.get(k + transform):
                        cond.append(left_sort.isOff(left_mask.get(k)))
                    else:
                        cond.append(Implies(left_sort.isOn(left_mask.get(k)),
                                            right_sort.isOn(right_mask.get(k + transform))))
    return BoolArg([mAnd(*cond)])
   '''

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
# STRINGS
#######################################################################
'''

''' need to improve to handle multiple strings'''

def op_concat(left, right):
    (_, left_mask) = left.getInstanceSort(0)
    left_i = left_mask.get(0)
    (_, right_mask) = right.getInstanceSort(0)
    right_i = right_mask.get(0)
    return IntArg(["Concat$" + left_i + "$" + right_i])

def op_length(arg):
    (_, mask) = arg.getInstanceSort(0)
    arg_i = mask.get(0)
    stringID = Common.STRCONS_SUB + str(Common.getStringUID())
    Common.string_map[stringID] = arg_i
    return IntArg([Int("Length$" + str(stringID))])

def op_substring(whole_string, left_index, right_index):
    (_, whole_mask) = whole_string.getInstanceSort(0)
    whole_i = whole_mask.get(0)
    left_stringID = Common.STRCONS_SUB + str(Common.getStringUID())
    right_stringID = Common.STRCONS_SUB + str(Common.getStringUID())
    Common.string_map[left_stringID] = left_index
    Common.string_map[right_stringID] = right_index
    return IntArg(["Substring$" + whole_i + "$" + left_stringID + "$" + right_stringID])

def op_replace(whole_string, from_string, to_string):
    (_, whole_mask) = whole_string.getInstanceSort(0)
    whole_i = whole_mask.get(0)
    (_, from_mask) = from_string.getInstanceSort(0)
    from_i = from_mask.get(0)
    (_, to_mask) = to_string.getInstanceSort(0)
    to_i = to_mask.get(0)
    return IntArg(["Replace$" + whole_i + "$" + from_i + "$" + to_i])

def op_split(left, right):
    sys.exit("Split not implemented.")

def op_contains(left, right):
    (_, left_mask) = left.getInstanceSort(0)
    left_i = left_mask.get(0)
    (_, right_mask) = right.getInstanceSort(0)
    right_i = right_mask.get(0)
    return BoolArg(["Contains$" + left_i + "$" + right_i])

def op_indexof(left, right):
    (_, mask) = left.getInstanceSort(0)
    left_i = mask.get(0)
    (_, mask) = right.getInstanceSort(0)
    right_i = mask.get(0)
    return IntArg([Int("Indexof$" + left_i + "$" + right_i)])

'''
#######################################################################
# END STRINGS
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
    return mOr(*condList)

def quant_all(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [Implies(i, j) for i,j in zip(ifConstraints, condList)]
    return mAnd(*condList)

def quant_no(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [And(i, j) for i,j in zip(ifConstraints, condList)]
    return Not(Or(*condList))

EXPR = ""
EXPR2 = ""

def quant_one(exprs, ifConstraints):
    '''
    There's probably a better way to do this.
    '''
    condList = getQuantifierConditionList(exprs)
    #print(ifConstraints)
    #print(condList)
    if ifConstraints:
        condList = [And(i, j) for i,j in zip(ifConstraints, condList)]
    exprList = []
    for i in range(len(condList)):
        #exprList.append(If(condList[i], indicatorVars[i] == 1, indicatorVars[i] == 0))
        exprList.append(If(condList[i], 1, 0))
    return Sum(*exprList) == 1
    
def quant_lone(exprs, ifConstraints):
    return Or(quant_no(exprs, ifConstraints), quant_one(exprs, ifConstraints))

''' 
#######################################################################
# END QUANTIFIERS
#######################################################################
''' 

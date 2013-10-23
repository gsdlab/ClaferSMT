'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from bintrees.avltree import AVLTree
from common import Common
from common.Common import mOr, mAnd
from constraints import Constraints
from constraints.Constraints import GenericConstraints
from lxml.builder import basestring
from structures.ExprArg import ExprArg, IntArg, BoolArg, Mask
from z3 import Function, IntSort, BoolSort, If, Not, Sum, Implies, Or, And, Xor
import inspect
import sys


#FIX ME
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

def joinHelper(left, right, zeroedVal):
    '''
    :param leftSort:
    :type leftSort: :class:`~common.ClaferSort`
    :param rightSort:
    :type rightSort: :class:`~common.ClaferSort`
    :param linstances:
    :type linstances: [Int()]
    :param rinstances:
    :type rinstances: [Int()]
    :param zeroedVal: the number of parentInstances of rightSort, or zero if rightSort is "int"
    :type zeroedVal: int
    :returns: Z3-function(int, int) 
    
    Creates a Z3-function that ranges over len(rinstances). For each index in rinstances, 
    returns the instance if its corresponding instance in linstances is on
    , else the instances is *masked* to be zeroedVal. ::
    
    >>> zeroedVal = 3
    >>> leftSort.parentInstances = 1
    >>> linst = [0,0,1]
    >>> rinst = [0,1,1,2,2,3]
    >>> join([0,0,1], [0,1,1,2,2,3]) 
    >>>    => [mask(0), mask(1), mask(1), mask(2), mask(2), mask(3]]
    >>>    => [0,1,1,3,3,3]
    
    Here, since linst[2] = leftSort.parentInstances, any instance in rinstances that points to linst[2] is *zeroed*. 
    The other instances remain the same.
    '''
    leftJoinPoint = left.joinSorts[-1]
    rightJoinPoint = right.joinSorts[0]
    
    #get the instanceSorts associated with the join point.
    for i in left.instanceSorts:
        (left_sort, left_mask) = i
        if isinstance(left_sort, basestring) or left_sort == leftJoinPoint:
            break
    for i in right.instanceSorts:
        (right_sort, right_mask) = i #FIXME
        if isinstance(right_sort, basestring) or right_sort == rightJoinPoint:
            break
        
    #create cond for join
    condList = []
    onInstancesList = []
    count = 0
    '''
    for i in range(len(left_mask)):
        if left_mask[i]:
            condList.append(left.instances[count] != leftJoinPoint.parentInstances)
            onInstancesList.append(i) 
            count = count + 1
    '''
    newMaskList = []
    condList = []
    #should be very fine-grained for the solver, but might bog down translation, not sure yet
    newMask = Mask()
    for i in right_mask.keys():
        (lower, upper, _) = rightJoinPoint.instanceRanges[i]
        for j in range(lower, upper + 1):
            #only possibly join with things that are in left
            if left_mask.get(j):
                prevClause = newMask.get(i)
                newMask.put(i, mOr(prevClause, And(left_mask.get(j) != left_sort.parentInstances, 
                                                right_mask.get(i) == j)))
        #if leftJoinInstances:
         #   newMaskList.append(i)
         #   condList.append(mOr(*[And(left_mask.get(k) != leftJoinPoint.parentInstances, rightJoinPoint.instances[i] == k) for k in leftJoinInstances]))
    for i in newMask.keys():
        newMask.put(i, If(newMask.get(i), right_mask.get(i) , zeroedVal))
    return newMask
    '''
    (sort, mask) = left.instanceSorts[0]
    newMask = Mask()
    for i in mask.keys():
        (lower,upper,_) = sort.instanceRanges[i]
        for j in range(lower, upper + 1):
            prevClause = newMask.get(j)
            newMask.put(j, mOr(prevClause, mask.get(i) == j))
    
    funcID = str(Common.getFunctionUID())
    functionName = "f" + funcID + "_" + leftJoinPoint.element.nonUniqueID() + "." + rightJoinPoint.element.nonUniqueID()
    joinFunction = Function(functionName, IntSort(), IntSort())
    joinHelperFunction = Function("h" + functionName , IntSort(), IntSort())
    constraints = []
    for i in range(len(left.instances)):
        constraints.append(joinHelperFunction(i) == left.instances[i]) 
    constraints.append(joinHelperFunction(len(left.instances)) == leftJoinPoint.parentInstances)
    for i in range(len(right.instances)):  #rinstance[i] in joinHelperFunction arg
        constraints.append(joinFunction(i) == If(joinHelperFunction(rightJoinPoint.instances[i]) != leftJoinPoint.parentInstances, right.instances[i], zeroedVal))
    constraints.append(joinFunction(len(right.instances)) == zeroedVal)
    leftJoinPoint.z3.join_constraints.addAll(constraints)
    return joinFunction
    '''

#can optimize this.parent
#need to range newInstances over ALL sorts in instanceSorts (don't have a test case yet)
#   for example, leftJoinPoint.parentInstances CHANGES if there are multiple sorts here
#XXX
def op_join(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns the join of left and right, using the join function created in createJoinFunction().
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    
    leftJoinPoint = left.joinSorts[-1]
    rightJoinPoint = right.joinSorts[0]
    newInstances = []
    
    if isinstance(rightJoinPoint, basestring):
        if rightJoinPoint == "parent":
            joinSorts = left.joinSorts + [leftJoinPoint.parent] +  [right.joinSorts[i] for i in range(1, len(right.joinSorts))]
            (sort, mask) = left.instanceSorts[0]
            newMask = Mask()
            for i in mask.keys():
                (lower,upper,_) = sort.instanceRanges[i]
                for j in range(lower, upper + 1):
                    if j == leftJoinPoint.parentInstances:
                        break
                    prevClause = newMask.get(j)
                    newMask.put(j, mOr(prevClause, mask.get(i) == j))
                    #*[j == i for j in left.instances])
                #newInstances.append(If(clause, leftJoinPoint.parent.instances[i], leftJoinPoint.parent.parentInstances))
            for i in newMask.keys():
                newMask.put(i, If(newMask.get(i), leftJoinPoint.parent.instances[i], leftJoinPoint.parent.parentInstances))
            return ExprArg(joinSorts, [(leftJoinPoint.parent, newMask)])
        elif rightJoinPoint == "ref":
            if isinstance(leftJoinPoint.refSort, basestring):
                if leftJoinPoint.refSort == "integer":
                    mask = left.getInstanceMask(leftJoinPoint)
                    newInstances = []
                    newMask = Mask()
                    for i in mask.keys():
                        newMask.put(i, If(mask.get(i) != leftJoinPoint.parentInstances, leftJoinPoint.refs[i], 0))
                    return(ExprArg(left.joinSorts + ["int"], 
                                   [("int", newMask)] ))   
                else:
                    print("Error on: " + leftJoinPoint.refSort + "string refs other than int (e.g. double) unimplemented")
                    sys.exit()
            else: 
                #join on ref sort
                joinSorts = left.joinSorts + [leftJoinPoint.refSort] +  [right.joinSorts[i] for i in range(1, len(right.joinSorts))]
                #needs to be more robust for multiple instanceSorts
                (sort, mask) = left.instanceSorts[0]
                tempRefs = []
                newMask = Mask()
                for i in mask.keys():
                    # **** the "else" used to be refSort.parentInstances, but i think this is right
                    tempRefs.append(If(mask.get(i) != leftJoinPoint.parentInstances,
                                       leftJoinPoint.refs[i], leftJoinPoint.refSort.numInstances))
                for i in range(leftJoinPoint.refSort.numInstances):
                    clause = mOr(*[j == i for j in tempRefs])
                    newMask.put(i, If(clause, leftJoinPoint.refSort.instances[i], leftJoinPoint.refSort.parentInstances))
                return(ExprArg(joinSorts, [(leftJoinPoint.refSort, newMask)]))
                '''
                for j in range(sort.numInstances):
                    if mask[j]:
                        tempRefs.append(If(left.instances[count] != leftJoinPoint.parentInstances
                                           , leftJoinPoint.refs[j], leftJoinPoint.refSort.parentInstances))
                        count = count + 1
                for i in range(leftJoinPoint.refSort.numInstances):
                    
                    clause = mOr(*[j == i for j in tempRefs])
                    newInstances.append(If(clause, leftJoinPoint.refSort.instances[i], leftJoinPoint.refSort.parentInstances))
                return(ExprArg(joinSorts, [(leftJoinPoint.refSort, newMask)]))
                '''
    else:
        #Make more robust
        instanceSort = left.instanceSorts[0]
        (leftJoinPoint, leftMask) = instanceSort
        while not(rightJoinPoint in leftJoinPoint.fields):
            (leftJoinPoint, leftMask) = joinWithSuper(leftJoinPoint, leftMask)
            #(leftJoinPoint, leftInstances) = joinWithSuper(leftJoinPoint, leftInstances)
        instanceSorts = right.instanceSorts
        (sort, mask) = instanceSorts[0]
        if(isinstance(sort,basestring) and sort == "int"):
            zeroedVal = 0
        else:
            zeroedVal = sort.parentInstances
        newJoinSorts = left.joinSorts[:]
        newJoinSorts.append(leftJoinPoint)
        newLeft = ExprArg(newJoinSorts, [(leftJoinPoint, leftMask)])
        newInstanceSorts = [(rightJoinPoint, joinHelper(newLeft, right, zeroedVal))]
        joinSorts = newLeft.joinSorts + right.joinSorts
        return(ExprArg(joinSorts, newInstanceSorts))

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
    for i in arg.instanceSorts:
        (sort, mask) = i
        '''
        for j in range(ExprArg.getUnmaskedCount(mask)):
            newInstances.append(If(arg.instances[j] != sort.parentInstances, 1, 0))
        '''
        for j in mask.values():
            instances.append(If(j != sort.parentInstances, 1, 0))  
    return IntArg([Sum(instances)])

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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, mask) = arg.instanceSorts[0]
    val = mask.pop_value()
    return IntArg([-(val)])
    

def op_not(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Boolean negation of arg.
    '''
    assert isinstance(arg, ExprArg)
    (_, mask) = arg.instanceSorts[0]
    val = mask.pop_value()
    return BoolArg([Not(val)])
    
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
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.instanceSorts])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.instanceSorts])
    
    #integer equality case
    (sort, left_mask) = left.instanceSorts[0]
    if isinstance(sort, basestring) and sort == "int":
        (_, right_mask) = right.instanceSorts[0]
        return BoolArg([sum(left_mask.values()) == sum(right_mask.values())])
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
                    cond.append(i == sort.parentInstances)
                    
            else:
                (_, (sort, l)) = nextSorts[0]
                (_, (_, r)) = nextSorts[1]
                newMask = Mask()
                
                for i in l.difference(r.getTree()):
                    cond.append(l.get(i) == sort.parentInstances)
                for i in r.difference(l.getTree()):
                    cond.append(r.get(i) == sort.parentInstances)
                for i in l.intersection(r.getTree()):
                    cond.append(mAnd(Implies(l.get(i) != sort.parentInstances,
                                              r.get(i) != sort.parentInstances),
                                          Implies(l.get(i) == sort.parentInstances,
                                              r.get(i) == sort.parentInstances)))
        return BoolArg([And(*cond)])
        #return BoolArg([mAnd(*[i == j for i,j in zip(left.instances, right.instances)])])
    '''
    if(isinstance(left.instances, list) and isinstance(right.instances, list)):
        #ref case
        if isinstance(left.instanceSorts[0], basestring) and left.instanceSorts[0] == "int":
            return BoolArg([sum(left.instances) == sum(right.instances)])
        else:
            return BoolArg(And(*[i == j for i,j in zip(left.instances, right.instances)]))
    elif(isinstance(left.instances, list)):
        return BoolArg(sum(*left.instances) == right.instances)
    elif(isinstance(right.instances, list)):
        return BoolArg(sum(right.instances) == left.instances)
    else:
        return BoolArg(left.instances == right.instances)  
    '''
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
    for i in expr.instanceSorts:
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    (_, left_mask) = left.instanceSorts[0]
    (_, right_mask) = right.instanceSorts[0]
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
    return BoolArg([mAnd(*[Implies(i,j) for i,j in zip(left.instances, right.instances)])])

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
    return BoolArg([mAnd(*[mAnd(Implies(i,j), Implies(j,i)) for i,j in zip(left.instances, right.instances)])])
    
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
    return BoolArg([If(cond.instances[0], ifExpr.instances[0], elseExpr.instances[0])])

#THIS IS NO LONGER USED
def set_extend(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Extends two sets to facilitate set operations.
    Simplified Example: ::
    
    >>> Extend(Set(A,B), Set(B,C)) => (Set(A,B,C), Set(A,B,C))
    
    In this case, the C's in the left set are "zeroed", and the A's in the right set are "zeroed."
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    left = ExprArg(left.joinSorts[:], left.instanceSorts[:], left.instances[:])
    right = ExprArg(right.joinSorts[:], right.instanceSorts[:], right.instances[:])
    finalSorts = []
    finalJoinSorts = []
    finalLinstances = []
    finalRinstances = []
    while left.instanceSorts or right.instanceSorts:
        if (not right.instanceSorts):
            (nextSort, nextMask) = left.instanceSorts.pop(0)
            newLeftInstances = Common.getInstancesFromMask(nextSort, nextMask, left.instances)
            nextJoinSort = left.joinSorts.pop(0)
            finalLinstances = finalLinstances + newLeftInstances
            finalRinstances = finalRinstances + [nextSort.parentInstances for _ in newLeftInstances]
        elif (not left.instanceSorts):
            (nextSort, nextMask) = right.instanceSorts.pop(0)
            newRightInstances = Common.getInstancesFromMask(nextSort, nextMask, right.instances)
            nextJoinSort = right.joinSorts.pop(0)
            finalLinstances = finalLinstances + [nextSort.parentInstances for _ in newRightInstances]
            finalRinstances = finalRinstances + newRightInstances
        else:
            (nextLeftSort, _) = left.instanceSorts[0]
            (nextRightSort, _) = right.instanceSorts[0]
            if nextLeftSort.element.uid < nextRightSort.element.uid:
                (nextSort, nextMask) = left.instanceSorts.pop(0)
                newLeftInstances = Common.getInstancesFromMask(nextSort, nextMask, left.instances)
                nextJoinSort = left.joinSorts.pop(0)
                finalLinstances = finalLinstances + newLeftInstances
                finalRinstances = finalRinstances + [nextSort.parentInstances for _ in newLeftInstances]
            elif nextLeftSort.element.uid > nextRightSort.element.uid:
                (nextSort, nextMask) = right.instanceSorts.pop(0)
                newRightInstances = Common.getInstancesFromMask(nextSort, nextMask, right.instances)
                nextJoinSort = right.joinSorts.pop(0)
                finalLinstances = finalLinstances + [nextSort.parentInstances for _ in newRightInstances]
                finalRinstances = finalRinstances + newRightInstances
            else:
                (nextSort, nextLeftMask) = left.instanceSorts.pop(0)
                (_, nextRightMask) = right.instanceSorts.pop(0)
                nextJoinSort = left.joinSorts.pop(0)
                right.joinSorts.pop(0)
                #overlay the masks
                nextMask = []
                for i in range(nextSort.numInstances):
                    if nextLeftMask[i] or nextRightMask[i]:
                        nextMask.append(True)
                    else:
                        nextMask.append(False)
                for i in range(nextSort.numInstances):
                    if nextMask[i]:
                        if nextLeftMask[i]:
                            finalLinstances.append(left.instances.pop(0))
                        else:
                            finalLinstances.append(nextSort.parentInstances)
                        if nextRightMask[i]:
                            finalRinstances.append(right.instances.pop(0))
                        else:
                            finalRinstances.append(nextSort.parentInstances)
        finalSorts.append((nextSort, nextMask))
        finalJoinSorts.append(nextJoinSort)
    return(ExprArg(finalJoinSorts, finalSorts, finalLinstances), 
           ExprArg(finalJoinSorts, finalSorts, finalRinstances))

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
    else: #end outer
        return []
        

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
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.instanceSorts])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.instanceSorts])
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
    return ExprArg(left.joinSorts, newInstanceSorts)
                
  
def op_intersection(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set intersection (left & right)
    '''
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.instanceSorts])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.instanceSorts])
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
    (extendedL, extendedR) = set_extend(left,right)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.instanceSorts])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.instanceSorts])
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
            for i in l.intersection(r.keys()):
                newMask.put(i, If(r.get(i) != sort.parentInstances
                                     , l.get(i)
                                     , sort.parentInstances))
            newInstanceSorts.append((sort, newMask))
    return ExprArg(left.joinSorts, newInstanceSorts)
    
    '''
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            linstance = extendedL.instances.pop(0)
            rinstance = extendedR.instances.pop(0)
            finalInstances.append(If(mAnd(linstance != i.parentInstances, rinstance == i.parentInstances)
                                     , linstance
                                     , i.parentInstances))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)
    '''

def op_in(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that left is a subset of right.
    '''
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.instanceSorts])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.instanceSorts])
    cond = []
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            (side, (sort, l)) = nextSorts[0]
            if side == "l":
                #make sure nothing on the left is on, since it cant be in the right
                for i in l.values():
                    cond.append(i == sort.parentInstances)
                
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            for i in l.difference(r.getTree()):
                cond.append(l.get(i) == sort.parentInstances)
            for i in l.intersection(r.getTree()):
                cond.append(Implies(l.get(i) != sort.parentInstances,
                                          r.get(i) != sort.parentInstances))
    return BoolArg([And(*cond)])
    
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (extendedL, extendedR) = set_extend(left,right)
    finalExpr = True
    for i in extendedL.instanceSorts:
        (sort, mask) = i
        for j in range(sort.numInstances):
            if mask[j]:
                finalExpr = mAnd(finalExpr, Implies(extendedL.instances.pop(0) != sort.parentInstances, 
                                                   extendedR.instances.pop(0) != sort.parentInstances))
    return BoolArg([finalExpr])
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

def op_sum(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Computes the sum of all integer instances in arg. May not match the semantics of the Alloy backend.
    '''
    assert isinstance(arg, ExprArg)
    instances = []
    for i in arg.instanceSorts:
        (_, mask) = i
        for j in mask.values():
            instances.append(j)
    return IntArg([Sum(instances)])

'''
    Map used to convert Clafer operations to Z3 operations
    keys: operation(str) returned by Clafer Python generator
    values: pairs:
        1. arity
        2. function associated with the operator
'''
ClaferToZ3OperationsMap = {
                           #Unary Ops
                           "!"           : (1, op_not),
                           "UNARY_MINUS" : (1, op_un_minus),
                           "#"           : (1, op_card),
                           "max"         : (1, "TODO"),
                           "min"         : (1, "TODO"),
                           "sum"         : (1, op_sum),    
                           #Binary Ops
                           "<=>"         : (2, op_equivalence),
                           "=>"          : (2, op_implies),
                           "||"          : (2, op_or),
                           "xor"         : (2, op_xor),
                           "&&"          : (2, op_and),
                           "<"           : (2, op_lt),
                           ">"           : (2, op_gt),
                           "<="          : (2, op_le),
                           ">="          : (2, op_ge),
                           "="           : (2, op_eq),
                           "!="          : (2, op_ne),
                           "in"          : (2, op_in),
                           "nin"         : (2, op_nin),
                           "+"           : (2, op_add),
                           "-"           : (2, op_sub),
                           "*"           : (2, op_mul),
                           "/"           : (2, op_div),
                           "++"          : (2, op_union),
                           "--"          : (2, op_difference),
                           "&"           : (2, op_intersection),
                           "<:"          : (2, op_domain_restriction),
                           ":>"          : (2, op_range_restriction),
                           "."           : (2, op_join),
                           #Ternary Ops
                           "ifthenelse"  : (3, op_ifthenelse)       
                           }

def getOperationConversion(op):
    '''
    :param op: String representation of Clafer operation.
    :type op: str
    :returns: 2-tuple from ClaferToZ3OperationsMap with the fields:
    
    The 2-tuple has the fields:
        1. arity of the function
        2. function associated with the operator
    '''
    return ClaferToZ3OperationsMap[op]


class BracketedConstraint(Constraints.GenericConstraints):
    '''
    :var stack: ([]) Used to process a tree of expressions.
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, z3, claferStack):
        GenericConstraints.__init__(self)
        self.z3 = z3
        self.claferStack = claferStack
        self.stack = []
        self.locals = {}
        self.value = "bracketed constraint"
        
    def addLocal(self, uid, expr):
        self.locals[uid] = expr
    
    def addArg(self, arg):
        self.stack.append(arg)
       
    #clean     
    def addQuantifier(self, quantifier, num_args, num_quantifiers, num_combinations, ifconstraints):
        localStack = []
        ifConstraints = []
        finalInstances = []
        for _ in range(num_combinations):
            localStack.append(self.stack.pop())
            if ifconstraints:
                ifConstraints.append(ifconstraints.pop())
            else:
                ifConstraints = []
        localStack.reverse()
        ifConstraints.reverse()
        condList = []
        for q in range(num_combinations):
            instances = []
            instanceSorts = []
            finalInnerInstances = []
            
            
            currExpr = localStack.pop(0)
            if ifConstraints:
                currIfConstraint = ifConstraints.pop(0)
            else:
                currIfConstraint = None
            '''
            for i in currExpr:
                instances = instances + i.instances
                instanceSorts = instanceSorts + i.instanceSorts
            '''
            if quantifier == "Some":
                cond = False
                for i in currExpr:
                    for j in i.instanceSorts:
                        (sort, mask) = j
                        for k in mask.keys():
                            cond = mOr(cond, mask.get(k) != sort.parentInstances)
                condList.append(cond)
                '''
                for i in instances:
                    innerExpr = False
                    if instanceSorts and not isinstance(instanceSorts[0], basestring):
                        for i in instanceSorts:
                            (sort, mask) =  i
                            newInstances = Common.getInstancesFromMask(sort, mask, instances)
                            for j in range(sort.numInstances): 
                                innerExpr = Or(innerExpr, 
                                               Or(*[k != sort.parentInstances for k in newInstances]))
                    else:
                        #refactor me
                        j = 0
                        innerExpr = mOr(innerExpr, 
                                               mOr(*[k for k in  newInstances]))
                    #finalInnerInstances.append(innerExpr)
                finalInstances = mOr(finalInstances, innerExpr)
                '''
            elif quantifier == "All":
                cond = []
                for i in currExpr:
                    for j in i.instanceSorts:
                        (sort, mask) = j
                        for k in mask.keys():
                            if isinstance(sort,basestring) and sort == "bool":
                                cond.append(mask.get(k))
                            else:
                                cond.append(mask.get(k) != sort.parentInstances)
                cond = And(*cond)
                if currIfConstraint:
                    cond = Implies(currIfConstraint, cond)
                condList.append(cond)
                #for i in instances:
                    #finalInstances.append([And(*[Implies(currIfConstraints[j], i[j][0]) for j in range(len(i))])])
                #cond = mAnd(cond, Implies(currIfConstraint, mAnd(*[i for i in instances])))
            else:
                print("lone, no, and one still unimplemented")
                sys.exit()
        self.stack.append([BoolArg([And(*condList)])])
           
    def extend(self, args):
        maxInstances = 0
        extendedArgs = []
        for i in args:
            maxInstances = max(maxInstances, len(i))
        for i in args:
            if len(i) != maxInstances:
                extendedArgs.append([i[0].clone() for _ in range(maxInstances)])
            else:
                extendedArgs.append(i)
        return (maxInstances, extendedArgs)
                
    def addOperator(self, operation):
        (arity, operator) = getOperationConversion(operation)
        args = []
        for _ in range(0,arity):
            args.insert(0, self.stack.pop())
        (maxInstances, extendedArgs) = self.extend(args)
        finalExprs = []
        for i in range(maxInstances):
            tempExprs = []
            for j in extendedArgs:
                tempExprs.append(j[i])
            finalExprs.append(tempExprs)
        finalExprs = [operator(*finalExprs[i]) for i in range(len(finalExprs))]
        self.stack.append(finalExprs)
    
    def endProcessing(self):
        self.value = self.stack.pop()
        expr = self.value
        if(self.claferStack):
            thisClafer = self.claferStack[-1]
            for i in range(thisClafer.numInstances):
                if thisClafer.numInstances == len(expr):
                    self.addConstraint(Implies(thisClafer.instances[i] != thisClafer.parentInstances, expr[i].finish()))
                #hack for now
                else:
                    self.addConstraint(Implies(thisClafer.instances[i] != thisClafer.parentInstances, expr[0].finish()))
        else:
            for i in expr:
                for j in i.instanceSorts:
                    (_, mask) = j
                    self.addConstraint(mask.pop_value())
        self.z3.z3_bracketed_constraints.append(self)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
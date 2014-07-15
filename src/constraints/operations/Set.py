'''
Created on Nov 1, 2013

@author: ezulkosk
'''
from common import Common, SMTLib
from common.Common import mAnd

from structures.ClaferSort import BoolSort, IntSort, StringSort, RealSort
from structures.ExprArg import Mask, ExprArg, IntArg, BoolArg 
    
def getClaferMatch(key, my_list):
    '''
    Returns the entries in my_list that correspond to either sub or super sorts of key,
    specifically a list of tuples [(bool, int, (sort, Mask))],
    where bool is True iff the key is the subsort,
    int is the index of the subsort in the supersort (0 if the same sort),
    (sort,Mask) are the actual entries from my_list.
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
    
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    #numeric equality case
    if isinstance(left_sort, IntSort) or isinstance(right_sort, IntSort) or isinstance(left_sort, RealSort) or isinstance(right_sort, RealSort):
        return BoolArg([SMTLib.SMT_EQ(SMTLib.SMT_Sum(*[left_mask.values() for (_, left_mask) in left.getInstanceSorts()]),
                         SMTLib.SMT_Sum(*[right_mask.values() for (_, right_mask) in right.getInstanceSorts()]))])
    #string equality case
    elif isinstance(left_sort, StringSort) or isinstance(right_sort, StringSort):
        return BoolArg([SMTLib.SMT_EQ(left_mask.get(0), right_mask.get(0))])
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
                        cond.append(SMTLib.SMT_And(SMTLib.SMT_Implies(sub_sort.isOn(sub_mask.get(k)),
                                            super_sort.isOn(super_mask.get(k + transform))),
                                        SMTLib.SMT_Implies(super_sort.isOn(super_mask.get(k + transform)),
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
            mask.put(j, SMTLib.SMT_Not(mask.get(j)))
    return expr
    




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
        return BoolArg([SMTLib.SMT_Implies(left_mask.pop_value(), right_mask.pop_value())])
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
                        cond.append(SMTLib.SMT_Implies(sub_sort.isOn(sub_mask.get(k)),
                                            super_sort.isOn(super_mask.get(k + transform))))
                    else:
                        cond.append(SMTLib.SMT_Implies(super_sort.isOn(super_mask.get(k + transform)),
                                            sub_sort.isOn(sub_mask.get(k))))
        #unmatched extension
        for i in unmatchedL:
            (sort, mask) = i
            for j in mask.keys():
                cond.append(sort.isOff(mask.get(j)))
        return BoolArg([mAnd(*cond)])
    


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
                instances.append(SMTLib.SMT_If(sort.isOn(j), SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
    return IntArg([SMTLib.SMT_Sum(instances)])

def int_set_union(leftIntSort, rightIntSort):
    (_,(left_sort, left_mask)) = leftIntSort
    (_,(right_sort, right_mask)) = rightIntSort
    newMask = Mask()
    sort = IntSort()
    for i in left_mask.keys():
        cardMask_constraint = SMTLib.SMT_EQ(left_sort.cardinalityMask.get(i), SMTLib.SMT_IntConst(1))
        if newMask.size() != 0:
            noPrevious_constraint = SMTLib.SMT_And(*[SMTLib.SMT_Or(SMTLib.SMT_EQ(sort.cardinalityMask.get(j), SMTLib.SMT_IntConst(0)),
                                                                   SMTLib.SMT_NE(newMask.get(j), left_mask.get(i))) for j in newMask.keys()])
        else:
            noPrevious_constraint = SMTLib.SMT_BoolConst(True)
        full_constraint = SMTLib.SMT_And(noPrevious_constraint, cardMask_constraint)
        
        sort.cardinalityMask.put(i, SMTLib.SMT_If(full_constraint, SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
        newMask.put(i, SMTLib.SMT_If(full_constraint, left_mask.get(i), SMTLib.SMT_IntConst(0)))
    delta = left_mask.size()
    for i in right_mask.keys():
        cardMask_constraint = SMTLib.SMT_EQ(right_sort.cardinalityMask.get(i), SMTLib.SMT_IntConst(1))
        if newMask.size() != 0:
            noPrevious_constraint = SMTLib.SMT_And(*[SMTLib.SMT_Or(SMTLib.SMT_EQ(sort.cardinalityMask.get(j), SMTLib.SMT_IntConst(0)),
                                                                   SMTLib.SMT_NE(newMask.get(j), right_mask.get(i))) for j in newMask.keys()])
        else:
            noPrevious_constraint = SMTLib.SMT_BoolConst(True)
        full_constraint = SMTLib.SMT_And(noPrevious_constraint, cardMask_constraint)
        
        
        
        #constraint = SMTLib.SMT_And(SMTLib.SMT_EQ(right_sort.cardinalityMask.get(i), SMTLib.SMT_IntConst(1)),
        #                 *[SMTLib.SMT_Or(SMTLib.SMT_NE(left_mask.get(j), right_mask.get(i)),
        #                                 SMTLib.SMT_EQ(left_sort.cardinalityMask.get(j), SMTLib.SMT_IntConst(0))) for j in left_mask.keys()])
        sort.cardinalityMask.put(i + delta, SMTLib.SMT_If(full_constraint, SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
        newMask.put(i+delta, SMTLib.SMT_If(full_constraint, right_mask.get(i), SMTLib.SMT_IntConst(0)))
    return (sort, newMask)

    

def putIfNotMatched(sort, mask, index, value, matches):
    '''
    Used to make sure you don't add duplicate elements to a set i.e. a sub and super.
    Needed by union, intersection, and difference.
    '''
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
            mask.put(index, SMTLib.SMT_If(mAnd(*cond), value, SMTLib.SMT_IntConst(sort.parentInstances)))
           
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
                putIfNotMatched(sort, newMask, i, Common.min2(l.get(i), r.get(i)), matches)
            newInstanceSorts.append((sort, newMask))
    return ExprArg(newInstanceSorts)
                

def int_set_intersection(left_sort, left_mask, right_sort, right_mask):
    newMask = Mask()
    sort = IntSort()
    for i in left_mask.keys():
        cardMask_constraint = SMTLib.SMT_EQ(left_sort.cardinalityMask.get(i), SMTLib.SMT_IntConst(1))
        onRight_constraint = SMTLib.SMT_Or(*[SMTLib.SMT_And(SMTLib.SMT_EQ(left_mask.get(i), right_mask.get(j)),
                                         SMTLib.SMT_EQ(right_sort.cardinalityMask.get(j), SMTLib.SMT_IntConst(1))) for j in right_mask.keys()])
        if newMask.size() != 0:
            noPrevious_constraint = SMTLib.SMT_And(*[SMTLib.SMT_Or(SMTLib.SMT_EQ(sort.cardinalityMask.get(j), SMTLib.SMT_IntConst(0)),
                                                                   SMTLib.SMT_NE(newMask.get(j), left_mask.get(i))) for j in newMask.keys()])
        else:
            noPrevious_constraint = SMTLib.SMT_BoolConst(True)
        full_constraint = SMTLib.SMT_And(noPrevious_constraint, cardMask_constraint, onRight_constraint)
        sort.cardinalityMask.put(i, SMTLib.SMT_If(full_constraint, SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
        newMask.put(i, SMTLib.SMT_If(full_constraint, left_mask.get(i), SMTLib.SMT_IntConst(0)))
    return (sort, newMask)              

def op_intersection(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set intersection (left & right)
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])

    #for all instances in left:
    #  if there is a match in right:
    #    add it if not already matched
    newInstanceSorts = []
    for (left_sort, left_mask) in sortedL:
        newMask = Mask()
        right_matches = getClaferMatch(left_sort, sortedR)
        added_matches = getClaferMatch(left_sort, newInstanceSorts)
        if not right_matches:
            continue
        if isinstance(left_sort, IntSort):
            (_,_,(right_sort, right_mask)) = right_matches[0]
            (left_sort, newMask) = int_set_intersection(left_sort, left_mask, right_sort, right_mask)
        else:
            for left_key in left_mask.keys():
                key_matches = []
                for (leftIsSub, transform, (match_sort,match_mask)) in right_matches:
                    right_val = match_mask.get(left_key + transform)
                    if right_val:
                        key_matches.append(match_sort.isOn(right_val))
                #if the left key is on, and ANY of it's matches are on, then include it
                if key_matches:
                    putIfNotMatched(left_sort, newMask, left_key,
                                    SMTLib.SMT_If(SMTLib.SMT_And(left_sort.isOn(left_mask.get(left_key)), SMTLib.SMT_Or(*key_matches)),
                                                  left_mask.get(left_key),
                                                  SMTLib.SMT_IntConst(left_sort.parentInstances)),
                                    added_matches + [(True,0,(left_sort,newMask))])
        newInstanceSorts.append((left_sort,newMask))
    return ExprArg(newInstanceSorts)

def int_set_difference(leftIntSort, rightIntSort):
    (_,(left_sort, left_mask)) = leftIntSort
    (_,(right_sort, right_mask)) = rightIntSort
    
    newMask = Mask()
    sort = IntSort()
    for i in left_mask.keys():
        constraint = SMTLib.SMT_And(SMTLib.SMT_EQ(left_sort.cardinalityMask.get(i), SMTLib.SMT_IntConst(1)),
                         *[SMTLib.SMT_Or(SMTLib.SMT_NE(left_mask.get(i), right_mask.get(j)),
                                         SMTLib.SMT_EQ(right_sort.cardinalityMask.get(j), SMTLib.SMT_IntConst(0))) for j in right_mask.keys()])
        sort.cardinalityMask.put(i, SMTLib.SMT_If(constraint, SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
        newMask.put(i, SMTLib.SMT_If(constraint, left_mask.get(i), SMTLib.SMT_IntConst(0)))
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
                    putIfNotMatched(sort, newMask, i, SMTLib.SMT_If(sort.isOn(r.get(i))
                                         , l.get(i)
                                         , SMTLib.SMT_IntConst(sort.parentInstances)), matches)
            newInstanceSorts.append((sort, newMask))
    return ExprArg(newInstanceSorts)
    

'''
CHECKED UNDER HERE********************************************************************************************
'''         

def int_set_in(leftIntSort, rightIntSort):
    (left_sort, left_mask) = leftIntSort
    (right_sort, right_mask) = rightIntSort
    cond = []
    for i in left_mask.keys():
        constraint = SMTLib.SMT_Or(SMTLib.SMT_EQ(left_sort.cardinalityMask.get(i), SMTLib.SMT_IntConst(0)),
                        SMTLib.SMT_Or(*[SMTLib.SMT_And(SMTLib.SMT_EQ(right_sort.cardinalityMask.get(j), SMTLib.SMT_IntConst(1)),
                                 SMTLib.SMT_EQ(right_mask.get(j), left_mask.get(i))) for j in right_mask.keys()]))
        cond.append(constraint)
    return(SMTLib.SMT_And(*cond))


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
    return BoolArg([SMTLib.SMT_Not(expr.pop_value())])

def op_domain_restriction(l,r):
    pass

def op_range_restriction(l,r):
    pass

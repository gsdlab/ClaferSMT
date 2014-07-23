'''
Created on Nov 1, 2013

@author: ezulkosk
'''
from common import Common, SMTLib
from common.Common import mAnd, mOr
from structures.ExprArg import ExprArg, IntArg, BoolArg, JoinArg
import sys


def getClaferMatch(key, my_list):
    '''
    TODO REMOVE
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
    #TODO REMOVE
    for i in l:
        (sort, mask) =  i
        if sort == key:
            return mask

def addMatchValues(matches, instances, left=True):
    '''
    Ignores PrimitiveSorts
    '''
    for (sort, index) in instances.keys():
        (expr,polarity) = instances[(sort,index)]
        #!!!
        default = (SMTLib.SMT_BoolConst(False), Common.DEFINITELY_OFF)
        (prev_left, prev_right) = matches.get((sort,index), (default,default))
        if left:
            (prev_expr, prev_pol) = prev_left
            new_left = (mOr(expr, prev_expr), Common.aggregate_polarity(polarity, prev_pol))
            new_right = prev_right
        else:
            (prev_expr, prev_pol) = prev_right
            new_left = prev_left
            new_right = (mOr(expr, prev_expr), Common.aggregate_polarity(polarity, prev_pol))
        matches[(sort,index)] = (new_left,new_right)

    return matches

def getSetInstancePairs(left,right=None):
    #key -- (sort, index), where sort must be a highest sort
    #value -- ([isOnExpr], [isOnExpr]), where the left and right come from leftInstanceSort or rightInstanceSort, respectively
    matches = {}
    matches = addMatchValues(matches, left.getInstances(), left=True)
    if right:
        matches = addMatchValues(matches, right.getInstances(), left=False)
    return matches

def compute_int_set(instances):
    cons = []
    for index in range(len(instances)):
        (i,c) = instances[index]
        cons.append(mAnd(c, *[mOr(SMTLib.createNot(jc), SMTLib.SMT_NE(j,i)) for (j, jc) in instances[0:index]]))
    return cons 
   
def op_eq(left,right, cacheJoins=False, bc = None):
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
    if cacheJoins and bc:
        #TODO CLEAN
        left_key = None
        right_key = None
        keys = []
        #asil allocation speedup, if both sides are sets, we can perform expression substitution in other constraints
        #bc is the bracketed constraint to put the cache
        
        for i in [left,right]:
            if isinstance(i, JoinArg):
                newkeys = Common.computeCacheKeys(i.flattenJoin())
                
                #print(tuple(key))
                keys = keys + newkeys
                #need to return all keys during the progress of join, add flag?
                #get the all keys
                all_keys = i.checkIfJoinIsComputed(nonsupered=True, getAllKeys = True)
                #print(keys)
                #print(all_keys)
                keys = keys+all_keys
                #sys.exit()
                #print()
            #print("GGGG right" + str(right.__class__))
            #print(right.clafers)
        if len(left.clafers) != len(right.clafers):
            minJoinVal = left.clafers if len(left.clafers) < len(right.clafers) else right.clafers
            for i in keys:
                #TODO make more robust (e.g. if multiple equalities exist for the same join key, aggregate expressions
                bc.cache[i] = ExprArg(minJoinVal)
                #print(i)
                #print(minJoinVal)
                #print(str(len(minJoinVal)) + "  " + str(len(left.clafers)) + "  " + str(len(right.clafers)))
        #print(str(len(left.clafers)) + " " + str(len(right.clafers)))
    
    cond = []
    #int equality case
    lints = [(e,c) for (e,c) in left.getInts() if str(c) != "False"]
    rints = [(e,c) for (e,c) in right.getInts() if str(c) != "False"]
    if lints or rints:
        for (e,c) in lints:
            #exists r in R s.t. e == r
            expr = mOr(*[mAnd(rc, SMTLib.SMT_EQ(e,r)) for (r,rc) in rints]) 
            if str(c) != "True":
                expr = SMTLib.SMT_Implies(c, expr)
            cond.append(expr)        
        for (e,c) in rints:
            #exists l in L s.t. e == l
            expr = mOr(*[mAnd(lc, SMTLib.SMT_EQ(e,l)) for (l,lc) in lints]) 
            if str(c) != "True":
                expr = SMTLib.SMT_Implies(c, expr)
            cond.append(expr)    
    #clafer-set equality case
    matches = getSetInstancePairs(left,right)
    for ((lexpr, lpol),(rexpr, rpol)) in matches.values():
        if lpol == Common.DEFINITELY_OFF and rpol == Common.DEFINITELY_OFF:
            continue
        elif lpol == Common.DEFINITELY_OFF:
            cond.append(SMTLib.createNot(rexpr))
        elif rpol == Common.DEFINITELY_OFF:
            cond.append(SMTLib.createNot(lexpr))
        else:
            cond.append(SMTLib.SMT_Implies(lexpr, rexpr))
            cond.append(SMTLib.SMT_Implies(rexpr, lexpr))
    return BoolArg(mAnd(*cond))
            
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
    b = expr.getBool()
    return BoolArg(SMTLib.createNot(b))
    
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
    #clafer-set equality case
    if left.getInts():
        sys.exit("FIXME Implies")
    if isinstance(left, BoolArg) and isinstance(right, BoolArg):
        return BoolArg(SMTLib.SMT_Implies(left.getBool(), right.getBool()))
    cond = []
    matches = getSetInstancePairs(left,right)
    for ((lexpr, lpol),(rexpr, rpol)) in matches.values():
        if lpol == Common.DEFINITELY_OFF or rpol == Common.DEFINITELY_ON:
            continue
        elif lpol == Common.DEFINITELY_ON:
            cond.append(rexpr)
        else:
            #lpol is unknown and rpol is off or unknown
            #almost the same as op_difference below
            cond.append(SMTLib.SMT_Implies(lexpr, rexpr))
    return BoolArg(mAnd(*cond))

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
    matches = getSetInstancePairs(arg)
    known_card = 0
    if arg.getInts():
        card_cons = compute_int_set(arg.getInts())
        for i in card_cons:
            if isinstance(i, SMTLib.SMT_BoolConst):
                if i.value:
                    known_card = known_card + 1
            else:
                instances.append(SMTLib.SMT_If(i, SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
    for (instance,_) in matches.values():
        (expr, polarity) = instance
        if polarity == Common.DEFINITELY_ON:
            known_card = known_card + 1
        else:
            instances.append(SMTLib.SMT_If(expr, SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
    instances.append(SMTLib.SMT_IntConst(known_card))
    return IntArg(SMTLib.createSum(instances))
    
def int_set_union(leftIntSort, rightIntSort):
    sys.exit("TODO")
    '''
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
    '''
    

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
    if left.getInts() or right.getInts():
        sys.exit("FIXME ints union")
    matches = getSetInstancePairs(left,right)
    newInstances = {}
    for (sort,index) in matches.keys():
        key = (sort,index)
        ((lexpr,lpol),(rexpr,rpol)) = matches[(sort,index)]
        if rpol == Common.DEFINITELY_OFF and lpol == Common.DEFINITELY_OFF:
            continue
        else:
            new_expr = mOr(lexpr,rexpr)
            newInstances[key] = (new_expr, Common.aggregate_polarity(lpol, rpol))
    return ExprArg(newInstances)

def int_set_intersection(left_sort, left_mask, right_sort, right_mask):
    sys.exit("TODO")
    '''
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
    '''          

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
    if left.getInts() or right.getInts():
        sys.exit("FIXME ints intersection")
    matches = getSetInstancePairs(left,right)
    newInstances = {}
    for (sort,index) in matches.keys():
        key = (sort,index)
        ((lexpr,lpol),(rexpr,rpol)) = matches[(sort,index)]
        if rpol == Common.DEFINITELY_OFF or lpol == Common.DEFINITELY_OFF:
            continue
        else:
            new_expr = mAnd(lexpr,rexpr)
            newInstances[key] = (new_expr, Common.aggregate_polarity(lpol, rpol))
    return ExprArg(newInstances)
   

def int_set_difference(leftIntSort, rightIntSort):
    sys.exit("TODO")
    '''
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
    if left.getInts() or right.getInts():
        sys.exit("FIXME ints diff")
    matches = getSetInstancePairs(left,right)
    newInstances = {}
    for (sort,index) in matches.keys():
        key = (sort,index)
        ((lexpr,lpol),(rexpr,rpol)) = matches[(sort,index)]
        if rpol == Common.DEFINITELY_ON or lpol == Common.DEFINITELY_OFF:
            #cases (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)
            continue
        elif rpol == Common.DEFINITELY_OFF:
            #cases (0 , -1), (1, -1)
            newInstances[key] = (lexpr, lpol)
        else:
            #rpol is unknown, lpol is unknown or on => new_pol is UNKNOWN
            #cases (0, 0), (1, 0)
            #if right is not on, then left, else sort.isOff
            new_expr = SMTLib.SMT_If(SMTLib.createNot(rexpr), lexpr, sort.parentInstances)
            newInstances[key] = (new_expr, Common.UNKNOWN)
    return ExprArg(newInstances)

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
    return BoolArg(SMTLib.createNot(expr.pop_value()))

def op_domain_restriction(l,r):
    sys.exit("Domain Restriction")

def op_range_restriction(l,r):
    sys.exit("Range Restriction")

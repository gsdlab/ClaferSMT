'''
Created on Jul 14, 2014

@author: ezulkosk
'''
from common import SMTLib, Assertions, Options, Common
from common.Common import mOr, mAnd
from structures.ClaferSort import IntSort, StringSort, RealSort, PrimitiveType, \
    ClaferSort
from structures.ExprArg import ExprArg, JoinArg, PrimitiveArg
import sys

def joinWithSuper(sort, index):
    '''
    :param sort:
    :type sort: :class:`~common.ClaferSort`
    :returns: (:class:`~common.ClaferSort`, [Int()]) 
    
    Maps each instance of the subclafer **sort** to the corresponding super instance. Returns the super sort and its instances.
    '''
    return (sort.superSort, sort.indexInSuper + index)


def joinWithParent(arg):
    instances = arg.getInstances(nonsupered=True)
    newInstances = {}
    for (sort, index) in instances.keys():
        (expr, pol) = instances[(sort,index)]
        if pol == Common.DEFINITELY_OFF:
            continue
        (lower,upper,_) = sort.instanceRanges[index]
        for i in range(lower, min(sort.parentInstances,upper+1)):
            (old_expr, old_pol) = newInstances.get((sort.parent,i), (SMTLib.SMT_BoolConst(False), Common.DEFINITELY_OFF))
            if pol == Common.DEFINITELY_ON and lower == upper:
                new_pol = Common.DEFINITELY_ON
                new_expr = SMTLib.SMT_BoolConst(True)
            else:
                new_pol = Common.aggregate_polarity(old_pol, Common.UNKNOWN)
                new_expr = mOr(old_expr, mAnd(expr, SMTLib.SMT_EQ(sort.instances[index], SMTLib.SMT_IntConst(i))))
            newInstances[(sort.parent, i)] = (new_expr, new_pol)
    return ExprArg(newInstances)

def joinWithPrimitive(newArg, sort, index, expr, pol):
    ref = sort.refs[index]
    if sort.refSort == "integer":
        #do not need to check if already in set.
        #if bag, no need. if set, pairwise uniqueness will be added eventually
        if pol == Common.DEFINITELY_ON:
            newArg.ints.append((ref, True))
        elif pol == Common.UNKNOWN:
            newArg.ints.append((ref, expr))
    else:
        sys.exit("TODO string real")
    
'''
ASSUME SIMPLE JOINS
'''
def joinWithClaferRef(arg):
    instances = arg.getInstances(nonsupered=True)
    newArg = ExprArg(nonsupered=True)
    
    for (sort, index) in instances.keys():
        (expr, pol) = instances[(sort,index)]
        while not sort.refSort:
            (sort, index) = joinWithSuper(sort, index)
        if isinstance(sort.refSort, PrimitiveType):
            joinWithPrimitive(newArg,sort,index,expr,pol)
        for i in range(sort.refSort.numInstances):
            (prev_expr, _) = newArg.getInstances(nonsupered=True).get((sort.refSort,i), (SMTLib.SMT_BoolConst(False), Common.DEFINITELY_OFF))
            newArg.getInstances(nonsupered=True)[(sort.refSort,i)] = (mOr(prev_expr, mAnd(expr, 
                                                            SMTLib.SMT_EQ(sort.refs[index], SMTLib.SMT_IntConst(i))
                                                            )), Common.UNKNOWN)
        #newArg[(sort,index)] = (expr, pol)
    return newArg
    '''
    newInstanceSorts = []
    for i in arg.getInstanceSorts():
        (sort, mask) = i
        while not sort.refSort:
            (sort, mask) = joinWithSuper(sort, mask)
        tempRefs = []
        newMask = alreadyExists(sort.refSort, newInstanceSorts)
        if isinstance(sort.refSort, PrimitiveType):
            return joinWithPrimitive(ExprArg([(sort, mask)],nonsupered=True))
        for j in mask.keys():
            tempRefs.append(SMTLib.SMT_If(sort.isOn(mask.get(j)),
                               sort.refs[j], SMTLib.SMT_IntConst(sort.refSort.numInstances)))
        for j in range(sort.refSort.numInstances):
            clause = mOr(*[SMTLib.SMT_EQ(k, SMTLib.SMT_IntConst(j)) for k in tempRefs])
            newMask.put(j, mOr(newMask.get(j), clause))
        newInstanceSorts.append((sort.refSort, newMask))
        Assertions.nonEmptyMask(newMask)
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, SMTLib.SMT_If(mask.get(j), sort.instances[j], SMTLib.SMT_IntConst(sort.parentInstances)))
    return ExprArg(newInstanceSorts, nonsupered=True)
    '''
def joinWithRef(arg): 
    instances = arg.getInstances(nonsupered=True)
    newArg = ExprArg(nonsupered=True)
    
    for (sort,index) in instances:
        (expr, pol) = instances[(sort,index)]
        if pol == Common.DEFINITELY_OFF:
            continue
        else:
            if isinstance(sort.refSort, PrimitiveType):
                joinWithPrimitive(newArg,sort,index,expr,pol)
            else: 
                #join on ref sort
                #needs to be more robust for multiple instanceSorts
                return joinWithClaferRef(arg)
    return newArg


def flattenInstances(instances):
    '''
    sets the new polarities to corresponding ternary values
    '''
    #print(instances)
    for (sort, index) in instances.keys():
        final_expr = mOr(SMTLib.SMT_BoolConst(False))
        (l,h,e) = sort.instanceRanges[index]
        (exprs, pols) = instances[(sort,index)]
        final_polarity = Common.DEFINITELY_OFF
        all_on = True
        for i in range(l, h+1):
            currExpr = exprs.get(i)
            currPol = pols.get(i)
            if not(i in pols.keys()) or currPol == Common.DEFINITELY_OFF:
                all_on = False
                continue
            elif currPol == Common.UNKNOWN:
                all_on = False
                final_polarity = Common.UNKNOWN
                final_expr = mOr(final_expr, currExpr)
            else:
                final_polarity = Common.UNKNOWN
                final_expr = mOr(final_expr, currExpr)
        if all_on:
            final_polarity = Common.DEFINITELY_ON
            final_expr = SMTLib.SMT_BoolConst(True)
        instances[(sort,index)] = (final_expr, final_polarity)       
    #print(instances)
    return instances


def joinWithClafer(left, right):
    newInstances = {}
    leftInstances = left.getInstances(nonsupered=True)
    rightInstances = right.getInstances(nonsupered=True)
    for (lsort, lindex) in leftInstances.keys():
        (lexpr, lpolarity) = leftInstances[(lsort,lindex)]
        if lpolarity == Common.DEFINITELY_OFF:
            continue
        for (rsort, rindex) in rightInstances.keys():
            (rexpr, rpolarity) = rightInstances[(rsort,rindex)]
            if rpolarity == Common.DEFINITELY_OFF:
                continue
            noMatch = False
            while not(rsort in lsort.fields):
                if not lsort.superSort:
                    noMatch = True
                    break
                (lsort, lindex) = joinWithSuper(lsort, lindex)
            if noMatch:
                continue
            (lower,upper,rextra) = rsort.instanceRanges[rindex]
            
            (new_rexpr, new_rpol) = newInstances.get((rsort,rindex), ({},{}))
            new_rpol[lindex] = lpolarity
            new_rexpr[lindex] = mAnd(lexpr, SMTLib.SMT_EQ(rsort.instances[rindex], SMTLib.SMT_IntConst(lindex)))
            if lower <= lindex and lindex <= upper:
                newInstances[(rsort, rindex)] = (new_rexpr, new_rpol)
    newInstances = flattenInstances(newInstances)
    #print(newInstances)
    #sys.exit("join exit")
    return ExprArg(newInstances, nonsupered=True)
    
def computeJoin(joinList):
    left = joinList.pop(0) 
    while joinList:
        right = joinList.pop(0)
        if isinstance(right, PrimitiveArg):
            if right.getValue() == "parent":
                left = joinWithParent(left)
            elif right.getValue() == "ref":
                left = joinWithRef(left)
        else:
            left = joinWithClafer(left, right)
    return left

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

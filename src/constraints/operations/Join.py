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
        newMask.put(i + sort.indexInSuper,
                    SMTLib.SMT_If(sort.isOn(mask.get(i)), 
                       sort.superSort.instances[i + sort.indexInSuper], 
                       SMTLib.SMT_IntConst(sort.superSort.parentInstances)))
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
                newMask.put(k, mOr(prevClause, SMTLib.SMT_EQ(mask.get(j), SMTLib.SMT_IntConst(k))))
        newInstanceSorts.append((sort.parent, newMask))
        Assertions.nonEmptyMask(newMask)
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, SMTLib.SMT_If(mask.get(j), sort.instances[j], SMTLib.SMT_IntConst(sort.parentInstances)))
    return ExprArg(newInstanceSorts, nonsupered=True)


def addPrimitive(newSort, newMask, oldSort, oldMask, index, wasEmpty=False):
    newIndex = newSort.getNextIndex()
    cardinalityMask = newSort.getCardinalityMask()
    if wasEmpty:
        constraint = oldSort.isOn(oldMask.get(index))
    else:
        #TODO: only add this constraint if it is NOT the first set being added (needs to be modified to not look in the same set) (bag fix)
        constraint = SMTLib.SMT_And(oldSort.isOn(oldMask.get(index)), mAnd(*[SMTLib.SMT_NE(oldSort.refs[index], i) for i in newMask.values()]))
    cardinalityMask.put(newIndex, SMTLib.SMT_If(constraint, SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
    newMask.put(newIndex, SMTLib.SMT_If(constraint, oldSort.refs[index], SMTLib.SMT_IntConst(0)))


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
    return ExprArg(newInstanceSorts, nonsupered=True)
    
    
'''
CLEAN : THERE IS PRIMITIVES STUFF IN HERE
'''
def joinWithClaferRef(arg):
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
    
def joinWithRef(arg): 
    (sort, _) = arg.instanceSorts[0]
    if len(arg.instanceSorts) > 1:
        #TODO: allow joins with multiple RHS 
        sys.exit("bug in join with ref, need to implement...")
    if isinstance(sort.refSort, PrimitiveType):
        return joinWithPrimitive(arg)
    else: 
        #join on ref sort
        #needs to be more robust for multiple instanceSorts
        return joinWithClaferRef(arg)


def flattenInstances(instances):
    '''
    sets the new polarities to corresponding ternary values
    '''
    #print(instances)
    for (sort, index) in instances.keys():
        final_expr = mOr(SMTLib.SMT_BoolConst(True))
        (l,h,e) = sort.instanceRanges[index]
        (exprs, pols) = instances[(sort,index)]
        final_polarity = Common.DEFINITELY_OFF
        all_on = True
        for i in range(l, h+1):
            currExpr = exprs.get(i)
            currPol = pols.get(i)
            if not currPol:
                all_on = False
                continue
            elif currPol == Common.UNKNOWN:
                all_on = False
                final_polarity = Common.UNKNOWN
                final_expr = mOr(final_expr, currExpr)
            else:
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
                sys.exit("TODO joinsuper")
                if not lsort.superSort:
                    noMatch = True
                    break
                (lsort, lpolarity) = joinWithSuper(lsort, lpolarity)
            if noMatch:
                continue
            (lower,upper,rextra) = rsort.instanceRanges[rindex]
            try:
                rpolarity[lindex] = lpolarity
                rexpr[lindex] = mAnd(lexpr, SMTLib.SMT_EQ(rsort.instances[rindex], SMTLib.SMT_IntConst(lindex)))
            except:
                rpolarity = {} # TODO this shit right here
                rexpr = {}
                rpolarity[lindex] = lpolarity
                rexpr[lindex] = mAnd(lexpr, SMTLib.SMT_EQ(rsort.instances[rindex], SMTLib.SMT_IntConst(lindex)))
            if lower <= lindex and lindex <= upper:
                newInstances[(rsort, rindex)] = (rexpr, rpolarity)
    newInstances = flattenInstances(newInstances)
    #print(newInstances)
    #sys.exit("join exit")
    return ExprArg(newInstances, nonsupered=True)
    
    '''
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
                        newMask.put(i, mOr(prevClause, SMTLib.SMT_And(left_sort.isOn(left_mask.get(j)), 
                                                    SMTLib.SMT_EQ(right_sort.instances[i], SMTLib.SMT_IntConst(j)))))
            #CAREFUL!!!
            if newMask.size() == 0:
                #print(left)
                #print(right)
                continue
            newInstanceSorts.append((right_sort, newMask))
            Assertions.nonEmptyMask(newMask)
    for i in newInstanceSorts:
        (sort, mask) = i
        for j in mask.keys():
            mask.put(j, SMTLib.SMT_If(mask.get(j), sort.instances[j], SMTLib.SMT_IntConst(sort.parentInstances)))
    return ExprArg(newInstanceSorts)
    '''

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
    return left.getInstances()

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

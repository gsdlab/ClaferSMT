'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Common
from constraints import Constraints
from constraints.Constraints import GenericConstraints
from lxml.builder import basestring
from z3 import Function, IntSort, BoolSort, If, Not, Sum, Implies, Or, And, Xor
import sys


class ExprArg():
    def __init__(self, joinSorts, instanceSorts, instances):
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
        self.instances = instances
        
    def modifyInstances(self, newInstances):
        '''
        :param newInstances:
        :type newInstances: [Int()]
        :returns: :class:`~ExprArg`
        
        Returns the old ExprArg, with its instances changed to **newInstances**.
        '''
        return ExprArg(self.joinSorts[:], self.instanceSorts[:], newInstances)
      
    def __str__(self):
        return (str(self.instances)) 
     
    def __repr__(self):
        return (str(self.instances)) 
               
class IntArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds an integer instance.
        '''
        self.joinSorts = ["int"]
        self.instanceSorts = ["int"]
        self.instances = instances
        
class BoolArg(ExprArg):
    def __init__(self, instances):
        '''
        Convenience class that extends ExprArg and holds a boolean instance.
        '''
        self.joinSorts = ["bool"]
        self.instanceSorts = ["bool"]
        self.instances = instances

def joinWithSuper(sort, instances):
    '''
    :param sort:
    :type sort: :class:`~common.ClaferSort`
    :param instances:
    :type instances: [Int()]
    :returns: (:class:`~common.ClaferSort`, [Int()]) 
    
    Maps each instance of the subclafer **sort** to the corresponding super instance. Returns the super sort and its instances.
    '''
    newInstances = []
    for i in range(0, sort.indexInSuper):
        newInstances.append(sort.superSort.parentInstances)
    for i in range(len(instances)):
        newInstances.append(If(instances[i] != sort.parentInstances, sort.superSort.instances[i + sort.indexInSuper], sort.superSort.parentInstances))
    for i in range(len(instances), sort.superSort.numInstances):
        newInstances.append(sort.superSort.parentInstances)
    return(sort.superSort, newInstances)

def createJoinFunction(leftSort, rightSort, linstances, rinstances, zeroedVal):
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
    joinFunction = Function("join" + str(Common.getFunctionUID()) + ":" + str(leftSort) , IntSort(), IntSort())
    joinHelperFunction = Function("joinhelper" + str(Common.getFunctionUID()) + ":" + str(leftSort) , IntSort(), IntSort())
    constraints = []
    for i in range( len(linstances)):
        constraints.append(joinHelperFunction(i) == linstances[i])
    constraints.append(joinHelperFunction(len(linstances)) == leftSort.parentInstances)
    for i in range(len(rinstances)):  #rinstance[i] in joinHelperFunction arg
        constraints.append(joinFunction(i) == If(joinHelperFunction(rightSort.instances[i]) != leftSort.parentInstances, rinstances[i], zeroedVal))
    constraints.append(joinFunction(len(rinstances)) == zeroedVal)
    leftSort.z3.join_constraints.addAll(constraints)
    return joinFunction

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
            for i in range(leftJoinPoint.parent.numInstances):
                clause = Or(*[j == i for j in left.instances])
                newInstances.append(If(clause, leftJoinPoint.parent.instances[i], leftJoinPoint.parent.parentInstances))
            return(ExprArg(joinSorts, [leftJoinPoint.parent], newInstances))
        elif rightJoinPoint == "ref":
            if isinstance(leftJoinPoint.refSort, basestring):
                if leftJoinPoint.refSort == "integer":
                    return(ExprArg(left.joinSorts + ["int"], 
                                   ["int"], 
                                   [If(left.instances[i] != leftJoinPoint.parentInstances, leftJoinPoint.refs[i], 0)  
                                    for i in range(leftJoinPoint.numInstances)]))      
                else:
                    print("Error on: " + leftJoinPoint.refSort + "string refs other than int (e.g. double) unimplemented")
                    sys.exit()
            else: 
                joinSorts = left.joinSorts + [leftJoinPoint.refSort] +  [right.joinSorts[i] for i in range(1, len(right.joinSorts))]
                for i in range(leftJoinPoint.refSort.numInstances):
                    tempRefs = [If(left.instances[j] != leftJoinPoint.parentInstances, leftJoinPoint.refs[j]
                                   , leftJoinPoint.refSort.parentInstances) for j in range(len(left.instances))]
                    clause = Or(*[j == i for j in tempRefs])
                    newInstances.append(If(clause, leftJoinPoint.refSort.instances[i], leftJoinPoint.refSort.parentInstances))
                return(ExprArg(joinSorts, [leftJoinPoint.refSort], newInstances))
    else:
        leftInstances = left.instances
        while not(rightJoinPoint in leftJoinPoint.fields):
            (leftJoinPoint, leftInstances) = joinWithSuper(leftJoinPoint, leftInstances)
        instanceSorts = right.instanceSorts
        if(isinstance(instanceSorts[0],basestring) and instanceSorts[0] == "int"):
            zeroedVal = 0
        else:
            zeroedVal = instanceSorts[0].parentInstances
        joinFunction = createJoinFunction(leftJoinPoint, rightJoinPoint, leftInstances, right.instances, zeroedVal)
        joinSorts = left.joinSorts + [leftJoinPoint] + right.joinSorts
        for i in range(len(right.instances)):
            newInstances.append(joinFunction(i))
        return(ExprArg(joinSorts, instanceSorts, newInstances))

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
    index = 0
    newInstances = []
    for i in arg.instanceSorts:
        for _ in range(i.numInstances):
            newInstances.append(If(arg.instances[index] != i.parentInstances, 1, 0))
            index = index + 1
    return IntArg([Sum(newInstances)])

def op_add(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left + right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return IntArg([sum(left.instances) + sum(right.instances)])
    #return IntArg(left.instances + right.instances)

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
    return IntArg([sum(left.instances) - sum(right.instances)])

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
    return IntArg([sum(left.instances) * sum(right.instances)])

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
    lsum = sum(left.instances)
    rsum = sum(right.instances)
    return IntArg(lsum / rsum
                   if((not isinstance(lsum, int)) or (not isinstance(rsum, int)))
                             else lsum // rsum)
    
def op_un_minus(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Negates arg.
    '''
    assert isinstance(arg, ExprArg)
    return IntArg([-(sum(arg.instances))])
    

def op_not(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Boolean negation of arg.
    '''
    assert isinstance(arg, ExprArg)
    return BoolArg([Not(arg.instances[0])])
    
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
    
    #integer equality case
    if isinstance(left.instanceSorts[0], basestring) and left.instanceSorts[0] == "int":
        return BoolArg([sum(left.instances) == sum(right.instances)])
    #clafer-set equality case
    else:
        return BoolArg([And(*[i == j for i,j in zip(left.instances, right.instances)])])
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
    expr.instances = [Not(i) for i in expr.instances]
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
    return BoolArg([sum(left.instances) < sum(right.instances)])  
        
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
    return BoolArg([sum(left.instances) <= sum(right.instances)])  

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
    return BoolArg([And(left.instances[0], right.instances[0])])  

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
    return BoolArg([Or(left.instances[0], right.instances[0])]) 

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
    return BoolArg([Xor(left.instances[0], right.instances[0])]) 

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
    return BoolArg([And(*[Implies(i,j) for i,j in zip(left.instances, right.instances)])])

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
    return BoolArg([And(*[And(Implies(i,j), Implies(j,i)) for i,j in zip(left.instances, right.instances)])])
    #return BoolArg(And(Implies(left.instances, right.instances),
    #                   Implies(right.instances, left.instances))) 

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

#XXX
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
            nextSort = left.instanceSorts.pop(0)
            nextJoinSort = left.joinSorts.pop(0)
            for _ in range(nextSort.numInstances):
                finalLinstances.append(left.instances.pop(0))
                finalRinstances.append(nextSort.parentInstances)
        elif (not left.instanceSorts):
            nextSort = right.instanceSorts.pop(0)
            nextJoinSort = right.joinSorts.pop(0)
            for _ in range(nextSort.numInstances):
                finalLinstances.append(nextSort.parentInstances)
                finalRinstances.append(right.instances.pop(0))
        elif left.instanceSorts[0].element.uid < right.instanceSorts[0].element.uid:
            nextSort = left.instanceSorts.pop(0)
            nextJoinSort = left.joinSorts.pop(0)
            for _ in range(nextSort.numInstances):
                finalLinstances.append(left.instances.pop(0))
                finalRinstances.append(nextSort.parentInstances)
        elif left.instanceSorts[0].element.uid > right.instanceSorts[0].element.uid:
            nextSort = right.instanceSorts.pop(0)
            nextJoinSort = right.joinSorts.pop(0)
            for _ in range(nextSort.numInstances):
                finalLinstances.append(nextSort.parentInstances)
                finalRinstances.append(right.instances.pop(0))        
        else:
            nextSort = left.instanceSorts.pop(0)
            nextJoinSort = left.joinSorts.pop(0)
            right.instanceSorts.pop(0)
            right.joinSorts.pop(0)
            for _ in range(nextSort.numInstances):
                finalLinstances.append(left.instances.pop(0))
                finalRinstances.append(right.instances.pop(0))  
        finalSorts.append(nextSort)
        finalJoinSorts.append(nextJoinSort)
    return(ExprArg(finalJoinSorts, finalSorts, finalLinstances), 
           ExprArg(finalJoinSorts, finalSorts, finalRinstances))

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
    (extendedL, extendedR) = set_extend(left,right)
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.min2(extendedL.instances.pop(0), extendedR.instances.pop(0)))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)

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
    (extendedL, extendedR) = set_extend(left,right)
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.max2(extendedL.instances.pop(0), extendedR.instances.pop(0)))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)

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
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            linstance = extendedL.instances.pop(0)
            rinstance = extendedR.instances.pop(0)
            finalInstances.append(If(And(linstance != i.parentInstances, rinstance == i.parentInstances)
                                     , linstance
                                     , i.parentInstances))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)

def op_in(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that left is a subset of right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (extendedL, extendedR) = set_extend(left,right)
    finalExpr = True
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalExpr = And(finalExpr, Implies(extendedL.instances.pop(0) != i.parentInstances, 
                                               extendedR.instances.pop(0) != i.parentInstances))
    return BoolArg([finalExpr])

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
    return expr.modifyInstances(Not(expr.instances))

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
    return IntArg([Sum(arg.instances)])

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
        assert isinstance(expr, ExprArg)
        self.locals[uid] = expr
    
    def addArg(self, arg):
        assert isinstance(arg, ExprArg)
        self.stack.append(arg)
            
    def addQuantifier(self, quantifier, num_args, num_quantifiers, ifconstraints):
        finalInstances = []
        localStack = []
        for _ in range(num_quantifiers):
            for _ in range(num_args):
                localStack.append(self.stack.pop())
        for q in range(num_quantifiers):
            instances = []
            instanceSorts = []
            finalInnerInstances = []
            if ifconstraints:
                currIfConstraints = ifconstraints.pop(0)
            else:
                currIfConstraints = []
            for a in range(num_args):
                currExpr = localStack.pop()
                instanceSorts = instanceSorts + currExpr.instanceSorts
                #essentially a zip
                if not instances:
                    instances = [[i] for i in currExpr.instances]
                else:
                    instances = [instances[i] + [currExpr.instances[i]] for i in range(len(currExpr.instances))]
            if quantifier == "Some":
                for h in instances:
                    firstIndexOfCurrentSort = 0
                    innerExpr = False
                    if instanceSorts and not isinstance(instanceSorts[0], basestring):
                        for i in instanceSorts:
                            for j in range(i.numInstances): 
                                innerExpr = Or(innerExpr, 
                                               Or(*[k != i.parentInstances for k in h[firstIndexOfCurrentSort + j] ]))
                            firstIndexOfCurrentSort = firstIndexOfCurrentSort + i.numInstances
                    else:
                        #refactor me
                        j = 0
                        innerExpr = Or(innerExpr, 
                                               Or(*[k for k in h[firstIndexOfCurrentSort + j] ]))
                    finalInnerInstances.append(innerExpr)
                finalInstances.append([And(*finalInnerInstances)])
            elif quantifier == "All":
                for i in instances:
                    finalInstances.append([And(*[Implies(currIfConstraints[j], i[j][0]) for j in range(len(i))])])
                if not instances:
                    finalInstances = [[True]]
            else:
                print("lone, no, and one still unimplemented")
                sys.exit()
        self.stack.append(BoolArg(finalInstances))
           
    def extend(self, args):
        for i in args:
            assert isinstance(i, ExprArg)
        maxInstances = 0
        extendedArgs = []
        for i in args:
            maxInstances = max(maxInstances, len(i.instances))
        for i in args:
            if len(i.instances) != maxInstances:
                tempInstances = []
                for _ in range(maxInstances):
                    if not isinstance(i.instances[0], int):
                        tempInstances.append(i.instances[0])
                    else:
                        tempInstances.append([i.instances[0]])
                extendedArgs.append(ExprArg(i.joinSorts, i.instanceSorts, tempInstances))
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
                tempExprs.append(j.modifyInstances(j.instances[i]))
            finalExprs.append(tempExprs)
        finalExprs = [operator(*finalExprs[i]) for i in range(len(finalExprs))]
        finalInstances = [i.instances for i in finalExprs]
        self.stack.append(finalExprs[0].modifyInstances(finalInstances))
    
    def endProcessing(self):
        self.value = self.stack.pop()
        expr = self.value
        if(self.claferStack):
            thisClafer = self.claferStack[-1]
            for i in range(thisClafer.numInstances):
                self.addConstraint(Implies(thisClafer.instances[i] != thisClafer.parentInstances, expr.instances[i][0]))
        else:
            for i in expr.instances:
                for j in i:
                    self.addConstraint(j)
        self.z3.z3_bracketed_constraints.append(self)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
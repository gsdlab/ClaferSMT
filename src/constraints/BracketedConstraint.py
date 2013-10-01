'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Common
from lxml.builder import basestring
from z3 import Function, IntSort, BoolSort, If, Not, Sum, Implies, Or, And, Xor
import sys


class ExprArg():
    def __init__(self, joinSorts, instanceSorts, instances):
        self.joinSorts = joinSorts
        self.instanceSorts = instanceSorts
        self.instances = instances
        
    def modifyInstances(self, newInstances):
        return ExprArg(self.joinSorts[:], self.instanceSorts[:], newInstances)
      
    def __str__(self):
        return (str(self.instances)) 
     
    def __repr__(self):
        return (str(self.instances)) 
               
class IntArg(ExprArg):
    def __init__(self, instances):
        self.joinSorts = ["int"]
        self.instanceSorts = ["int"]
        self.instances = instances
        
class BoolArg(ExprArg):
    def __init__(self, instances):
        self.joinSorts = ["bool"]
        self.instanceSorts = ["bool"]
        self.instances = instances

def joinWithSuper(sort, instances):
    newInstances = []
    for i in range(0, sort.indexInSuper):
        newInstances.append(sort.superSort.parentInstances)
    for i in range(len(instances)):
        newInstances.append(If(instances[i] != sort.parentInstances, sort.superSort.instances[i + sort.indexInSuper], sort.superSort.parentInstances))
    for i in range(len(instances), sort.superSort.numInstances):
        newInstances.append(sort.superSort.parentInstances)
    return(sort.superSort, newInstances)

def createJoinFunction(leftSort, rightSort, linstances, rinstances, zeroedVal):
    joinFunction = Function("join" + str(Common.getFunctionUID()) + ":" + str(leftSort) , IntSort(), IntSort())
    joinHelperFunction = Function("joinhelper" + str(Common.getFunctionUID()) + ":" + str(leftSort) , IntSort(), IntSort())
    constraints = []
    for i in range(len(linstances)):
        constraints.append(joinHelperFunction(i) == linstances[i])
    constraints.append(joinHelperFunction(len(linstances)) == leftSort.parentInstances)
    for i in range(len(rinstances)):  
        #clause = Or(*[j == i for j in linstances])  
        constraints.append(joinFunction(i) == If(joinHelperFunction(rightSort.instances[i]) != leftSort.parentInstances, rinstances[i], zeroedVal))
    constraints.append(joinFunction(len(rinstances)) == zeroedVal)
    leftSort.z3.z3_constraints = leftSort.z3.z3_constraints + constraints
    return joinFunction

#can optimize this.parent
#need to range newInstances over ALL sorts in instanceSorts (don't have a test case yet)
#   for example, leftJoinPoint.parentInstances CHANGES if there are multiple sorts here
def op_join(left,right):
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
        #this can be entirely subsumed by the below case
        if(rightJoinPoint in leftJoinPoint.fields):
            joinSorts = left.joinSorts + right.joinSorts
            instanceSorts = right.instanceSorts
            if(isinstance(instanceSorts[0],basestring) and instanceSorts[0] == "int"):
                zeroedVal = 0
            else:
                zeroedVal = instanceSorts[0].parentInstances
            joinFunction = createJoinFunction(leftJoinPoint, rightJoinPoint, left.instances, right.instances, zeroedVal)    
            for i in range(len(right.instances)):
                newInstances.append(joinFunction(i))
            return(ExprArg(joinSorts, instanceSorts, newInstances))
        else:
            #join with super abstract
            #i think this only works for one level of inheritance...just loop it
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
            #for i in range(len(right.instances)):
            #    newInstances.append(If(joinFunction(right.instances[i]), right.instances[i], rightJoinPoint.parentInstances))
            #newInstances = [zeroedVal for i in range(leftJoinPoint.indexInSuper)] \
            #    + [If(left.instances[i] != leftJoinPoint.parentInstances, right.instances[i + leftJoinPoint.indexInSuper], zeroedVal) for i in range(len(left.instances))] \
            #    + [zeroedVal for i in range(leftJoinPoint.indexInSuper + len(leftJoinPoint.instances), len(rightJoinPoint.instances))]
            for i in range(len(right.instances)):
                newInstances.append(joinFunction(i))
            return(ExprArg(joinSorts, instanceSorts, newInstances))
    
    
def op_card(arg):
    assert isinstance(arg, ExprArg)
    index = 0
    newInstances = []
    for i in arg.instanceSorts:
        for _ in range(i.numInstances):
            newInstances.append(Common.bool2Int(arg.instances[index] != i.parentInstances))
            index = index + 1
    return IntArg(Sum(newInstances))

def op_add(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return IntArg(left.instances + right.instances)

def op_sub(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return IntArg(left.instances - right.instances)

def op_mul(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return IntArg(left.instances * right.instances)

#integer division
def op_div(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return IntArg(left.instances / right.instances 
                   if((not isinstance(left.instances, int)) or (not isinstance(right.instances, int)))
                             else left.instances // right.instances)
    
def op_un_minus(arg):
    assert isinstance(arg, ExprArg)
    return IntArg(-(arg.instances))
    
def op_eq(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    if(isinstance(left.instances, list) and isinstance(right.instances, list)):
        #ref case
        if isinstance(left.instanceSorts[0], basestring) and left.instanceSorts[0] == "int":
            return BoolArg(Sum(*left.instances) == Sum(*right.instances))
        else:
            return BoolArg(And(*[i == j for i,j in zip(left.instances, right.instances)]))
    elif(isinstance(left.instances, list)):
        return BoolArg(Sum(*left.instances) == right.instances)
    elif(isinstance(right.instances, list)):
        return BoolArg(Sum(*right.instances) == left.instances)
    else:
        return BoolArg(left.instances == right.instances)  
    
def op_ne(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    expr = op_eq(left, right)
    expr.instances = Not(expr.instances)
    return expr
    
def op_lt(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(left.instances < right.instances)  
        
def op_le(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(left.instances <= right.instances)  

def op_gt(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_lt(right, left)

def op_ge(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_le(right, left)

def op_and(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(And(left.instances, right.instances))  

def op_or(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(Or(left.instances, right.instances)) 

def op_xor(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(Xor(left.instances, right.instances)) 

def op_implies(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(Implies(left.instances, right.instances)) 

def op_equivalence(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(And(Implies(left.instances, right.instances),
                       Implies(right.instances, left.instances))) 

def op_ifthenelse(cond, ifexpr, elseexpr):
    assert isinstance(cond, ExprArg)
    assert isinstance(ifexpr, ExprArg)
    assert isinstance(elseexpr, ExprArg)
    return BoolArg(If(cond.instances, ifexpr.instances, elseexpr.instances))

def set_extend(left,right):
    '''
    extends two sets to facilitate set operations
    Simplified Example:
       Extend(Set(A,B), Set(B,C)) => (Set(A,B,C), Set(A,B,C)),
       In this case, the C's in the left set are "zeroed", and
       the A's in the right set are "zeroed"
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
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
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (extendedL, extendedR) = set_extend(left,right)
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.min2(extendedL.instances.pop(0), extendedR.instances.pop(0)))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)

def op_intersection(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (extendedL, extendedR) = set_extend(left,right)
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.max2(extendedL.instances.pop(0), extendedR.instances.pop(0)))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)

def op_difference(left,right):
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
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (extendedL, extendedR) = set_extend(left,right)
    finalExpr = True
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalExpr = And(finalExpr, Implies(extendedL.instances.pop(0) != i.parentInstances, 
                                               extendedR.instances.pop(0) != i.parentInstances))
    return BoolArg(finalExpr)

def op_nin(left,right):
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    expr = op_in(left,right)
    return ExprArg(expr.joinSorts, expr.instanceSorts, Not(expr.instances))

def op_domain_restriction(l,r):
    pass

def op_range_restriction(l,r):
    pass

def op_sum(arg):
    assert isinstance(arg, ExprArg)
    return IntArg(Sum(arg.instances))

'''
    Map used to convert Clafer operations to Z3 operations
    keys: operation(str) returned by Clafer Python generator
    values: pairs:
        1. arity
        2. function associated with the operator
'''
ClaferToZ3OperationsMap = {
                           #Unary Ops
                           "!"           : (1, Not),
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
    :returns: 4-tuple from ClaferToZ3OperationsMap with the fields:
    
    The 4-tuple has the fields:
        1. arity
        2. equivalent operation(str) in Z3 (e.g. '&&' maps to 'And')
        3. isPrefix(boolean), states whether the op is prefix or infix in Z3
        4. function associated with the operator
    '''
    if(op in ClaferToZ3OperationsMap):
        return ClaferToZ3OperationsMap[op]
    else:
        sys.exit("Error in getOperationConversion(op)")

class BracketedConstraint(object):
    '''
    :var stack: ([]) Used to process a tree of expressions.
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, z3, claferStack):
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
            
    #might need to join better (e.g. B and B should be B+B, not [B, B]
    #SHOULD JOIN THE INDIVIDUAL INSTANCES, NOT THE WHOLE THING
    #may need to reverse pops
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
                    for i in instanceSorts:
                        for j in range(i.numInstances): 
                            innerExpr = Or(innerExpr, 
                                           Or(*[k != i.parentInstances for k in h[firstIndexOfCurrentSort + j] ]))
                        firstIndexOfCurrentSort = firstIndexOfCurrentSort + i.numInstances
                    finalInnerInstances.append(innerExpr)
                finalInstances.append(And(*finalInnerInstances))
            elif quantifier == "All":
                for i in instances:
                    finalInstances.append(And(*[Implies(currIfConstraints[j], i[j]) for j in range(len(i))]))
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
                    tempInstances.append(i.instances[0])
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
                self.z3.z3_bracketed_constraints.append(Implies(thisClafer.instances[i] != thisClafer.parentInstances, expr.instances[i]))
        else:
            for i in expr.instances:
                self.z3.z3_bracketed_constraints.append(i)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
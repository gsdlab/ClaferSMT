'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Common
from lxml.builder import basestring
from z3 import Function, IntSort, BoolSort, If, Not, Sum, Implies, Or, And, Xor
import sys


def joinWithSuper(sort, instances):
    newinstances = []
    for i in range(len(instances)):
        newinstances.append(If(instances[i] != sort.parentInstances, sort.superSort.instances[i + sort.indexInSuper], sort.superSort.parentInstances))
    return(sort.superSort, newinstances)

#can optimize this.parent
def op_join(l, r):
    (lsorts, linstances) = l
    (rsorts, rinstances) = r
    leftJoinPoint = lsorts[-1]
    rightJoinPoint = rsorts[0]
    if isinstance(rightJoinPoint, basestring):
        newinstances = []
        if rightJoinPoint == "parent":
            for i in range(leftJoinPoint.parent.numInstances):
                clause = Or(*[j == i for j in linstances])
                newinstances.append(If(clause, leftJoinPoint.parent.instances[i], leftJoinPoint.parent.parentInstances))
        return([leftJoinPoint.parent], newinstances)
    else:
        #join with super abstract
        if not(rightJoinPoint in leftJoinPoint.fields):
            #deep copy list, should change eventually
            lsorts = lsorts[:]
            lsorts.pop()
            (leftJoinPoint, linstances) = joinWithSuper(leftJoinPoint, linstances)
            lsorts.append(leftJoinPoint)
        join_function = Function("join" + str(Common.getFunctionUID()) + ":" + str(leftJoinPoint) + "." + str(rightJoinPoint), IntSort(), BoolSort())
        constraints = [join_function(i) == (linstances[i] != leftJoinPoint.parentInstances) for i in range(len(linstances))]
        leftJoinPoint.z3.z3_constraints = leftJoinPoint.z3.z3_constraints + constraints
        newinstances = [If(join_function(rinstances[i]), rinstances[i], rightJoinPoint.parentInstances) for i in range(len(rinstances))]
        return ([rightJoinPoint], newinstances)        
    
def op_card(arg):
    (sorts, instances) = arg
    rightmostInstance = sorts[-1]
    bool2Int = rightmostInstance.z3.bool2Int
    instances = [bool2Int(rightmostInstance.parentInstances != instances[i]) for i in range(len(instances))]
    return (["int"], Sum(instances))    

def op_add(l,r):
    (_, linstance) = l
    (_, rinstance) = r
    return(["int"], linstance + rinstance)

def op_sub(l,r):
    (_, linstance) = l
    (_, rinstance) = r
    return(["int"], linstance - rinstance)

def op_mul(l,r):
    (_, linstance) = l
    (_, rinstance) = r
    return(["int"], linstance * rinstance)

#integer division
def op_div(l,r):
    (_, linstance) = l
    (_, rinstance) = r
    return(["int"], linstance / rinstance if((not isinstance(linstance, int)) or (not isinstance(rinstance, int)))
                             else linstance // rinstance)
    
def op_un_minus(arg):
    (_, expr) = arg
    return (["int"], -(expr))
    
def op_eq(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], lvalue == rvalue)  
    
def op_ne(l,r):
    (_, expr) = op_eq(l,r)
    return (["bool"], Not(expr))
    
def op_lt(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], lvalue < rvalue)  
        
def op_le(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], lvalue <= rvalue)  

def op_gt(l,r):
    return op_lt(r,l)

def op_ge(l,r):
    return op_le(r,l)

def op_and(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], And(lvalue, rvalue))  

def op_or(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], Or(lvalue, rvalue))  

def op_xor(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], Xor(lvalue, rvalue))  

def op_implies(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], Implies(lvalue, rvalue)) 

def op_equivalence(l,r):
    (_, lvalue) = l
    (_, rvalue) = r
    return (["bool"], And(Implies(lvalue, rvalue), Implies(rvalue, lvalue)))

def op_ifthenelse(cond, ifexpr, elseexpr):
    (_, condvalue) = cond
    (_, ifvalue) = ifexpr
    (_, elsevalue) = elseexpr
    return (["bool"], If(condvalue, ifvalue, elsevalue))



def set_extend(l,r):
    '''
    extends two sets to facilitate set operations
    Simplified Example:
       Extend(Set(A,B), Set(B,C)) => (Set(A,B,C), Set(A,B,C)),
       In this case, the C's in the left set are "zeroed", and
       the A's in the right set are "zeroed"
    '''
    (lsorts, linstances) = l
    (rsorts, rinstances) = r
    finalsorts = []
    finalLinstances = []
    finalRinstances = []
    while lsorts or rsorts:
        if (not rsorts):
            nextsort = lsorts.pop(0)
            for _ in range(nextsort.numInstances):
                finalLinstances.append(linstances.pop(0))
                finalRinstances.append(nextsort.parentInstances)
        elif (not lsorts):
            nextsort = rsorts.pop(0)
            for _ in range(nextsort.numInstances):
                finalLinstances.append(nextsort.parentInstances)
                finalRinstances.append(rinstances.pop(0))
        elif lsorts[0].element.uid < rsorts[0].element.uid:
            nextsort = lsorts.pop(0)
            for _ in range(nextsort.numInstances):
                finalLinstances.append(linstances.pop(0))
                finalRinstances.append(nextsort.parentInstances)
        elif lsorts[0].element.uid > rsorts[0].element.uid:
            nextsort = rsorts.pop(0)
            for _ in range(nextsort.numInstances):
                finalLinstances.append(nextsort.parentInstances)
                finalRinstances.append(rinstances.pop(0))        
        else:
            nextsort = lsorts.pop(0)
            rsorts.pop(0)
            for _ in range(nextsort.numInstances):
                finalLinstances.append(linstances.pop(0))
                finalRinstances.append(rinstances.pop(0))
        
        finalsorts.append(nextsort)
    return((finalsorts, finalLinstances), (finalsorts, finalRinstances))

def op_union(l,r):
    (extendedL, extendedR) = set_extend(l,r)
    (sorts, extendedLinstances) = extendedL
    (_, extendedRinstances) = extendedR
    finalInstances = []
    for i in sorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.min2(extendedLinstances.pop(0), extendedRinstances.pop(0)))
    return (sorts, finalInstances)

def op_intersection(l,r):
    (extendedL, extendedR) = set_extend(l,r)
    (sorts, extendedLinstances) = extendedL
    (_, extendedRinstances) = extendedR
    finalInstances = []
    for i in sorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.max2(extendedLinstances.pop(0), extendedRinstances.pop(0)))
    return (sorts, finalInstances)

def op_difference(l,r):
    (extendedL, extendedR) = set_extend(l,r)
    (sorts, extendedLinstances) = extendedL
    (_, extendedRinstances) = extendedR
    finalInstances = []
    for i in sorts:
        for _ in range(i.numInstances):
            linstance = extendedLinstances.pop(0)
            finalInstances.append(If(And(linstance != i.parentInstances, extendedRinstances.pop(0) == i.parentInstances)
                                     , linstance
                                     , i.parentInstances))
    return (sorts, finalInstances)

def op_in(l,r):
    (extendedL, extendedR) = set_extend(l,r)
    (sorts, extendedLinstances) = extendedL
    (_, extendedRinstances) = extendedR
    finalExpr = True
    for i in sorts:
        for _ in range(i.numInstances):
            finalExpr = And(finalExpr, Implies(extendedLinstances.pop(0) != i.parentInstances, 
                                               extendedRinstances.pop(0) != i.parentInstances))
    return (sorts, finalExpr)

def op_nin(l,r):
    (sorts, finalExpr) = op_in(l,r)
    return (sorts, Not(finalExpr))

def op_domain_restriction(l,r):
    pass

def op_range_restriction(l,r):
    pass



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
                           "sum"         : (1, "TODO"),    
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
                           "ifthenelse"  : (3, "TODO")       
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
        self.value = "bracketed constraint"
        
    
    
    
    def addArg(self, arg):
        #handle this, and eventually parent
        self.stack.append(arg)
            
    def extend(self, args):
        maxInstances = 0
        extendedArgs = []
        for i in args:
            (_, instances) = i
            maxInstances = max(maxInstances, len(instances))
        for i in args:
            (sorts, instances) = i
            if len(instances) != maxInstances:
                tempInstances = []
                for i in range(maxInstances):
                    tempInstances.append(instances[0])
                extendedArgs.append((sorts, tempInstances))
            else:
                extendedArgs.append(i)
        return (maxInstances, extendedArgs)
                
    def addOperator(self, operation):
        (arity, operator) = getOperationConversion(operation)
        args = []
        for _ in range(0,arity):
            args.insert(0, self.stack.pop())
        (maxInstances, duplicatedArgs) = self.extend(args)
        finalExprs = []
        for i in range(maxInstances):
            tempExprs = []
            for j in duplicatedArgs:
                (sorts, instances) = j
                tempExprs.append((sorts,instances[i]))
            finalExprs.append(tempExprs)
        finalExprs = [operator(*finalExprs[i]) for i in range(len(finalExprs))]
        (sorts,_) = finalExprs[0]
        finalExprs = [exprs for (_,exprs) in finalExprs]
        self.stack.append((sorts,finalExprs))
    
    def endProcessing(self, parentClafer):
        self.value = self.stack.pop()
        (_, exprs) = self.value
        if(self.claferStack):
            thisClafer = self.claferStack[-1]
            for i in range(thisClafer.numInstances):
                self.z3.z3_bracketed_constraints.append(Implies(thisClafer.instances[i] != thisClafer.parentInstances, exprs[i]))
        else:
            for i in exprs:
                self.z3.z3_bracketed_constraints.append(i)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
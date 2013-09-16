'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from z3 import Function, IntSort, BoolSort, If, Not, Sum, Implies
import sys



def op_join(l, r):
    (lsorts, linstances) = l
    (rsorts, rinstances) = r
    leftJoinPoint = lsorts[-1]
    rightJoinPoint = rsorts[0]
    
    join_function = Function("join:" + str(leftJoinPoint) + "." + str(rightJoinPoint) + str(leftJoinPoint.z3.getFunctionUID()), IntSort(), BoolSort())
    constraints = [join_function(i) == (linstances[i] != leftJoinPoint.parentInstances) for i in range(len(linstances))]
    leftJoinPoint.z3.z3_constraints = leftJoinPoint.z3.z3_constraints + constraints
    newinstances = [If(join_function(rinstances[i]), rinstances[i], rightJoinPoint.parentInstances) for i in range(len(rinstances))]
    return (lsorts + rsorts, newinstances)        
    
def op_add(l,r):
    pass

def op_sub(l,r):
    pass

def op_mul(l,r):
    pass

#integer division
def op_div(l,r):
    pass
    
def op_un_minus(e):
    return (e[0], [[-i for i in j] for j in e[1]])
    
def op_eq(l,r):
    (lsorts, lvalue) = l
    (rsorts, rvalue) = r
    return (lsorts+rsorts, lvalue == rvalue)  
    
def op_ne(l,r):
    return Not(op_eq(l,r))
    
def op_lt(l,r):
    pass
        
def op_le(l,r):
    pass

def op_gt(l,r):
    return op_lt(r,l)

def op_ge(l,r):
    return op_le(r,l)

def op_and(l,r):
    pass

def op_or(l,r):
    pass

def op_union(l,r):
    pass 

def op_in(l,r):
    pass

def op_card(arg):
    (sorts, instances) = arg
    rightmostInstance = sorts[-1]
    bool2Int = rightmostInstance.z3.bool2Int
    instances = [bool2Int(rightmostInstance.parentInstances != instances[i]) for i in range(len(instances))]
    return (sorts, Sum(instances))    
    

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
                           "<=>"         : (2, lambda *args: args),
                           "=>"          : (2, lambda *args: args),
                           "||"          : (2, op_or),
                           "xor"         : (2, lambda *args: args),
                           "&&"          : (2, op_and),
                           "<"           : (2, op_lt),
                           ">"           : (2, op_gt),
                           "<="          : (2, op_le),
                           ">="          : (2, op_ge),
                           "="           : (2, op_eq),
                           "!="          : (2, op_ne),
                           "in"          : (2, op_in),
                           "nin"         : (2, lambda *args: args),
                           "+"           : (2, op_add),
                           "-"           : (2, op_sub),
                           "*"           : (2, op_mul),
                           "/"           : (2, op_div),
                           "++"          : (2, op_union),
                           "--"          : (2, "TODO"),
                           "&"           : (2, "TODO"),
                           "<:"          : (2, "TODO"),
                           ":>"          : (2, "TODO"),
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
        (maxInstances, extendedArgs) = self.extend(args)
        finalExprs = []
        for i in range(maxInstances):
            tempExprs = []
            for j in extendedArgs:
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
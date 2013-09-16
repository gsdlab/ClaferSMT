'''
Created on Apr 28, 2013

@author: ezulkosk
'''
from z3 import Function, IntSort, BoolSort, If, Not, Sum
import sys

NORMAL = 0
DEBUG = 1
TEST = 2
MODE = NORMAL

def debug_print(string):
    if(MODE == DEBUG):
        print(string)
        
def standard_print(string):
    if(MODE != TEST):
        print(string)

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




    
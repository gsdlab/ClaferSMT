'''
Created on Apr 28, 2013

@author: ezulkosk
'''



from ast import ClaferId, IntegerLiteral
from common import ClaferSort
from lxml.builder import basestring
from z3 import *
import operator
import time

def resolve(arg):
    if not isinstance(arg,tuple):
        return arg
    else:
        (s, sort) = arg
        return sort #needs to change

#ensures the lists are the same size through replication of the smaller list
def extend(l,r):
    #believe this only happens for int literals
    (lsort, lbits) = l
    (rsort, rbits) = r
    
    if len(lbits) < len(r):
        lbits = [i for i in lbits for _ in range(int(len(rbits)/len(lbits)))]
    elif len(lbits) > len(rbits):
        rbits = [i for i in rbits for _ in range(int(len(lbits)/len(rbits)))]       
    return (lbits, rbits)

def addFuncs():
    pass

def op_join(l, r):
    (lsorts, linstances) = l
    (rsorts, rinstances) = r
    leftJoinPoint = lsorts[-1]
    rightJoinPoint = rsorts[0]
    
    #newinstances = [False for _ in range(len(rinstances))]
    #for i in range(len(linstances)):
    #for i in range(len(rinstances)):
    #    newinstances[i] = Or(newinstances[i], If(leftJoinPoint.full(rinstances[i]), True, False))
    millis = int(round(time.time() * 1000))
    joinFunc = Function("join:" + str(leftJoinPoint) + "." + str(rightJoinPoint) + str(leftJoinPoint.z3.getFunctionUID()), IntSort(), BoolSort())
    constraints = [joinFunc(i) == (linstances[i] != leftJoinPoint.parentInstances) for i in range(len(linstances))]
    leftJoinPoint.z3.z3_constraints = leftJoinPoint.z3.z3_constraints + constraints
    leftJoinPoint.z3.join = joinFunc
    #print(constraints)
    #print()
    newinstances = [If(joinFunc(rinstances[i]), rinstances[i], rightJoinPoint.parentInstances) for i in range(len(rinstances))]
    
    #for i in range(len(rinstances)):
    #    newinstances[i] = If(newinstances[i], rinstances[i], rightJoinPoint.parentInstances)
    return (lsorts + rsorts, newinstances)        
    
    
    '''
    if isinstance(l, ClaferSort.ClaferSort) and isinstance(r, ClaferSort.ClaferSort):
        return (r.full, r.numInstances)
    else:
        (lfunc, linstances) = l
        constraints = [0 for _ in range(r.numInstances)]
        #joinFunc = Function("join:" + r.element.uid , IntSort(), IntSort())
        for i in range(linstances):
            for j in range(len(constraints)):
                constraints[j] = constraints[j] + If(lfunc(i), r.mask(i,j),0)   #r.mask()
        return constraints
    #rightFunc = r.
    '''

def op_add(l,r):
    (l,r) = extend(l,r)
    return ("int",[i+j for i,j in zip(l,r)])

def op_sub(l,r):
    (l,r) = extend(l,r)
    return ("int",[i-j for i,j in zip(l,r)])

def op_mul(l,r):
    (l,r) = extend(l,r)
    return ("int",[i*j for i,j in zip(l,r)])

#integer division
def op_div(l,r):
    (l,r) = extend(l,r)
    return ("int",[i//j for i,j in zip(l,r)])
    
def op_un_minus(e):
    return (e[0], [[-i for i in j] for j in e[1]])
    
def op_eq(l,r):
    #leftint = isinstance(l, IntegerLiteral.IntegerLiteral)
    #rightint = isinstance(r, IntegerLiteral.IntegerLiteral)
    #(l,r) = extend(l,r)
    (lsorts, lvalue) = l
    (rsorts, rvalue) = r
    return (lsorts+rsorts, lvalue == rvalue)  
    
def op_ne(l,r):
    return Not(op_eq(l,r))
    
def op_lt(l,r):
    (l,r) = extend(l,r)
    return [i < j for i,j in zip(l,r)]
        
def op_le(l,r):
    (l,r) = extend(l,r)
    return [i <= j for i,j in zip(l,r)]

def op_gt(l,r):
    return op_lt(r,l)

def op_ge(l,r):
    return op_le(r,l)

def op_and(l,r):
    #test 
    return [And(i,j) for i,j in zip(l,r)]

def op_or(l,r):
    #test
    return[Or(i,j) for i,j in zip(l,r)]

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




    
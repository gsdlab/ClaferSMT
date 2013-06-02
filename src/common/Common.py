'''
Created on Apr 28, 2013

@author: ezulkosk
'''



from ast import ClaferId
from common import ClaferSort
from lxml.builder import basestring
from z3 import *
import operator

def resolve(arg):
    if not isinstance(arg,tuple):
        return arg
    else:
        (s, sort) = arg
        return sort #needs to change

#ensures the lists are the same size through replication of the smaller list
def extend(l,r):
    #believe this only happens for int literals
    l = list(l)
    r = list(r)
    if len(l) < len(r):
        l = l * int(len(r)/len(l))
    elif len(l) > len(r):
        r = r * int(len(l)/len(r))       
    return (l,r)

def op_join(l, r):
    if isinstance(r, ClaferId.ClaferId) and r.id == "ref":
        return l.claferSort.refs
    elif isinstance(l, ClaferId.ClaferId) and l.id == "this":
        rightHandPartitions = l.claferSort.partitionSize * l.claferSort.partitions
        rightHandPartitionSize = int(len(r) / rightHandPartitions)
        return [ Sum(r[i*rightHandPartitionSize : (i+1)*rightHandPartitionSize]) 
                  for i in range(len(l.claferSort.bits))]
    elif isinstance(r[0], ArithRef):
        #needs to be fixed
        return [Sum(*r)]    #(str(l) + " join " +str(r))
    raise Exception("Join error")

def op_add(l,r):
    (l,r) = extend(l,r)
    return [i+j for i,j in zip(l,r)]

def op_sub(l,r):
    (l,r) = extend(l,r)
    return [i-j for i,j in zip(l,r)]

def op_mul(l,r):
    (l,r) = extend(l,r)
    return [i*j for i,j in zip(l,r)]

#integer division
def op_div(l,r):
    (l,r) = extend(l,r)
    return [i//j for i,j in zip(l,r)]
    
def op_un_minus(e):
    return [-i for i in e]
    
def op_eq(l,r):    
    (l,r) = extend(l,r)
    return [i == j for i,j in zip(l,r)]
    
def op_ne(l,r):
    (l,r) = extend(l,r)
    return [i != j for i,j in zip(l,r)]
    
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
                           "#"           : (1, "TODO"),
                           "max"         : (1, "TODO"),
                           "min"         : (1, "TODO"),
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
                           "in"          : (2, lambda *args: args),
                           "nin"         : (2, lambda *args: args),
                           "+"           : (2, op_add),
                           "-"           : (2, op_sub),
                           "*"           : (2, op_mul),
                           "/"           : (2, op_div),
                           "++"          : (2, "TODO"),
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




    
'''
Created on Apr 28, 2013

@author: ezulkosk
'''


import operator
from z3 import *

'''
    Map used to convert Clafer operations to Z3 operations
    keys: operation(str) returned by Clafer Python generator
    values: 3-tuples:
        1. arity
        2. equivalent operation(str) in Z3 (e.g. '&&' maps to 'And')
        3. isPrefix(boolean), states whether the op is prefix or infix in Z3
        4. function associated with the operator
'''
ClaferToZ3OperationsMap = {
                           #Unary Ops
                           "!"           : (1, "Not", True,Not),
                           "UNARY_MINUS" : (1, "-", True, operator.neg),
                           "#"           : (1, "TODO", True, "TODO"),
                           "max"         : (1, "TODO", True, "TODO"),
                           "min"         : (1, "TODO", True, "TODO"),
                           #Binary Ops
                           "<=>"         : (2, "TODO", False, lambda *args: args),
                           "=>"          : (2, "TODO", False, lambda *args: args),
                           "||"          : (2, "Or", True, Or),
                           "xor"         : (2, "TODO", True, lambda *args: args),
                           "&&"          : (2, "And", True, And),
                           "<"           : (2, "<", False, operator.lt),
                           ">"           : (2, ">", False, operator.gt),
                           "<="          : (2, "<=", False, operator.le),
                           ">="          : (2, ">=", False, operator.ge),
                           "="           : (2, "=", False, operator.eq),
                           "!="          : (2, "!=", False, operator.ne),
                           "in"          : (2, "TODO", False, lambda *args: args),
                           "nin"         : (2, "TODO", False, lambda *args: args),
                           "+"           : (2, "+", False, operator.add),
                           "-"           : (2, "-", False, operator.sub),
                           "*"           : (2, "*", False, operator.mul),
                           "/"           : (2, "/", False, operator.truediv),
                           "++"          : (2, "TODO", False, "TODO"),
                           "--"          : (2, "TODO", False, "TODO"),
                           "&"           : (2, "TODO", False, "TODO"),
                           "<:"          : (2, "TODO", False, "TODO"),
                           ":>"          : (2, "TODO", False, "TODO"),
                           "."           : (2, "TODO", False, operator.add),
                           #Ternary Ops
                           "ifthenelse"  : (3, "If", True)       
                           }



'''
op(str): string representation of Clafer operation
returns: 3-tuple from ClaferToZ3OperationsMap (see above)
'''
def getOperationConversion(op):
    if(op in ClaferToZ3OperationsMap):
        return ClaferToZ3OperationsMap[op]
    else:
        sys.exit("Error in getOperationConversion(op)")


    

    
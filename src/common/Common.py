'''
Created on Apr 28, 2013

@author: ezulkosk
'''

import common.ClaferSort
import sys
'''
    Map used to convert Clafer operations to Z3 operations
    keys: operation(str) returned by Clafer Python generator
    values: 3-tuples:
        1. arity
        2. equivalent operation(str) in Z3 (e.g. '&&' maps to 'And')
        3. isPrefix(boolean), states whether the op is prefix or infix in Z3
'''
ClaferToZ3OperationsMap = {
                           #Unary Ops
                           "!"           : (1, "Not", True),
                           "UNARY_MINUS" : (1, "-", True),
                           "#"           : (1, "TODO", True),
                           "max"         : (1, "TODO", True),
                           "min"         : (1, "TODO", True),
                           #Binary Ops
                           "<=>"         : (2, "TODO", False),
                           "=>"          : (2, "TODO", False),
                           "||"          : (2, "Or", True),
                           "xor"         : (2, "TODO", True),
                           "&&"          : (2, "And", True),
                           "<"           : (2, "<", False),
                           ">"           : (2, ">", False),
                           "<="          : (2, "<=", False),
                           ">="          : (2, ">=", False),
                           "="           : (2, "=", False),
                           "!="          : (2, "!=", False),
                           "in"          : (2, "TODO", False),
                           "nin"         : (2, "TODO", False),
                           "+"           : (2, "+", False),
                           "-"           : (2, "-", False),
                           "*"           : (2, "*", False),
                           "/"           : (2, "/", False),
                           "++"          : (2, "TODO", False),
                           "--"          : (2, "TODO", False),
                           "&"           : (2, "TODO", False),
                           "<:"          : (2, "TODO", False),
                           ":>"          : (2, "TODO", False),
                           "."           : (2, "TODO", False),
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


    

    
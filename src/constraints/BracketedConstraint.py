'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Assertions
from constraints import Constraints
from constraints.Constraints import GenericConstraints
from structures.ExprArg import BoolArg
from z3 import Implies, And, Or
import constraints.Operations as Ops
import sys


'''
    Map used to convert Clafer operations to Z3 operations
    keys: operation(str) returned by Clafer Python generator
    values: pairs:
        1. arity
        2. function associated with the operator
'''

ClaferToZ3OperationsMap = {
                           #Unary Ops
                           "!"           : (1, Ops.op_not),
                           "UNARY_MINUS" : (1, Ops.op_un_minus),
                           "#"           : (1, Ops.op_card),
                           "max"         : (1, "TODO"),
                           "min"         : (1, "TODO"),
                           "sum"         : (1, Ops.op_sum),    
                           #Binary Ops
                           "<=>"         : (2, Ops.op_equivalence),
                           "=>"          : (2, Ops.op_implies),
                           "||"          : (2, Ops.op_or),
                           "xor"         : (2, Ops.op_xor),
                           "&&"          : (2, Ops.op_and),
                           "<"           : (2, Ops.op_lt),
                           ">"           : (2, Ops.op_gt),
                           "<="          : (2, Ops.op_le),
                           ">="          : (2, Ops.op_ge),
                           "="           : (2, Ops.op_eq),
                           "!="          : (2, Ops.op_ne),
                           "in"          : (2, Ops.op_in),
                           "nin"         : (2, Ops.op_nin),
                           "+"           : (2, Ops.op_add),
                           "-"           : (2, Ops.op_sub),
                           "*"           : (2, Ops.op_mul),
                           "/"           : (2, Ops.op_div),
                           "++"          : (2, Ops.op_union),
                           "--"          : (2, Ops.op_difference),
                           "&"           : (2, Ops.op_intersection),
                           "<:"          : (2, Ops.op_domain_restriction),
                           ":>"          : (2, Ops.op_range_restriction),
                           "."           : (2, Ops.op_join),
                           #Ternary Ops
                           "ifthenelse"  : (3, Ops.op_ifthenelse),
                           #String Ops
                           "concat"      : (2, Ops.op_concat),
                           "length"      : (1, Ops.op_length),
                           "substring"   : (3, Ops.op_substring),
                           "contains"    : (2, Ops.op_contains),
                           "indexOf"     : (2, Ops.op_indexof),
                           "replace"     : (3, Ops.op_replace),
                           "split"       : (2, Ops.op_split)
                           }

QuantifierMap = {
               "All"           : Ops.quant_all,
               "Lone"          : Ops.quant_lone,
               "One"           : Ops.quant_one,
               "No"            : Ops.quant_no, 
               "Some"          : Ops.quant_some, 
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

def getQuantifier(quant):
    '''
    :param op: String representation of Clafer operation.
    :type op: str
    :returns: 2-tuple from ClaferToZ3OperationsMap with the fields:
    
    The 2-tuple has the fields:
        1. arity of the function
        2. function associated with the operator
    '''
    return QuantifierMap[quant]

class BracketedConstraint(Constraints.GenericConstraints):
    '''
    :var stack: ([]) Used to process a tree of expressions.
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, z3, claferStack):
        ident = "BC:" + ".".join([str(i.element.uid) for i in claferStack])
        GenericConstraints.__init__(self, ident)
        self.z3 = z3
        self.claferStack = claferStack
        self.stack = []
        self.locals = {}
        self.value = None
        
    def addLocal(self, uid, expr):
        self.locals[uid] = expr
    
    def addArg(self, arg):
        self.stack.append(arg)
       
    #clean     
    def addQuantifier(self, quantifier, num_args, num_combinations, ifconstraints):
        localStack = []
        ifConstraints = []
        for _ in range(num_combinations):
            localStack.append(self.stack.pop())
            if ifconstraints:
                ifConstraints.append(ifconstraints.pop())
            else:
                ifConstraints = []
        localStack.reverse()
        ifConstraints.reverse()
        '''
        for _ in range(num_combinations):
            currExpr = localStack.pop(0)
            if ifConstraints:
                currIfConstraint = ifConstraints.pop(0)
            else:
                currIfConstraint = None
                
            quantFunction = getQuantifier(quantifier)
            cond = quantFunction(currExpr)
            
            if currIfConstraint:
                cond = Implies(currIfConstraint, cond)
            condList.append(cond)
        self.stack.append([BoolArg([And(*condList)])])
        '''
        #for _ in range(num_combinations):
        #    currExpr = localStack.pop(0)
        #    condList.append(currExpr)
        quantFunction = getQuantifier(quantifier)
        cond = quantFunction(localStack, ifConstraints)
        Assertions.nonEmpty(cond)
        self.stack.append([BoolArg([cond])])
        
        
    def extend(self, args):
        maxInstances = 0
        extendedArgs = []
        for i in args:
            maxInstances = max(maxInstances, len(i))
        for i in args:
            if len(i) != maxInstances:
                if len(i) != 1:
                    sys.exit("Bug in BracketedConstraint.")
                extendedArgs.append([i[0].clone() for _ in range(maxInstances)])
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
                tempExprs.append(j[i])
            finalExprs.append(tempExprs)
        finalExprs = [operator(*finalExprs[i]) for i in range(len(finalExprs))]
        Assertions.nonEmpty(finalExprs)
        self.stack.append(finalExprs)
    
    def endProcessing(self, addToZ3 = True):
        if not self.stack:
            return
        self.value = self.stack.pop()
        expr = self.value
        if(self.claferStack):
            thisClafer = self.claferStack[-1]
            for i in range(thisClafer.numInstances):
                if thisClafer.numInstances == len(expr):
                    self.addConstraint(Implies(thisClafer.isOn(thisClafer.instances[i]), expr[i].finish()))
                #hack for now
                else:
                    self.addConstraint(Implies(thisClafer.isOn(thisClafer.instances[i]), expr[0].finish()))
        else:
            for i in expr:
                for j in i.getInstanceSorts():
                    (_, mask) = j
                    self.addConstraint(mask.pop_value())
        if addToZ3:
            self.z3.z3_bracketed_constraints.append(self)
        
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
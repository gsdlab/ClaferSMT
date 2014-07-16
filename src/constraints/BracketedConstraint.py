'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Assertions, Common, SMTLib
from constraints import Constraints
from constraints.Constraints import GenericConstraints
from constraints.operations import Join, Numeric, String, Quantifier, Boolean, \
    Set
from structures.ExprArg import BoolArg
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
                           "!"           : (1, Boolean.op_not),
                           "UNARY_MINUS" : (1, Numeric.op_un_minus),
                           "#"           : (1, Set.op_card),
                           "sum"         : (1, Numeric.op_sum),    
                           #Binary Ops
                           "<=>"         : (2, Boolean.op_equivalence),
                           "=>"          : (2, Set.op_implies),
                           "||"          : (2, Boolean.op_or),
                           "xor"         : (2, Boolean.op_xor),
                           "&&"          : (2, Boolean.op_and),
                           "<"           : (2, Numeric.op_lt),
                           ">"           : (2, Numeric.op_gt),
                           "<="          : (2, Numeric.op_le),
                           ">="          : (2, Numeric.op_ge),
                           "="           : (2, Set.op_eq),
                           "!="          : (2, Set.op_ne),
                           "in"          : (2, Set.op_in),
                           "nin"         : (2, Set.op_nin),
                           "+"           : (2, Numeric.op_add),
                           "-"           : (2, Numeric.op_sub),
                           "*"           : (2, Numeric.op_mul),
                           "/"           : (2, Numeric.op_div),
                           "++"          : (2, Set.op_union),
                           "--"          : (2, Set.op_difference),
                           "&"           : (2, Set.op_intersection),
                           "<:"          : (2, Set.op_domain_restriction),
                           ":>"          : (2, Set.op_range_restriction),
                           "."           : (2, Join.op_join),
                           #Ternary Ops
                           "ifthenelse"  : (3, Boolean.op_ifthenelse),
                           #String Ops
                           "concat"      : (2, String.op_concat),
                           "length"      : (1, String.op_length),
                           "substring"   : (3, String.op_substring),
                           "contains"    : (2, String.op_contains),
                           "indexOf"     : (2, String.op_indexof),
                           "replace"     : (3, String.op_replace),
                           "split"       : (2, String.op_split)
                           }

QuantifierMap = {
               "All"           : Quantifier.quant_all,
               "Lone"          : Quantifier.quant_lone,
               "One"           : Quantifier.quant_one,
               "No"            : Quantifier.quant_no, 
               "Some"          : Quantifier.quant_some, 
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
    
    def __init__(self, cfr, element, claferStack):
        ident = "BC" + str(Common.getConstraintUID()) + ":" + ".".join([str(i.element.uid) for i in claferStack])
        GenericConstraints.__init__(self, ident)
        self.element = element
        self.cfr = cfr
        self.claferStack = [i for i in claferStack]
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
                    sys.exit("Bug in BracketedConstraint." + str(i))
                extendedArgs.append([i[0] for _ in range(maxInstances)])
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
                    self.addConstraint(SMTLib.SMT_Implies(thisClafer.isOn(thisClafer.instances[i]), expr[i].finish()))
                #hack for now
                else:
                    self.addConstraint(SMTLib.SMT_Implies(thisClafer.isOn(thisClafer.instances[i]), expr[0].finish()))
        else:
            for i in expr:
                self.addConstraint(i.getBool())
        if addToZ3:
            self.cfr.smt_bracketed_constraints.append(self)
        
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
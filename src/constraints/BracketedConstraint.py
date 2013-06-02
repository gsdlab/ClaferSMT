'''
Created on Apr 29, 2013

@author: ezulkosk
'''

from collections import deque
from common import Common
from constraints import Constraint
from z3 import *

class BracketedConstraint(object):
    '''
    :var stack: ([Z3_expression]) Used to process a tree of expressions.
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, z3):
        self.z3 = z3
        self.stack = []
        
    def addArg(self, claferStack, arg):
        #self.stack.append(arg)
        #handle this, and eventually parent
        '''if arg == "this":
            this_sort =  ("this",claferStack[-1])
            self.stack.append(this_sort)
        elif arg == "ref":
            self.stack.append("ref")
        elif isinstance(arg, int):
            self.stack.append(arg)
        else:
            self.stack.append(self.z3.z3_sorts[arg])'''
        self.stack.append(arg)
            
    
    def addOperator(self, operation):
        (arity, operator) = Common.getOperationConversion(operation)
        args = []
        for _ in range(0,arity):
            args.insert(0, self.stack.pop())
        #print(args)
        self.stack.append(operator(*args))
    
    def endProcessing(self, parentClafer):
        self.value = self.stack.pop()
        #print(self.value)    
        if(parentClafer):
            self.z3.z3_bracketed_constraints.append([Implies(j == 1, i) for i,j in zip(self.value, parentClafer.bits)])
        else:
            self.z3.z3_bracketed_constraints.append(self.value)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
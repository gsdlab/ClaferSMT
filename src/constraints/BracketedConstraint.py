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
    :var stack: ([Z3_expression]) Used to process a tree of expressionts.
    :var value: (Z3_expression) The final Z3_expression representation of the constraint.
    
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, value = None):
        self.value = value
        self.stack = []
        
    def addArg(self, arg):
        self.stack.append(arg)
    
    
    def addOperator(self, operation):
        (arity, z3_op, isPrefix, operator) = Common.getOperationConversion(operation)
        args = deque([])
        for _ in range(0,arity):
            args.appendleft(self.stack.pop())
        print(args)
        
        self.stack.append(operator(*args))
    
    def endProcessing(self):
        self.value = self.stack.pop()
        print(self.value)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
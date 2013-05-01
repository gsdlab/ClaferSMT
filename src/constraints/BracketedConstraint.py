'''
Created on Apr 29, 2013

@author: ezulkosk
'''

from collections import deque
from common import Common
from constraints import Constraint
from z3 import *

class BracketedConstraint(Constraint.Constraint):
    '''
    stack([Z3_expression]): used to process expressions
    stringStack([str]): used to display/debug expressions
    '''
    def __init__(self, comment, stringValue = None, value = None):
        self.comment = comment
        if(stringValue is None):
            self.stringValue = "stub_constraint"
            self.stringStack = []
            self.stack = []
        else:
            self.stringValue = stringValue
            self.value = value
        
    def addArg(self, arg):
        self.stringStack.append(arg)
        self.stack.append(arg)
    
    '''
    Gets operator arity, pops off that number of elements from stack
    Places Z3-operator and args onto stack in string form
    '''
    def addOperator(self, operation):
        (arity, z3_op, isPrefix, operator) = Common.getOperationConversion(operation)
        stringArgs = deque([])
        args = deque([])
        for _ in range(0,arity):
            stringArgs.appendleft(self.stringStack.pop())
            args.appendleft(self.stack.pop())
        if(isPrefix):
            self.stringStack.append("(" + z3_op + "(" + ", ".join(map(str, stringArgs)) + "))")
        else:
            self.stringStack.append("(" + z3_op.join(map(str,stringArgs)) + ")")
        self.stack.append(operator(*args))
    '''
    when a constraint is finished processing,
    its string representation is the only thing in stack 
    '''
    def endProcessing(self):
        self.stringValue = self.stringStack.pop()
        self.value = self.stack.pop()
    
    def __str__(self):
        return self.comment + " === " + self.stringValue
    
    def __repr__(self):
        #return self.__str__()
        return self.comment + " === " + self.stringValue
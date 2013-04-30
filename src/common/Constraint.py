'''
Created on Apr 29, 2013

@author: ezulkosk
'''

from collections import deque
from common import Common
from z3 import *

class Constraint(object):
    
    '''
    value(str): contains the string representation of the constraint
    comment(str): used for debugging constraints
    stack([]): used to process expressions
    '''
    def __init__(self, comment, value = None):
        self.comment = comment
        if(value is None):
            self.value = "stub_constraint"
            self.stack = []
        else:
            self.value = value
        
    def addArg(self, arg):
        self.stack.append(arg)
    
    '''
    Gets operator arity, pops off that number of elements from stack
    Places Z3-operator and args onto stack in string form
    '''
    def addOperator(self, operation):
        (arity, z3_op, isPrefix) = Common.getOperationConversion(operation)
        args = deque([])
        for _ in range(0,arity):
            args.appendleft(self.stack.pop())
        if(isPrefix):
            self.stack.append("(" + z3_op + "(" + ", ".join(map(str, args)) + "))")
        else:
            self.stack.append("(" + z3_op.join(map(str,args)) + ")")
    
    '''
    when a constraint is finished processing,
    its string representation is the only thing in stack 
    '''
    def endProcessing(self):
        self.value = self.stack.pop()
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        #return self.__str__()
        return self.comment
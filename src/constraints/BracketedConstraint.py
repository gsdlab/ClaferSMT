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
    :var stack: ([Z3_expression]) Used to process a tree of expressionts.
    :var stringStack: ([str]) Used to display/debug expressions.
    :var stringValue: (str) The final string representation of the constraint.
    :var value: (Z3_expression) The final Z3_expression representation of the constraint.
    
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, comment, stringValue = None, value = None):
        '''
        :param comment: Description of constraint for debugging purposes.
        :type comment: str
        :param stringValue: More technical description of the constraint, essentially the string representially of the Z3 constraint.
        :type stringValue: str (o)
        :param value: The Z3_expression that will be passed to the solver.
        :type value: Z3_expression (o) 
        '''
        self.comment = comment
        if(stringValue is None):
            self.stringValue = "stub_constraint"
            self.stringStack = []
            self.stack = []
        else:
            self.stringValue = stringValue
            self.value = value
        
    def addArg(self, arg):
        '''
        TODO
        '''
        self.stringStack.append(arg)
        self.stack.append(arg)
    
    
    def addOperator(self, operation):
        '''
        :param operation: The expression operator in Clafer syntax.
        :type operation: str
        
        Gets operator arity, pops off that number of elements from stack and stringStack.
        Places Z3-operator and args onto stringStack in string form,
        and onto stack in Z3_expression form.
        '''
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
    
    def endProcessing(self):
        '''
        When a constraint is finished processing,
        its final representation is the only thing left on the stacks.
        Stores these values in *stringValue* and *value*.
        '''
        self.stringValue = self.stringStack.pop()
        self.value = self.stack.pop()
    
    def __str__(self):
        return self.comment + " === " + self.stringValue
    
    def __repr__(self):
        #return self.__str__()
        return self.comment + " === " + self.stringValue
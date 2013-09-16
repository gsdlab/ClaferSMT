'''
Created on Apr 29, 2013

@author: ezulkosk
'''


from common import Common
from constraints import Constraint
from z3 import *

class BracketedConstraint(object):
    '''
    :var stack: ([]) Used to process a tree of expressions.
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, z3, claferStack):
        self.z3 = z3
        self.claferStack = claferStack
        self.stack = []
        self.value = "bracketed constraint"
        
    def addArg(self, arg):
        #handle this, and eventually parent
        self.stack.append(arg)
            
    def extend(self, args):
        maxInstances = 0
        extendedArgs = []
        for i in args:
            (_, instances) = i
            maxInstances = max(maxInstances, len(instances))
        for i in args:
            (sorts, instances) = i
            if len(instances) != maxInstances:
                tempInstances = []
                for i in range(maxInstances):
                    tempInstances.append(instances[0])
                extendedArgs.append((sorts, tempInstances))
            else:
                extendedArgs.append(i)
        return (maxInstances, extendedArgs)
                
    def addOperator(self, operation):
        (arity, operator) = Common.getOperationConversion(operation)
        args = []
        for _ in range(0,arity):
            args.insert(0, self.stack.pop())
        #print(args)
        (maxInstances, extendedArgs) = self.extend(args)
        finalExprs = []
        for i in range(maxInstances):
            tempExprs = []
            for j in extendedArgs:
                (sorts, instances) = j
                tempExprs.append((sorts,instances[i]))
            finalExprs.append(tempExprs)
        finalExprs = [operator(*finalExprs[i]) for i in range(len(finalExprs))]
        (sorts,_) = finalExprs[0]
        finalExprs = [exprs for (_,exprs) in finalExprs]
        self.stack.append((sorts,finalExprs))
    
    def endProcessing(self, parentClafer):
        self.value = self.stack.pop()
        (_, exprs) = self.value
        if(self.claferStack):
            thisClafer = self.claferStack[-1]
            for i in range(thisClafer.numInstances):
                self.z3.z3_bracketed_constraints.append(Implies(thisClafer.instances[i] != thisClafer.parentInstances, exprs[i]))
        else:
            for i in exprs:
                self.z3.z3_bracketed_constraints.append(i)
    '''
self.value = self.stack.pop()
        (_, exprs) = self.value
        if(parentClafer):
            for i in range(self.this.numInstances):
                self.z3.z3_bracketed_constraints.append(Implies(self.this.instances[i] != self.this.parentInstances, exprs[i]))
        else:
            for i in exprs:
                self.z3.z3_bracketed_constraints.append(i)'''
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)
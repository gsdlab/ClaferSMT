'''
Created on Nov 11, 2013

@author: ezulkosk
'''
from ast.IntegerLiteral import IntegerLiteral
from common import Options
from common.Exceptions import UnusedAbstractException
from pip.backwardcompat import reduce
from visitors import VisitorTemplate, Visitor
import ast
import operator
import sys
import visitors

class AdjustAbstracts(VisitorTemplate.VisitorTemplate):
    '''
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    '''
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        self.z3 = z3
        self.glStack = []

    def computeScope(self):
        stack = self.glStack[:]
        stack.reverse()
        num = 1
        for i in stack:
            if i == -1:
                break
            num = num * i
        return num
    '''
    may need to fix for 3..*
    '''
    def claferVisit(self, element):
        (lower, upper) = element.card
        (glower, gupper) = element.glCard
        upper = upper.value
        sort = self.z3.z3_sorts[element.uid]
        
        if not self.glStack:
            self.glStack.append(gupper.value)
        elif sort.unbounded:
            self.glStack.append(-1)
            self.glStack.append(gupper.value)
        else:
            newScope = upper * self.glStack[-1]
            element.glCard = (lower, IntegerLiteral(newScope))
            self.glStack.append(newScope)
            #print(newScope)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.glStack.pop()
        if sort.unbounded and self.glStack:
            self.glStack.pop()
        '''
        sort = self.z3.z3_sorts[element.uid]
        newScope = reduce(operator.mul, self.scopeStack, 1)
        (_, u) = element.card
        if sort.numInstances != newScope and self.scopeStack and u.value != -1:
            sort.numInstances = self.scopeStack[-1] * u.value
        self.scopeStack.append(sort.numInstances)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.scopeStack.pop()    
        '''
        
def setAbstractScopes(z3):
    hasChanged = False
    for i in z3.z3_sorts.values():
        if i.element.isAbstract:
            summ = 0
            for j in i.subs:
                summ = summ + z3.getScope(j)
            (lower, upper) = i.element.glCard
            i.element.glCard = (lower, IntegerLiteral(summ))
            if upper.value != summ:
                #print(str(upper) + " " + str(summ))
                hasChanged = True
            #i.numInstances = summ#max(summ, Options.GLOBAL_SCOPE)#summ #temp
            #i.upperCardConstraint = summ
            if summ == 0:
                raise UnusedAbstractException(i.element.uid)
    return hasChanged 

def adjustAbstractsFixedPoint(z3):
    hasChanged = True
    while hasChanged:
        hasChanged = setAbstractScopes(z3)
        for i in z3.z3_sorts.values():
            if i.element.isAbstract:
                Visitor.visit(AdjustAbstracts(z3), i.element)
    
'''
Created on Nov 11, 2013

@author: ezulkosk
'''
from ast.Clafer import Clafer
from ast.IntegerLiteral import IntegerLiteral
from common import Options
from common.Exceptions import UnusedAbstractException
from pip.backwardcompat import reduce
from structures.ClaferSort import ClaferSort
from visitors import VisitorTemplate, Visitor
import ast
import operator
import sys
import visitors

class AdjustAbstracts(VisitorTemplate.VisitorTemplate):
    '''
    :var cfr: (:class:`~common.ClaferModel`) The Clafer model.
    '''
    def __init__(self, cfr):
        '''
        :param cfr: The Z3 solver.
        :type cfr: :class:`~common.Z3Instance`
        '''
        self.cfr = cfr
        self.hasChanged = False
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
        sort = self.cfr.cfr_sorts[element.uid]
        #print(element)
        #print(gupper)
        #print(sort.scope_summ)
        
        if sort.scope_summ >= 0 and sort.element.isAbstract:
            self.glStack.append(sort.scope_summ)
            element.glCard = (lower, IntegerLiteral(sort.scope_summ))
        elif sort.scope_summ >= 0:
            if self.glStack:
                newScope = sort.scope_summ * self.glStack[-1]
            else:
                total = 1
                for i in sort.parentStack:
                    (l,u) = i.element.glCard
                    total = total * u.value 
                newScope = total * sort.scope_summ
            element.glCard = (lower, IntegerLiteral(newScope))
            self.glStack.append(newScope)
        #elif sort.unbounded and isinstance(sort.refSort, ClaferSort) and sort.refSort.scope_summ >= 0:
        #    if self.glStack:
        #        newScope = sort.refSort.scope_summ * self.glStack[-1]
        #    else:
         #       newScope = sort.refSort.scope_summ
            #if newScope != gupper:
            #    self.hasChanged = True
        #    element.glCard = (lower, IntegerLiteral(newScope))
        #    self.glStack.append(newScope)
        elif not self.glStack or sort.unbounded:
            self.glStack.append(gupper.value)
        else:
            newScope = upper * self.glStack[-1]
            element.glCard = (lower, IntegerLiteral(newScope))
            self.glStack.append(newScope)
            #print(newScope)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.glStack.pop()
        '''
        sort = self.cfr.cfr_sorts[element.uid]
        newScope = reduce(operator.mul, self.scopeStack, 1)
        (_, u) = element.card
        if sort.numInstances != newScope and self.scopeStack and u.value != -1:
            sort.numInstances = self.scopeStack[-1] * u.value
        self.scopeStack.append(sort.numInstances)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.scopeStack.pop()    
        '''
        
def setAbstractScopes(cfr):
    hasChanged = False
    flag = False
    for i in cfr.cfr_sorts.values():
        #print(i.refSort)
        if i.element.isAbstract:# or (i.refSort and isinstance(i.refSort, ClaferSort)):
            if i.element.isAbstract:
                currAbs = i
            else:
                currAbs = i.refSort    
            
            summ = 0
            for j in currAbs.subs:
                summ = summ + cfr.getScope(j)
            (lower, upper) = i.element.glCard
            if i.element.isAbstract:
                i.element.glCard = (lower, IntegerLiteral(summ))
            elif i.element.isAbstract:
                flag = True   
             
            if upper.value != summ and not flag:
                #print(i)
                #print(str(upper) + " " + str(summ))
                hasChanged = True
            #i.numInstances = summ#max(summ, Options.GLOBAL_SCOPE)#summ #temp
            #i.upperCardConstraint = summ
            i.scope_summ = summ
            if summ == 0:
                continue
                raise UnusedAbstractException(i.element.uid)
    return hasChanged 

def adjustAbstractsFixedPoint(cfr):
    hasChanged = True
    while hasChanged:
        hasChanged = setAbstractScopes(cfr)
        for i in cfr.cfr_sorts.values():
            if i.element.isAbstract: #or (isinstance(i.refSort, ClaferSort)
                                    #    and i.refSort.element.isAbstract):
                adj = AdjustAbstracts(cfr)
                Visitor.visit(adj, i.element)
                if adj.hasChanged:
                    hasChanged = True
    
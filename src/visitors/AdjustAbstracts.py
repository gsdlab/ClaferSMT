'''
Created on Nov 11, 2013

@author: ezulkosk
'''
from ast.IntegerLiteral import IntegerLiteral
from common import Options
from common.Exceptions import UnusedAbstractException
from visitors import VisitorTemplate, Visitor
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
        
        if sort.scope_summ >= 0 and sort.element.isAbstract:
            self.glStack.append(sort.scope_summ)
            element.glCard = (lower, IntegerLiteral(sort.scope_summ))
        elif sort.scope_summ >= 0:
            if self.glStack:
                newScope = sort.scope_summ * self.glStack[-1]
            else:
                total = 1
                for i in sort.parentStack:
                    (_l,u) = i.element.glCard
                    total = total * u.value 
                newScope = total * sort.scope_summ
            element.glCard = (lower, IntegerLiteral(newScope))
            self.glStack.append(newScope)
        elif not self.glStack:
            self.glStack.append(gupper.value)
        elif sort.unbounded:
            glower = self.glStack[-1] * lower.value
            element.glCard = (glower, IntegerLiteral(max(glower, Options.GLOBAL_SCOPE)))
            self.glStack.append(max(Options.GLOBAL_SCOPE, glower))
        else:
            newScope = upper * self.glStack[-1]
            element.glCard = (lower, IntegerLiteral(newScope))
            self.glStack.append(newScope)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.glStack.pop()
        
def setAbstractScopes(cfr):
    hasChanged = False
    flag = False
    for i in cfr.cfr_sorts.values():
        if i.element.isAbstract: 
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
                hasChanged = True
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
            if i.element.isAbstract:  
                adj = AdjustAbstracts(cfr)
                Visitor.visit(adj, i.element)
                if adj.hasChanged:
                    hasChanged = True
    
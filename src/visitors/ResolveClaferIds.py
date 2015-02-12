'''
Created on May 31, 2013

@author: ezulkosk
'''

from visitors import VisitorTemplate
import visitors.Visitor




class ResolveClaferIds(VisitorTemplate.VisitorTemplate):
    '''
    :var CreateBracketedConstraints.currentConstraint: (:mod:`~constraints.BracketedConstraint`) Holds the constraint currently being traversed. 
    :var CreateBracketedConstraints.inConstraint: (bool) True if the traversal is currently within a constraint.
    :var claferStack: ([:mod:`~common.ClaferSort`]) Stack of clafers used primarily for debugging.
    :var cfr: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Converts Clafer constraints to cfr syntax,
    adds constraints to cfr.smt_constraints
    field.
    '''
    def __init__(self, cfr):
        '''
        :param cfr: The Z3 solver.
        :type cfr: :class:`~common.Z3Instance`
        '''
        VisitorTemplate.VisitorTemplate.__init__(self)
        self.cfr = cfr
        self.claferStack = []
    
    def claferVisit(self, element):
        self.claferStack.append(self.cfr.cfr_sorts[element.uid])
        #visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.claferStack.pop()
    
    def claferidVisit(self, element):
        if element.id == "clafer" or element.id == "integer"  or element.id == "ref" or element.id == "parent":
            return
        elif(element.id == "this"):
            element.claferSort = self.claferStack[-1]
        else:
            if(not element.id in self.cfr.cfr_sorts):
                #local variable decl
                return
            element.claferSort = self.cfr.cfr_sorts[element.id]
    
    
            
    
    
    
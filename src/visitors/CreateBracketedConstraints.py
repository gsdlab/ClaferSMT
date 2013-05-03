'''
Created on Mar 26, 2013

@author: ezulkosk
'''

from constraints import BracketedConstraint
from visitors import VisitorTemplate
import visitors.Visitor

inConstraint = False #true if beneath a constraint node
currentConstraint = None #holds the constraint currently being traversed


class CreateBracketedConstraints(VisitorTemplate.VisitorTemplate):
    '''
    :var CreateBracketedConstraints.currentConstraint: (:mod:`~constraints.BracketedConstraint`) Holds the constraint currently being traversed. 
    :var CreateBracketedConstraints.inConstraint: (bool) True if the traversal is currently within a constraint.
    :var claferStack: ([:mod:`~common.ClaferSort`]) Stack of clafers used primarily for debugging.
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Converts Clafer constraints to z3 syntax,
    adds constraints to z3.z3_constraints
    field.
    '''
    
    #stack of clafers, used to add comments to constraints
    claferStack = []
    
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        VisitorTemplate.VisitorTemplate.__init__(self)
        CreateBracketedConstraints.inConstraint = False
        self.z3 = z3
    
    def claferVisit(self, element):
        self.claferStack.append(self.z3.z3_sorts[element.uid].id)
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.claferStack.pop()
    
    def claferidVisit(self, element):
        #if element.moduleName=="" :
        #    prettyPrint("Module Name=\"\"")
        #else:
        #    prettyPrint("Module Name=" + element.moduleName)
        if(CreateBracketedConstraints.inConstraint):
            CreateBracketedConstraints.currentConstraint.addArg(element.id)
        #prettyPrint("isTop=" + str(element.isTop))
    
    def constraintVisit(self, element):
        '''
        this class is basically ruined currently
        ''' 
        CreateBracketedConstraints.inConstraint = True
        if(not self.claferStack):
            CreateBracketedConstraints.currentConstraint = BracketedConstraint.BracketedConstraint("TopLevelConstraint")
        else:
            CreateBracketedConstraints.currentConstraint = BracketedConstraint.BracketedConstraint("BracketedConstraint:" + self.claferStack[-1])
        visitors.Visitor.visit(self, element.exp)
        self.z3.addConstraint(CreateBracketedConstraints.currentConstraint)
        CreateBracketedConstraints.currentConstraint.endProcessing()
        CreateBracketedConstraints.currentConstraint = None
        CreateBracketedConstraints.inConstraint = False
    
    def funexpVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(CreateBracketedConstraints.inConstraint):
            CreateBracketedConstraints.currentConstraint.addOperator(element.operation)
            
    
    def localdeclarationVisit(self, element):
        #prettyPrint("element="+element.element)
        pass
    
    def integerliteralVisit(self, element):
        if(CreateBracketedConstraints.inConstraint):
            CreateBracketedConstraints.currentConstraint.addArg(element.value)
        
    def doubleliteralVisit(self, element):
        return element
        
    def stringliteralVisit(self, element):
        return element
    
    

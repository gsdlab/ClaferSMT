'''
Created on Mar 26, 2013

@author: ezulkosk
'''
from common import Constraint, Common
from visitors import VisitorTemplate
import visitors.Visitor

inConstraint = False #true if beneath a constraint node
currentConstraint = None #holds the constraint currently being traversed

class CreateConstraints(VisitorTemplate.VisitorTemplate):
    '''
    converts constraints to z3 syntax,
    adds constraints to z3.z3_constraints
    fields:
        z3(Z3Instance): the Z3Instance object
    '''
    
    #stack of clafers, used to add comments to constraints
    claferStack = []
    
    def __init__(self, z3instance):
        VisitorTemplate.VisitorTemplate.__init__(self)
        self.z3 = z3instance
    
    def claferVisit(self, element):
        self.claferStack.append(element.sortID)
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.claferStack.pop()
    
    def constraintVisit(self, element):
        CreateConstraints.inConstraint = True
        if(not self.claferStack):
            CreateConstraints.currentConstraint = Constraint.Constraint("TopLevelConstraint")
        else:
            CreateConstraints.currentConstraint = Constraint.Constraint("Constraint:" + self.claferStack[-1])
        visitors.Visitor.visit(self, element.exp)
        self.z3.addConstraint(CreateConstraints.currentConstraint)
        CreateConstraints.currentConstraint.endProcessing()
        CreateConstraints.currentConstraint = None
        CreateConstraints.inConstraint = False
    
    def funexpVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(CreateConstraints.inConstraint):
            CreateConstraints.currentConstraint.addOperator(element.operation)
            
    
    def localdeclarationVisit(self, element):
        #prettyPrint("element="+element.element)
        pass
    
    def integerliteralVisit(self, element):
        if(CreateConstraints.inConstraint):
            CreateConstraints.currentConstraint.addArg(element.value)
        
    def doubleliteralVisit(self, element):
        return element
        
    def stringliteralVisit(self, element):
        return element
    
    

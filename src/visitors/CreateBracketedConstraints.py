'''
Created on Mar 26, 2013

@author: ezulkosk
'''
from common import Common
from constraints import BracketedConstraint
from visitors import VisitorTemplate
import visitors.Visitor

inConstraint = False #true if beneath a constraint node
currentConstraint = None #holds the constraint currently being traversed


class CreateBracketedConstraints(VisitorTemplate.VisitorTemplate):
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
        CreateBracketedConstraints.inConstraint = False
        self.z3 = z3instance
    
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

    '''
    this class is basically ruined currently
    '''    
    def constraintVisit(self, element):
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
    
    

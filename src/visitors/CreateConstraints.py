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
    adds constraints to common.Common.z3_constraints
    uses:
        common.Common.addConstraint(constraint)
    '''
    
    def __init__(self):
        VisitorTemplate.VisitorTemplate.__init__(self)
    
    def claferVisit(self, element):
        #prettyPrint("ident="+element.ident)
        #prettyPrint("abstract="+str(element.isAbstract))
        #print("card="+str(element.card))
        #prettyPrint("gcard="+str(element.gcard))
        #prettyPrint("glcard="+str(element.glCard))
        #prettyPrint("uid="+str(element.uid))
        #prettyPrint("supers{")
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def claferidVisit(self, element):
        #if element.moduleName=="" :
        #    prettyPrint("Module Name=\"\"")
        #else:
        #    prettyPrint("Module Name=" + element.moduleName)
        #prettyPrint("id=" + element.id)
        #prettyPrint("isTop=" + str(element.isTop))
        pass
    
    def constraintVisit(self, element):
        CreateConstraints.inConstraint = True
        CreateConstraints.currentConstraint = Constraint.Constraint()
        visitors.Visitor.visit(self, element.exp)
        Common.addConstraint(CreateConstraints.currentConstraint)
        CreateConstraints.currentConstraint.endProcessing()
        CreateConstraints.currentConstraint = None
        CreateConstraints.inConstraint = False
    
    def declarationVisit(self, element):
        #prettyPrint("isDisjunct="+ str(element.isDisjunct))
        for i in element.localDeclarations:
            visitors.Visitor.visit(self, i)
        visitors.Visitor.visit(self, element.body)
    
    def declpexpVisit(self, element):
        #prettyPrint("quantifier="+ str(element.quantifier))
        visitors.Visitor.visit(self, element.declaration)
        visitors.Visitor.visit(self, element.bodyParentExp)
        
    def expVisit(self, element):
        #prettyPrint("expType=" + str(element.expType))
        #prettyPrint("type=" + str(element.type))
        #if str(element.parentId)=="" :
        #    prettyPrint("parentId=\"\"")
        #else:
        #    prettyPrint("parentId=" + str(element.parentId))
        #prettyPrint("pos=" + str(element.pos[0])+str(element.pos[1]))
        #prettyPrint("iExpType="+str(element.iExpType))
        for i in element.iExp:
            visitors.Visitor.visit(self, i)
    
    
    def funexpVisit(self, element):
        #prettyPrint("operation=" + str(element.operation))
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(CreateConstraints.inConstraint):
            CreateConstraints.currentConstraint.addOperator(element.operation)
            
    
    def gcardVisit(self, element):
        #prettyPrint("isKeyword=" + str(element.isKeyword))
        #prettyPrint("interval=" + str(element.interval))
        pass
    
    def goalVisit(self, element):
        #prettyPrint("isMaximize=" + str(element.isMaximize))
        visitors.Visitor.visit(self, element.exp)
    
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
    
    def noneVisit(self):
        #prettyPrint("None")
        pass
    

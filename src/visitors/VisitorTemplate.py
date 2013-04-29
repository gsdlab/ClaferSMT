'''
Created on Mar 26, 2013

@author: ezulkosk
'''
import visitors.Visitor

class VisitorTemplate(object):
    
    __TAB__ = "  "
    level = 0
    
    def __init__(self):
        pass
    
    def claferVisit(self, element):
        #prettyPrint("ident="+element.ident)
        #prettyPrint("absract="+str(element.isAbstract))
        #prettyPrint("card="+str(element.card))
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
        #prettyPrint("isHard=" + str(element.isHard))
        visitors.Visitor.visit(self, element.exp)
    
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
    
    def moduleVisit(self, element):
        #print(element.elements[0])
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def supersVisit(self, element):
        #prettyPrint("isOverlapping="+ str(element.isOverlapping))
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def integerliteralVisit(self, element):
        #prettyPrint(str(element.value))
        pass
        
    def doubleliteralVisit(self, element):
        #prettyPrint(str(element.value))
        pass
        
    def stringliteralVisit(self, element):
        #prettyPrint(element.value)
        pass
    
    def noneVisit(self):
        #prettyPrint("None")
        pass
    

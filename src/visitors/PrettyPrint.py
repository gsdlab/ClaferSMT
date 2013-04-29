'''
Created on Mar 26, 2013

@author: ezulkosk
'''
import visitors.Visitor

def prettyPrint(s):
    print(PrettyPrint.__TAB__ * PrettyPrint.level + s)

class PrettyPrint(object):
    
    __TAB__ = "  "
    level = 0
    
    def __init__(self):
        pass
    
    def claferVisit(self, element):
        prettyPrint("ident="+element.ident)
        prettyPrint("abstract="+str(element.isAbstract))
        prettyPrint("card="+str(element.card))
        prettyPrint("gcard="+str(element.gcard))
        prettyPrint("glcard="+str(element.glCard))
        prettyPrint("uid="+str(element.uid))
        prettyPrint("supers{")
        visitors.Visitor.visit(self,element.supers)
        prettyPrint("}")
        prettyPrint("elements{")
        self.inc()
        for i in element.elements:
            prettyPrint("CLAFER:")
            visitors.Visitor.visit(self, i)
            prettyPrint("END")
        self.dec()
        prettyPrint("}")
    
    def claferidVisit(self, element):
        if element.moduleName=="" :
            prettyPrint("Module Name=\"\"")
        else:
            prettyPrint("Module Name=" + element.moduleName)
        prettyPrint("id=" + element.id)
        prettyPrint("isTop=" + str(element.isTop))
    
    def constraintVisit(self, element):
        prettyPrint("isHard=" + str(element.isHard))
        prettyPrint("exp{")
        self.inc()
        visitors.Visitor.visit(self, element.exp)
        self.dec()
        prettyPrint("}")
    
    def declarationVisit(self, element):
        prettyPrint("isDisjunct="+ str(element.isDisjunct))
        prettyPrint("LocalDeclarations{")
        self.inc()
        for i in element.localDeclarations:
            prettyPrint("ELEMENT:")
            visitors.Visitor.visit(self, i)
            prettyPrint("END")
        self.dec()
        prettyPrint("}")
        prettyPrint("body{")
        self.inc()
        visitors.Visitor.visit(self, element.body)
        self.dec()
        prettyPrint("}")
    
    def declpexpVisit(self, element):
        prettyPrint("quantifier="+ str(element.quantifier))
        prettyPrint("declaration{")
        self.inc()
        visitors.Visitor.visit(self, element.declaration)
        self.dec()
        prettyPrint("}")
        prettyPrint("bodyParentExp{")
        self.inc()
        visitors.Visitor.visit(self, element.bodyParentExp)
        self.dec()
        prettyPrint("}")
        
    #expType, my_type, parentId, pos, iExpType ,iExp
    def expVisit(self, element):
        prettyPrint("expType=" + str(element.expType))
        prettyPrint("type=" + str(element.type))
        if str(element.parentId)=="" :
            prettyPrint("parentId=\"\"")
        else:
            prettyPrint("parentId=" + str(element.parentId))
        prettyPrint("pos=" + str(element.pos[0])+str(element.pos[1]))
        prettyPrint("iExpType="+str(element.iExpType))
        prettyPrint("iExp{")
        self.inc()
        for i in element.iExp:
            prettyPrint("EXPRESSION:")
            visitors.Visitor.visit(self, i)
            prettyPrint("END")
        self.dec()
        prettyPrint("}")
    
    
    def funexpVisit(self, element):
        prettyPrint("operation=" + str(element.operation))
        prettyPrint("elements{")
        self.inc()
        for i in element.elements:
            prettyPrint("FUNEXP:")
            visitors.Visitor.visit(self, i)
            prettyPrint("END")
        self.dec()
        prettyPrint("}")
    
    def gcardVisit(self, element):
        prettyPrint("isKeyword=" + str(element.isKeyword))
        prettyPrint("interval=" + str(element.interval))
    
    def goalVisit(self, element):
        prettyPrint("isMaximize=" + str(element.isMaximize))
        prettyPrint("exp{")
        self.inc()
        visitors.Visitor.visit(self, element.exp)
        self.dec()
        prettyPrint("}")
    
    def localdeclarationVisit(self, element):
        prettyPrint("element="+element.element)
    
    def moduleVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def supersVisit(self, element):
        prettyPrint("isOverlapping="+ str(element.isOverlapping))
        prettyPrint("elements{")
        self.inc()
        for i in element.elements:
            prettyPrint("SUPERS:")
            visitors.Visitor.visit(self, i)
            prettyPrint("END")
        self.dec()
        prettyPrint("}")
    
    def integerliteralVisit(self, element):
        prettyPrint(str(element.value))
        
    def doubleliteralVisit(self, element):
        prettyPrint(str(element.value))
        
    def stringliteralVisit(self, element):
        prettyPrint(element.value)
        
    def noneVisit(self):
        prettyPrint("None")
    
    def inc(self):
        PrettyPrint.level = PrettyPrint.level+1
        
    def dec(self):
        PrettyPrint.level = PrettyPrint.level-1
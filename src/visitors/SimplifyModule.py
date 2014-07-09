'''
Created on Mar 16, 2014

@author: ezulkosk
'''
import visitors.Visitor

class SimplifyModule(object):
    '''
    *see:* :class:`visitors.Visitor`
    '''
    def __init__(self):
        pass
    
    def claferVisit(self, element):
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def claferidVisit(self, element):
        pass
    
    def constraintVisit(self, element):
        visitors.Visitor.visit(self, element.exp)
    
    def declarationVisit(self, element):
        for i in element.localDeclarations:
            visitors.Visitor.visit(self, i)
        visitors.Visitor.visit(self, element.body)
    
    def declpexpVisit(self, element):
        visitors.Visitor.visit(self, element.declaration)
        visitors.Visitor.visit(self, element.bodyParentExp)
        
    def expVisit(self, element):
        for i in element.iExp:
            visitors.Visitor.visit(self, i)
    
    
    def funexpVisit(self, element):
        #print(element.operation)
        for i in element.elements:
            print(i)
            visitors.Visitor.visit(self, i)
    
    def gcardVisit(self, element):
        pass
    
    def goalVisit(self, element):
        visitors.Visitor.visit(self, element.exp)
    
    def localdeclarationVisit(self, element):
        pass
    
    def moduleVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def supersVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def integerliteralVisit(self, element):
        pass
        
    def realliteralVisit(self, element):
        pass
        
    def stringliteralVisit(self, element):
        pass
    
    def noneVisit(self):
        pass
    
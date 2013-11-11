'''
Created on Nov 7, 2013

@author: ezulkosk
'''
from common import Options
from structures.ClaferSort import ClaferSort
from visitors import VisitorTemplate, Visitor, CreateSorts
import visitors

def run():
    module = Options.MODULE
    
    ''' Get the number of clafers in the model. '''
    numClafersVisitor = GetNumClafers()
    Visitor.visit(numClafersVisitor, module)
    numClafers = numClafersVisitor.count
    print(numClafers)
    
    ''' Get the number of constraints in the model. '''
    numConstraintsVisitor = GetNumBracketedConstraints()
    Visitor.visit(numConstraintsVisitor, module)
    numConstraints = numConstraintsVisitor.count
    print(numConstraints)
    
    ''' Get stats about constraints. '''
    constraintsStatsVisitor = GetBracketedConstraintsStats()
    Visitor.visit(constraintsStatsVisitor, module)
    counts = sorted(constraintsStatsVisitor.counts)
    print(str(counts))
    
    

class GetNumClafers(VisitorTemplate.VisitorTemplate):
    
    def __init__(self):
        self.count = 0
    
    def claferVisit(self, element):
        self.count = self.count + 1
        for i in element.elements:
            visitors.Visitor.visit(self, i)
            
            
class GetNumBracketedConstraints(VisitorTemplate.VisitorTemplate):
    
    def __init__(self):
        self.count = 0
    
    def constraintVisit(self, element):
        self.count = self.count + 1
        visitors.Visitor.visit(self, element.exp)
            

class GetBracketedConstraintsStats(VisitorTemplate.VisitorTemplate):
    
    def __init__(self):
        self.counts = []
        self.currCount = 0
    
    def constraintVisit(self, element):
        self.inConstraint = True
        visitors.Visitor.visit(self, element.exp)
        self.inConstraint = False
        self.counts.append(self.currCount)
        self.currCount = 0
        
    def funexpVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(self.inConstraint):
            self.currCount = self.currCount + 1
            
    
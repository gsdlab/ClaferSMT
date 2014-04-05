'''
Created on Nov 7, 2013

@author: ezulkosk
'''
from common import Options
from structures.ClaferSort import ClaferSort
from visitors import VisitorTemplate, Visitor, CreateSorts
import visitors

def run(z3inst, module):
    ''' Get the number of clafers in the model. '''
    
    numClafers = getNumClafers(z3inst)
    numBracketedConstraints = getNumBracketedConstraints(z3inst)
    numBracketedConstraintOperatorsList = getNumBracketedConstraintsOperators(module)
    numTopLevelClafers = getNumTopLevelClafers(z3inst)
    (isObjectives, numObjectives) = getObjectiveStats(z3inst)
    (maxCard, maxBoundedGroupCard) = getMaxCards(z3inst)
    maxDepth = getMaxDepth(z3inst)
    numXors = getNumXors(z3inst)
    
    
    print("Num Clafers: " + str(numClafers))
    print("Num Bracketed Constraints: " + str(numBracketedConstraints))
    print("Num Bracketed Cosntraint Operators: " + str(numBracketedConstraintOperatorsList))
    print("Num Top Level Clafers: " + str(numTopLevelClafers))
    print("Objectives?: " + str(isObjectives))
    print("Num Objectives: " + str(numObjectives))
    print("Max Card: " + str(maxCard))
    print("Max Bounded Group Card: " + str(maxBoundedGroupCard))
    print("Max Depth: " + str(maxDepth))
    print("Num Xors: " + str(numXors))
    
    
''' ---------------------------------------------------------------'''    
    
def getNumTopLevelClafers(z3inst):
    tops = 0
    for i in z3inst.z3_sorts.values():
        if i.isTopLevel:
            tops = tops + 1
    return tops
    
''' ---------------------------------------------------------------'''    
    
def getMaxDepth(z3inst):
    maxDepth = 0
    for i in z3inst.z3_sorts.values():
        if len(i.parentStack) > maxDepth:
            maxDepth = len(i.parentStack)
    return maxDepth
    
''' ---------------------------------------------------------------'''    

def getNumXors(z3inst):
    numXors = 0
    for i in z3inst.z3_sorts.values():
        if i.lowerGCard == 1 and i.upperGCard == 1:
            numXors = numXors + 1
    return numXors

''' ---------------------------------------------------------------'''    

def getObjectiveStats(z3inst):
    isObjectives = True if z3inst.objectives else False
    numObjectives = len(z3inst.objectives)
    return (isObjectives, numObjectives)

''' ---------------------------------------------------------------'''    

def getMaxCards(z3inst):
    maxCard = -1
    maxBoundedGroupCard = -1
    for i in z3inst.z3_sorts.values():
        if i.upperCardConstraint > maxCard:
            maxCard = i.upperCardConstraint
        if i.upperGCard > maxBoundedGroupCard:
            maxBoundedGroupCard = i.upperGCard
    return (maxCard, maxBoundedGroupCard)

''' ---------------------------------------------------------------'''    

def getNumClafers(z3inst):
    return len(z3inst.z3_sorts)
   
''' ---------------------------------------------------------------'''    
                
def getNumBracketedConstraints(z3inst):
    return len(z3inst.z3_bracketed_constraints)    
    
''' ---------------------------------------------------------------'''    
def getNumBracketedConstraintsOperators(module):
    constraintsStatsVisitor = GetBracketedConstraintsStats()
    Visitor.visit(constraintsStatsVisitor, module)
    counts = sorted(constraintsStatsVisitor.counts)
    return counts

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
            
''' ---------------------------------------------------------------'''            
    
    
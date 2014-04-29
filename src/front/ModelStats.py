'''
Created on Nov 7, 2013

@author: ezulkosk
'''
from common import Options, Common
from common.Common import METRICS_MAXIMIZE, METRICS_MINIMIZE
from structures.ClaferSort import ClaferSort
from visitors import VisitorTemplate, Visitor, CreateSorts
import sys
import visitors

def run(z3inst, parameters=None, non_modelstats=[]):
    stats = []
    if parameters:
        for (parameter,_,_) in parameters:
            if parameter in non_modelstats:
                continue 
            stats.append(getParameter(parameter, z3inst))
        return stats
    else:
        numClafers = getNumClafers(z3inst)
        numBracketedConstraints = getNumBracketedConstraints(z3inst)
        numBracketedConstraintOperatorsList = getNumBracketedConstraintsOperators(z3inst)
        numTopLevelClafers = getNumTopLevelClafers(z3inst)
        (isObjectives, numObjectives) = getObjectiveStats(z3inst)
        (maxCard, maxBoundedGroupCard) = getMaxCards(z3inst)
        maxDepth = getMaxDepth(z3inst)
        numXors = getNumXorGCard(z3inst)
        numOptionalGCard = getNumOptionalGCard(z3inst)
        numOptionalCard = getNumOptionalCard(z3inst)
        numMandatoryCard = getNumMandatoryCard(z3inst)
        
        print("Num Clafers: " + str(numClafers))
        print("Num Bracketed Constraints: " + str(numBracketedConstraints))
        print("Num Bracketed Constraint Operators: " + str(numBracketedConstraintOperatorsList))
        print("Num Top Level Clafers: " + str(numTopLevelClafers))
        print("Objectives?: " + str(isObjectives))
        print("Num Objectives: " + str(numObjectives))
        print("Max Card: " + str(maxCard))
        print("Max Bounded Group Card: " + str(maxBoundedGroupCard))
        print("Max Depth: " + str(maxDepth))
        print("Num Xors GCard: " + str(numXors))
        print("Num Optional GCard: " + str(numOptionalGCard))
        print("Num Optional Card: " + str(numOptionalCard))
        print("Num Mandatory Card: " + str(numMandatoryCard))
    
    
    
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

def getNumXorGCard(z3inst):
    numXors = 0
    for i in z3inst.z3_sorts.values():
        if i.lowerGCard == 1 and i.upperGCard == 1:
            numXors = numXors + 1
    return numXors

def getNumOptionalGCard(z3inst):
    numOpts = 0
    for i in z3inst.z3_sorts.values():
        #print(str(i) + str(i.lowerGCard))
        if i.lowerGCard == 1 and i.upperGCard == -1:
            numOpts = numOpts + 1
    return numOpts

def getNumAnyGCard(z3inst):
    numAnys = 0
    for i in z3inst.z3_sorts.values():
        #print(str(i) + str(i.lowerGCard))
        if i.lowerGCard == 0 and i.upperGCard == -1:
            numAnys = numAnys + 1
    return numAnys


''' ---------------------------------------------------------------''' 

def getNumMandatoryCard(z3inst):
    numMandatory = 0
    for i in z3inst.z3_sorts.values():
        #print(str(i) + str(i.lowerCardConstraint) + " " + str(i.upperCardConstraint))
        if i.lowerCardConstraint == 1 and i.upperCardConstraint == 1:
            numMandatory = numMandatory + 1
    return numMandatory

def getNumOptionalCard(z3inst):
    numOptional = 0
    for i in z3inst.z3_sorts.values():
        #print(str(i) + str(i.lowerGCard))
        if i.lowerCardConstraint == 0 and i.upperCardConstraint == 1:
            numOptional = numOptional + 1
    return numOptional

''' ---------------------------------------------------------------'''    

def getObjectiveStats(z3inst):
    isObjectives = True if z3inst.objectives else False
    numObjectives = len(z3inst.objectives)
    return (isObjectives, numObjectives)

def getNumObjectives(z3inst):
    return len(z3inst.objectives)

def getNumMaximizeObjectives(z3inst):
    numObjectives = 0
    for i in z3inst.objectives:
        (polarity,_) = i
        if polarity == METRICS_MAXIMIZE:
            numObjectives = numObjectives + 1
    return numObjectives

def getNumMinimizeObjectives(z3inst):
    numObjectives = 0
    for i in z3inst.objectives:
        (polarity,_) = i
        if polarity == METRICS_MINIMIZE:
            numObjectives = numObjectives + 1
    return numObjectives

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

def getNumBracketedConstraintsOperators(z3inst):
    module = z3inst.module
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

def getParameter(parameter, z3inst):
    if parameter in parameter_functions.keys():
        function = parameter_functions[parameter]
        return function(z3inst)
    else:
        sys.exit("Unimplimented parameter: " + parameter)
    
parameter_functions = {
                       "numClafers"                : getNumClafers, 
                       "numBracketedConstraints"   : getNumBracketedConstraints,
                       "numMandatoryCards"         : getNumMandatoryCard,
                       "numOptionalCards"          : getNumOptionalCard,
                       "numXorGCards"              : getNumXorGCard,
                       "numOptionalGCards"         : getNumOptionalGCard,
                       "numAnyGCards"              : getNumAnyGCard,
                       "numObjectives"             : getNumObjectives,
                       "numMaximizeObjectives"     : getNumMaximizeObjectives,
                       "numMinimizeObjectives"     : getNumMinimizeObjectives,
                       "maxDepth"                  : getMaxDepth 
                       
                       }
    
    
'''
Created on Mar 26, 2013

@author: ezulkosk
'''

from constraints import BracketedConstraint
from visitors import VisitorTemplate
import itertools
import visitors.Visitor

claferStack = [] #used to determine where the constraint is in the clafer hierarchy
inConstraint = False #true if beneath a constraint node
currentConstraint = None #holds the constraint currently being traversed


class CreateBracketedConstraints(VisitorTemplate.VisitorTemplate):
    '''
    :var self.currentConstraint: (:mod:`~constraints.BracketedConstraint`) Holds the constraint currently being traversed. 
    :var self.inConstraint: (bool) True if the traversal is currently within a constraint.
    :var claferStack: ([:mod:`~common.ClaferSort`]) Stack of clafers used primarily for debugging.
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Converts Clafer constraints to z3 syntax,
    adds constraints to z3.z3_constraints
    field.
    '''
    
    
    def __init__(self, z3):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        VisitorTemplate.VisitorTemplate.__init__(self)
        self.inConstraint = False
        self.currentConstraint = None
        self.z3 = z3
    
    def claferVisit(self, element):
        visitors.Visitor.visit(self,element.supers)
        claferStack.append(self.z3.getSort(element.uid))
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        claferStack.pop()
    
    def claferidVisit(self, element):
        if(self.inConstraint):
            if element.id == "this":
                instances = element.claferSort.maskForThis()
                self.currentConstraint.addArg(([element.claferSort], instances))
                self.currentConstraint.this = element.claferSort
            elif element.id == "ref":
                self.currentConstraint.addArg((["ref"], ["ref"]))
            elif element.id == "parent":
                self.currentConstraint.addArg((["parent"], ["parent"]))
            elif element.claferSort:  
                self.currentConstraint.addArg(([element.claferSort], [element.claferSort.instances[:]]))
            else:
                #localdecl case
                (sort, instances) = self.currentConstraint.locals[element.id]
                self.currentConstraint.addArg(([sort], [instances[:]]))
   
    def constraintVisit(self, element):
        self.inConstraint = True
        self.currentConstraint = BracketedConstraint.BracketedConstraint(self.z3, claferStack)
        visitors.Visitor.visit(self, element.exp)
        self.currentConstraint.endProcessing()
        self.currentConstraint = None
        self.inConstraint = False
    
    def funexpVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(self.inConstraint):
            self.currentConstraint.addOperator(element.operation)
           
    #assume their is only one sort at this time
    def createAllLocalsCombinations(self, locals, sort, isDisjunct):
        ranges = [range(sort.numInstances) for i in locals]
        integer_combinations = itertools.product(*ranges)
        instances = []
        for i in integer_combinations: 
            list_of_ints = list(i)
            if(isDisjunct and (len(set(list_of_ints)) != len(list_of_ints))):
                continue
            instances.append([sort.maskForOne(j) for j in list_of_ints])
        return instances
     
    #handle local declarations (some, all, lone, one, no) 
    #not fully implemented
    def declpexpVisit(self, element):
        #visitors.Visitor.visit(self, element.declaration)
        #needs to be more robust, but need example programs.
        num_args = 0
        if element.declaration:
            sort = element.declaration.body.iExp[0].claferSort
            isDisjunct = element.declaration.isDisjunct
            combinations = self.createAllLocalsCombinations(element.declaration.localDeclarations, sort, isDisjunct)
            for i in range(len(combinations)):
                for j in range(len(combinations[i])):
                    self.currentConstraint.addLocal(element.declaration.localDeclarations[j].element
                                                                      , sort, combinations[i][j])
                visitors.Visitor.visit(self, element.bodyParentExp)
                num_args = num_args + 1 
        else:
            visitors.Visitor.visit(self, element.bodyParentExp)
            num_args = 1
        self.currentConstraint.addQuantifier(element.quantifier, num_args)
    
    def localdeclarationVisit(self, element):
        #prettyPrint("element="+element.element)
        pass
    
    def integerliteralVisit(self, element):
        if(self.inConstraint):
            self.currentConstraint.addArg(([element], [element.value]))
        
    def doubleliteralVisit(self, element):
        return element
        
    def stringliteralVisit(self, element):
        return element
    
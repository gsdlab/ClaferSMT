'''
Created on Mar 26, 2013

@author: ezulkosk
'''

from constraints import BracketedConstraint
from constraints.BracketedConstraint import ExprArg, IntArg
from visitors import VisitorTemplate
from z3 import And
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
                self.currentConstraint.addArg(ExprArg([element.claferSort], [element.claferSort], instances))
                self.currentConstraint.this = element.claferSort
            elif element.id == "ref":
                self.currentConstraint.addArg(ExprArg(["ref"], ["ref"], ["ref"]))
            elif element.id == "parent":
                self.currentConstraint.addArg(ExprArg(["parent"], ["parent"], ["parent"]))
            elif element.claferSort:  
                self.currentConstraint.addArg(ExprArg([element.claferSort], [element.claferSort], [element.claferSort.instances[:]]))
            else:
                #localdecl case
                expr = self.currentConstraint.locals[element.id]
                self.currentConstraint.addArg(expr)
   
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
    def createAllLocalsCombinations(self, localDecls, sort, instances, isDisjunct):
        ranges = [range(sort.numInstances) for i in localDecls]
        newinstances = []
        ifconstraints = []
        for h in instances:
            integer_combinations = itertools.product(*ranges)
            innerinstances = []
            innerIfConstraints = []
            for i in integer_combinations: 
                list_of_ints = list(i)
                if(isDisjunct and (len(set(list_of_ints)) != len(list_of_ints))):
                    continue
                innerinstances.append([[h[j] if j == k  else sort.parentInstances for j in range(len(h))] for k in list_of_ints])
                innerIfConstraints.append(And(*[h[k] != sort.parentInstances for k in list_of_ints]))
            newinstances.append(innerinstances[:])
            ifconstraints.append(innerIfConstraints)
        return (newinstances, ifconstraints)
     
    #handle local declarations (some, all, lone, one, no) 
    #not fully implemented
    def declpexpVisit(self, element):
        #visitors.Visitor.visit(self, element.declaration)
        #needs to be more robust, but need example programs.
        num_args = 0
        if element.declaration:
            #sort = []#element.declaration.body.iExp[0].claferSort
            visitors.Visitor.visit(self, element.declaration.body.iExp[0])
            #([sort], instances) = self.currentConstraint.stack.pop()
            arg = self.currentConstraint.stack.pop()
            isDisjunct = element.declaration.isDisjunct
            (combinations, ifconstraints) = self.createAllLocalsCombinations(element.declaration.localDeclarations, 
                                                                             arg.instanceSorts[0], 
                                                                             arg.instances, 
                                                                             isDisjunct)
            num_args = len(combinations[0])
            num_quantifiers = len(combinations)
            for i in combinations:
                for j in i:
                    for k in range(len(j)):
                        self.currentConstraint.addLocal(element.declaration.localDeclarations[k].element
                                                                        , ExprArg(arg.joinSorts[:]
                                                                                  , arg.instanceSorts[:]
                                                                                  , [j[k]]))
                    visitors.Visitor.visit(self, element.bodyParentExp)

        else:
            visitors.Visitor.visit(self, element.bodyParentExp)
            num_args = 1
            num_quantifiers = 1
            ifconstraints = []
        self.currentConstraint.addQuantifier(element.quantifier, num_args,num_quantifiers, ifconstraints)
    
    def localdeclarationVisit(self, element):
        pass
    
    def integerliteralVisit(self, element):
        if(self.inConstraint):
            self.currentConstraint.addArg(IntArg([element.value]))
        
    def doubleliteralVisit(self, element):
        return element
        
    def stringliteralVisit(self, element):
        return element
    
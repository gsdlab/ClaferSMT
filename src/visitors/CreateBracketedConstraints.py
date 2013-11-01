'''
Created on Mar 26, 2013

@author: ezulkosk
'''

from common import Common
from common.Common import mAnd
from constraints import BracketedConstraint
from structures.ExprArg import ExprArg, Mask, BoolArg, IntArg
from visitors import VisitorTemplate
import itertools
import visitors.Visitor


claferStack = [] #used to determine where the constraint is in the clafer hierarchy
inConstraint = False #true if within a constraint
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
    
    def __init__(self, z3, inConstraint=False):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        VisitorTemplate.VisitorTemplate.__init__(self)
        self.inConstraint = inConstraint
        self.currentConstraint = None
        self.z3 = z3
    
    def isomorphismVisit(self, element):
        '''
        :param element: The isomorphism constraint to be added to the solver. 
        :type element: :class:`~ast.FunExp`
        
        Mild hack. Only used when generating isomorphism constraints. Used to circumvent 
        fully creating a proper clafer constraint.
        '''
        self.inConstraint = True
        self.currentConstraint = BracketedConstraint.BracketedConstraint(self.z3, [])
        self.funexpVisit(element)
        self.currentConstraint.endProcessing()
        self.currentConstraint = None
        self.inConstraint = False
    
    def claferVisit(self, element):
        visitors.Visitor.visit(self,element.supers)
        claferStack.append(self.z3.getSort(element.uid))
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        claferStack.pop()
    
    def claferidVisit(self, element):
        if(self.inConstraint):
            if element.id == "this":
                exprArgList = []
                for i in range(element.claferSort.numInstances):
                    exprArgList.append(ExprArg([(element.claferSort, Mask(element.claferSort, [i]))]))
                self.currentConstraint.addArg(exprArgList)
            elif element.id == "ref":
                self.currentConstraint.addArg([ExprArg(["ref"])])
            elif element.id == "parent":
                self.currentConstraint.addArg([ExprArg(["parent"])])
            elif element.claferSort:  
                self.currentConstraint.addArg([ExprArg([(element.claferSort, 
                                                        Mask(element.claferSort, [i for i in range(element.claferSort.numInstances)]))])])
            else:
                #localdecl case
                expr = self.currentConstraint.locals[element.id]
                expr = [expr[i].clone() for i in range(len(expr))]
                self.currentConstraint.addArg(expr)
   
    def constraintVisit(self, element):
        self.inConstraint = True
        self.currentConstraint = BracketedConstraint.BracketedConstraint(self.z3, claferStack)
        visitors.Visitor.visit(self, element.exp)
        self.currentConstraint.endProcessing()
        self.currentConstraint = None
        self.inConstraint = False
    
    def funexpVisit(self, element):
        if element.operation =="in":
            Common.BREAK = True
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(self.inConstraint):
            self.currentConstraint.addOperator(element.operation)
        if element.operation =="in":
            Common.BREAK = False    
           
    #assume their is only one sort in the decl at this time, which is true of my old version of clafer
    def createAllLocalsCombinations(self, localDecls, exprArg, isDisjunct):
        (sort, mask) = exprArg.getInstanceSort(0)
        ranges = [mask.keys() for i in localDecls]
        localInstances = []
        ifConstraints = []
        
        integer_combinations = itertools.product(*ranges)
        for i in integer_combinations: 
            list_of_ints = list(i)
            set_of_ints = set(list_of_ints)
            if isDisjunct and (len(set_of_ints) != len(list_of_ints)):
                continue
            localInstances.append([ExprArg([(sort, Mask(sort, [list_of_ints[j]]))]
                                           ) for j in range(len(list_of_ints))])
            ifConstraints.append(mAnd(*[sort.isOn(mask.get(j)) for j in list_of_ints]))
            
        return (localInstances, ifConstraints)
     
    #handle local declarations (some, all, lone, one, no) 
    #not fully implemented
    def declpexpVisit(self, element):
        num_args = 0
        if element.declaration:
            visitors.Visitor.visit(self, element.declaration.body.iExp[0])
            arg = self.currentConstraint.stack.pop()
            isDisjunct = element.declaration.isDisjunct
            #XXX
            (combinations, ifconstraints) = self.createAllLocalsCombinations(element.declaration.localDeclarations, 
                                                                             arg[0],  
                                                                             isDisjunct)
            if len(combinations) == 0:
                if element.quantifier == "Some":
                    self.currentConstraint.stack.append([BoolArg([False])])
                elif element.quantifier == "All":
                    self.currentConstraint.stack.append([BoolArg([True])])
                return
            num_args = len(combinations[0])
            num_combinations = len(combinations)
            for i in combinations:
                for j in range(num_args):
                    self.currentConstraint.addLocal(element.declaration.localDeclarations[j].element, [i[j]])
                visitors.Visitor.visit(self, element.bodyParentExp)

        else:
            visitors.Visitor.visit(self, element.bodyParentExp)
            num_args = 1
            num_combinations = 1
            ifconstraints = []
        
        self.currentConstraint.addQuantifier(element.quantifier, num_args, num_combinations, ifconstraints)
    
    def localdeclarationVisit(self, element):
        pass
    
    def integerliteralVisit(self, element):
        if(self.inConstraint):
            self.currentConstraint.addArg([IntArg([element.value])])
        
    def doubleliteralVisit(self, element):
        return element
        
    def stringliteralVisit(self, element):
        #TODO stubbed
        self.currentConstraint.addArg([IntArg([0])])#element.value])])
    
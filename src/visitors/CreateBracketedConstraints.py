'''
Created on Mar 26, 2013

@author: ezulkosk
'''

from common import Common, Options, SMTLib
from common.Common import mAnd
from common.Options import debug_print
from constraints import BracketedConstraint
from structures.ClaferSort import PrimitiveType
from structures.ExprArg import ExprArg, BoolArg, IntArg, RealArg, \
    StringArg, PrimitiveArg
from visitors import VisitorTemplate
from visitors.CheckFunctionSymmetry import CheckFunctionSymmetry
import itertools
import sys
import visitors.Visitor


claferStack = []  # used to determine where the constraint is in the clafer hierarchy
inConstraint = False  # true if within a constraint
currentConstraint = None  # holds the constraint currently being traversed


class CreateBracketedConstraints(VisitorTemplate.VisitorTemplate):
    '''
    :var self.currentConstraint: (:mod:`~constraints.BracketedConstraint`) Holds the constraint currently being traversed. 
    :var self.inConstraint: (bool) True if the traversal is currently within a constraint.
    :var claferStack: ([:mod:`~common.ClaferSort`]) Stack of clafers used primarily for debugging.
    :var cfr: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Converts Clafer constraints to cfr syntax,
    adds constraints to cfr.z3_constraints
    field.
    '''
    
    def __init__(self, cfr, inConstraint=False):
        '''
        :param cfr: The Clafer model.
        :type cfr: :class:`~common.ClaferModel`
        '''
        VisitorTemplate.VisitorTemplate.__init__(self)
        self.inConstraint = inConstraint
        self.currentConstraint = None
        self.cfr = cfr
        self.BRACKETEDCONSCOUNT = 1
    
    def generatedConstraintVisit(self, element):
        '''
        :param element: The isomorphism constraint to be added to the solver. 
        :type element: :class:`~ast.FunExp`
        
        Mild hack. Only used when generating isomorphism constraints. Used to circumvent 
        fully creating a proper clafer constraint.
        '''
        self.inConstraint = True
        self.currentConstraint = BracketedConstraint.BracketedConstraint(self.cfr, [])
        self.funexpVisit(element)
        #return self.currentConstraint.stack.pop()
        self.currentConstraint.endProcessing(addToZ3=False)
        return self.currentConstraint.constraints.pop()
        
    
    def objectiveVisit(self, element):
        '''
        :param element: The goal constraint to be added to the list of objectives. 
        :type element: :class:`~ast.FunExp`
        
        Only used when generating goal constraints. Used to circumvent 
        fully creating a proper clafer constraint.
        '''
        self.inConstraint = True
        self.currentConstraint = BracketedConstraint.BracketedConstraint(self.cfr, element, [])
        visitors.Visitor.visit(self, element)
        #obtain the first element on the top of the stack (there should only be one anyway)
        return self.currentConstraint.stack[0]
    
    
    def claferVisit(self, element):
        if not self.cfr.isUsed(str(element)):
            return 
        visitors.Visitor.visit(self, element.supers)
        claferStack.append(self.cfr.getSort(element.uid))
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        claferStack.pop()
    
    def claferidVisit(self, element):
        if(self.inConstraint):
            if element.id == "this":
                exprArgList = []
                for i in range(element.claferSort.numInstances):
                    exprArg = ExprArg(instances={}, nonsupered=True)
                    exprArg.addBasedOnPolarity(element.claferSort, i, element.claferSort.isOn(i))
                    exprArgList.append(exprArg)
                                                #[(element.claferSort, Mask(element.claferSort, [i]))]))
                self.currentConstraint.addArg(exprArgList)
            elif element.id == "ref":
                self.currentConstraint.addArg([PrimitiveArg("ref")])
            elif element.id == "parent":
                self.currentConstraint.addArg([PrimitiveArg("parent")])
            elif element.claferSort:  
                exprArg = ExprArg(instances={}, nonsupered=True)
                for i in range(element.claferSort.numInstances):
                    exprArg.addBasedOnPolarity(element.claferSort, i, element.claferSort.isOn(i))
                self.currentConstraint.addArg([exprArg])
                                                        #Mask(element.claferSort, [i for i in range(element.claferSort.numInstances)]))])])
            else:
                # localdecl case
                expr = self.currentConstraint.locals[element.id]
                # expr = [expr[i].clone() for i in range(len(expr))]
                self.currentConstraint.addArg(expr)
   
    def constraintVisit(self, element):
        self.inConstraint = True
        debug_print(self.BRACKETEDCONSCOUNT)
        self.BRACKETEDCONSCOUNT = self.BRACKETEDCONSCOUNT + 1
        self.currentConstraint = BracketedConstraint.BracketedConstraint(self.cfr, element, claferStack)
        visitors.Visitor.visit(self, element.exp)
        self.currentConstraint.endProcessing()
        self.currentConstraint = None
        self.inConstraint = False
    
    def funexpVisit(self, element):
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(self.inConstraint):
            self.currentConstraint.addOperator(element.operation)   
           
    # assume there is only one sort in the decl at this time, ok for now
    def createAllLocalsCombinations(self, localDecls, exprArg, isDisjunct, isSymmetric):
        instances = exprArg.getInstances()
        my_range = list(instances.keys())
        integer_combinations = itertools.permutations(my_range, len(localDecls))
        
        localInstances = []
        ifConstraints = []
        
        
        for i in integer_combinations: 
            sys.exit("TODO local combos")
            list_of_ints = list(i)
            set_of_ints = set(list_of_ints)
            if isDisjunct and (len(set_of_ints) != len(list_of_ints)):
                continue
            localInstances.append([ExprArg([(sort, Mask(sort, [list_of_ints[j]], nonsupered=True))]
                                           ) for j in range(len(list_of_ints))])
            ifConstraints.append(mAnd(*[sort.isOn(mask.get(j)) for j in list_of_ints]))
            
        return (localInstances, ifConstraints)
     
    # handle local declarations (some, all, lone, one, no) 
    # not fully implemented
    def declpexpVisit(self, element):
        if Options.BREAK_QUANTIFIER_SYMMETRY:
            sys.exit("BREAK_QUANTIFIER_SYMMETRY still unimplemented.")
            symmetryChecker = CheckFunctionSymmetry(self.cfr)
            visitors.Visitor.visit(symmetryChecker, element.bodyParentExp)
            isSymmetric = symmetryChecker.isSymmetric
            # print(symmetryChecker.isSymmetric)
        else:
            isSymmetric = False
        num_args = 0
        if element.declaration:
             
            visitors.Visitor.visit(self, element.declaration.body.iExp[0])
            if not self.currentConstraint.stack:
                return
            arg = self.currentConstraint.stack.pop()
            isDisjunct = element.declaration.isDisjunct
            for i in range(len(arg)):
                (combinations, ifconstraints) = self.createAllLocalsCombinations(element.declaration.localDeclarations,
                                                                                 arg[i],
                                                                                 isDisjunct,
                                                                                 isSymmetric)
                if len(combinations) == 0:
                    if element.quantifier == "Some":
                        self.currentConstraint.stack.append([BoolArg([SMTLib.SMT_Bool(False)])])
                    elif element.quantifier == "All":
                        self.currentConstraint.stack.append([BoolArg([SMTLib.SMT_Bool(True)])])
                    return
                num_args = len(combinations[0])
                num_combinations = len(combinations)
                for i in combinations:
                    for j in range(num_args):
                            self.currentConstraint.addLocal(element.declaration.localDeclarations[j].element, [i[j]])
                    visitors.Visitor.visit(self, element.bodyParentExp)
                self.currentConstraint.addQuantifier(element.quantifier, num_args, num_combinations, ifconstraints)
            exprArgList = []
            for i in range(len(arg)):
                exprArgList.insert(0, self.currentConstraint.stack.pop()[0])
            self.currentConstraint.addArg(exprArgList)
        else:
            visitors.Visitor.visit(self, element.bodyParentExp)
            num_args = 1
            num_combinations = 1
            ifconstraints = []
            exprList = self.currentConstraint.stack.pop()
            exprArgList = []
            for i in exprList:
                self.currentConstraint.stack.append([i])
                self.currentConstraint.addQuantifier(element.quantifier, num_args, num_combinations, ifconstraints)
                exprArgList.append(self.currentConstraint.stack.pop()[0])
            self.currentConstraint.addArg(exprArgList)
    
    def localdeclarationVisit(self, element):
        pass
    
    def integerliteralVisit(self, element):
        if(self.inConstraint):
            self.currentConstraint.addArg([IntArg(SMTLib.SMT_IntConst(element.value))])
        
    def realliteralVisit(self, element):
        if(self.inConstraint):
            self.currentConstraint.addArg([RealArg([SMTLib.SMT_RealConst(element.value)])])
        
    def stringliteralVisit(self, element):
        stringID = Common.STRCONS_SUB + str(Common.getStringUID())
        Common.string_map[stringID] = element.value
        self.currentConstraint.addArg([StringArg([SMTLib.SMT_Int(stringID)])])  # element.value])])
    

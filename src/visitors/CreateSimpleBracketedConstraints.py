'''
Created on Mar 26, 2013

@author: ezulkosk
'''

from common import Common, Options, SMTLib
from common.Common import mAnd
from common.Options import debug_print
from constraints import BracketedConstraint
from constraints.operations import Boolean, Numeric, Set, Join, String
from structures.ClaferSort import PrimitiveType
from structures.ExprArg import ExprArg, BoolArg, IntArg, PrimitiveArg
from visitors import VisitorTemplate
from visitors.CheckFunctionSymmetry import CheckFunctionSymmetry
import itertools
import sys
import visitors.Visitor


ValidOpsMap = {
                           "&&"          : (2, Boolean.op_and),
                           "="           : (2, Set.op_eq),
                           "in"          : (2, Set.op_in),
                           "++"          : (2, Set.op_union),
                           "--"          : (2, Set.op_difference),
                           "&"           : (2, Set.op_intersection),
                           "."           : (2, Join.op_join)
              }

class CreateSimpleBracketedConstraints(VisitorTemplate.VisitorTemplate):
    
    def __init__(self, cfr, inConstraint=False):
        self.claferStack = []  # used to determine where the constraint is in the clafer hierarchy
        self.constraints = [] 
        self.inConstraint = False  # true if within a constraint
        self.currentConstraint = None  # holds the constraint currently being traversed
        self.setEqualityConstraints = []
        self.otherConstraints = []
        self.good = True
        self.inConstraint = inConstraint
        self.currentConstraint = None
        self.argStack = []
        self.stringStack = []
        self.opStack = []
        self.cfr = cfr
    
    def claferVisit(self, element):
        if not self.cfr.isUsed(str(element)):
            return 
        visitors.Visitor.visit(self, element.supers)
        self.claferStack.append(self.cfr.getSort(element.uid))
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        self.claferStack.pop()
    
    def claferidVisit(self, element):
        #print(self.argStack)
        if(self.inConstraint and self.good):
            self.stringStack.append(element.id)
            if element.claferSort:
                self.argStack.append([element.claferSort])
            elif element.id == "ref" and isinstance(self.argStack[-1][-1].refSort, PrimitiveType):
                self.reason = "primitive"
                self.good = False
                return
            elif element.id == "parent":
                self.argStack.append([self.argStack[-1][-1].parent])
            elif element.id == "ref":
                self.argStack.append([self.argStack[-1][-1].refSort])
                #self.argStack.append([element.id])
            else:
                # localdecl case
                self.reason = "quantifier"
                self.good = False

    def constraintVisit(self, element):
        self.inConstraint = True
        self.stringStack = []
        self.argStack = []
        self.opStack = []
        self.reason = ""
        self.good = True
        self.currentConstraint = BracketedConstraint.BracketedConstraint(self.cfr, element, self.claferStack)
        visitors.Visitor.visit(self, element.exp)
        quant = ""
        #print(self.stringStack)
        stringRep = str(self.good) + " (" + self.reason +"): " + (self.stringStack[0] if len(self.stringStack) > 0 else "Empty")
        #print(stringRep)
        #print(self.claferStack)
        self.currentConstraint.claferStack = [i for i in self.claferStack]
        self.currentConstraint.stringRep = stringRep
        if self.good:
            self.currentConstraint.cacheJoins = True
            self.setEqualityConstraints.append(self.currentConstraint)
        else:
            self.otherConstraints.append(self.currentConstraint)
        
        #sys.exit()
        self.currentConstraint = None
        self.inConstraint = False
    
    def funexpVisit(self, element):
        
        if not element.operation in ValidOpsMap.keys():
            self.reason = element.operation
            self.good = False
            return
        (arity, _op) = ValidOpsMap[element.operation]
        if not self.opStack:
            if element.operation != "=":
                #print(element.operation)
                self.good = False
                self.reason = "Non-equals"
                #return
            self.opStack.append(element.operation)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if(self.inConstraint):
            if self.good:
                args = [self.argStack.pop()[-1] for _ in range(arity)]
                args.append(str(element.operation))
                args.reverse()
                #print(args)
                self.argStack.append(args)#"(" + str(element.operation) + " " + " ".join(args) + ")")
                
                args = [self.stringStack.pop() for _ in range(arity)]
                args.append(element.operation)
                args.reverse()
                self.stringStack.append("(" + " ".join(args) + ")")
     
    def integerliteralVisit(self, element):
        if(self.inConstraint):
            self.argStack.append([element.value])
            self.stringStack.append(str(element.value))
            self.good = False
        
    
    def goalVisit(self, element):
        return    
    
    def realliteralVisit(self, element):
        sys.exit("TODO real literal")
        
    def stringliteralVisit(self, element):
        sys.exit("TODO string literal visit")

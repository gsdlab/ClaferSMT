'''
Created on Nov 1, 2013

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


Symmetric_Functions = [
                           #Unary Ops
                           "!",          
                           "UNARY_MINUS",
                           "#",           
                           "max",         
                           "min",        
                           "sum",        
                           #Binary Ops
                           "<=>",
                           #"=>" NOT SYMMETRIC
                           "||",
                           "xor",
                           "&&",
                           #"<" NOT SYMMETRIC
                           #">" NOT SYMMETRIC
                           #"<=" NOT SYMMETRIC
                           #">=" NOT SYMMETRIC
                           "=",
                           "!=",
                           #"in" NOT SYMMETRIC
                           #"nin" NOT SYMMETRIC
                           "+",
                           #"-" NOT SYMMETRIC
                           "*",
                           #"/" NOT SYMMETRIC
                           "++",
                           #"--" NOT SYMMETRIC
                           "&",
                           #"<:" NOT IMPLEMENTED
                           #":>" NOT IMPLEMENTED
                           "." #NOT SYMMETRIC, but we need to keep this one...I think it's ok from what I've seen, since joins are restricted in Clafer
                           #Ternary Ops
                           #"ifthenelse" NOT SURE
                           ]

class CheckFunctionSymmetry(VisitorTemplate.VisitorTemplate):
    '''
    :var self.currentConstraint: (:mod:`~constraints.BracketedConstraint`) Holds the constraint currently being traversed. 
    :var self.inConstraint: (bool) True if the traversal is currently within a constraint.
    :var z3: (:class:`~common.Z3Instance`) The Z3 solver.
    
    Determines if all functions in the given subtree are symmetric functions. If so, we can optimize.
    '''
    
    
    def __init__(self, z3, inConstraint=False):
        '''
        :param z3: The Z3 solver.
        :type z3: :class:`~common.Z3Instance`
        '''
        VisitorTemplate.VisitorTemplate.__init__(self)
        self.isSymmetric = True
        self.visitedLocalDecl = False
        self.z3 = z3


        


    def funexpVisit(self, element):
        #FIX ME
        flag = False
        if not element.operation in Symmetric_Functions:
            self.watchLocals = True
            flag = True
        for i in element.elements:
            visitors.Visitor.visit(self, i)
        if flag and self.visitedLocalDecl:
            self.watchLocals = False
            
        
           
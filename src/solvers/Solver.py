'''
Created on May 14, 2014

@author: ezulkosk
'''
from common import Options
from solvers import Z3
import sys


def getSolver():
    if Options.SOLVER == "z3":
        return Z3.Z3Solver()
    elif Options.SOLVER == "smt2":
        return SMTLibSolver()

class SMTLibSolver():
    def __init__(self):
        self.converter = SMTLibConverter()
        self.solver = []
        
    def add(self, constraint):
        self.solver.append(constraint.convert(self.converter))
    
    def addRaw(self, constraint):
        sys.exit("Unsupported by SMT2 converter.")
    
    def check(self):
        sys.exit("Unsupported by SMT2 converter.")
        
    def model(self):
        sys.exit("Unsupported by SMT2 converter.")

    def assertions(self):
        return self.solver.assertions()
    
    def push(self):
        sys.exit("Unsupported by SMT2 converter.")
        
    def pop(self):
        sys.exit("Unsupported by SMT2 converter.")

class SMTLibConverter():
    
    def if_expr(self):
        pass

'''
Created on May 14, 2014

@author: ezulkosk
'''
from common import Options
import sys


def getSolver():
    from solvers import Z3Solver, SMTLibSolver
    if Options.SOLVER == "z3":
        return Z3Solver.Z3Solver()
    elif Options.SOLVER == "smt2":
        return SMTLibSolver.SMTLibSolver()


class BaseSolver():
    
    def setOptions(self):
        pass
        
    def add(self, constraint):
        sys.exit("add() Unsupported by selected solver.")
    
    def addRaw(self, constraint):
        sys.exit("addRaw() Unsupported by selected solver.")
    
    def check(self):
        sys.exit("check() Unsupported by selected solver.")
        
    def model(self):
        sys.exit("model() Unsupported by selected solver.")

    def assertions(self):
        sys.exit("assertions() Unsupported by selected solver.")
    
    def push(self):
        sys.exit("push() Unsupported by selected solver.")
        
    def pop(self):
        sys.exit("pop() Unsupported by selected solver.")




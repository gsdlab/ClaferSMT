'''
Created on May 14, 2014

@author: ezulkosk
'''
import sys

from common import Options


def getSolver(cfr=None):
    from solvers import Z3Solver, SMTLib2Solver, SMTLib1Solver
    from solvers.walksmt import WalkZ3
    if Options.SOLVER == "z3":
        return Z3Solver.Z3Solver()
    elif Options.SOLVER == "smt2":
        return SMTLib2Solver.SMTLib2Solver()
    elif Options.SOLVER == "smt1":
        return SMTLib1Solver.SMTLib1Solver()
    elif Options.SOLVER == "walkz3":
        return WalkZ3.WalkZ3Solver(cfr)
    else:
        sys.exit(Options.SOLVER + " broken.")

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




'''
Created on May 14, 2014

@author: ezulkosk
'''
from common import Options
from solvers import Z3

def getSolver():
    if Options.SOLVER == "z3":
        return Z3.Z3Solver()
    elif Options.SOLVER == "smt2":
        print("Unimplimented")

class SMTLibConverter():
    
    def if_expr(self):
        pass
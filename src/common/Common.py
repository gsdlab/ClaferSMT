'''
Created on Apr 28, 2013

@author: ezulkosk
'''

from common import SMTLib
import imp
import json
import subprocess
import sys

NORMAL = 0
DEBUG = 1
TEST = 2
ONE = 3
ALL = 4
MODELSTATS = 5 
REPL = 6
EXPERIMENT = 7
ECLIPSE = 8
PRELOAD = 9

#tests
MY_TESTS = 1 # my tests from debugging
POSITIVE_TESTS = 2 # tests from test/positive in the Clafer repository
STRING_TESTS = 3 #tests that involve strings / string constraints
OPTIMIZATION_TESTS = 4
ALL_TESTS = 5

SAT=True
UNSAT=False


BREAK = False
FUNCTION_ID = 0 
CONSTRAINT_ID = 0
STRING_ID = 0
FLAG = False
string_map = {}
STRCONS_SUB = "STRCONS_SUB"
FIRST_REPL_LOOP = True
STANDARD_DELIMETER = "=== Instance "
BOUND = 600

METRICS_MAXIMIZE = 1
METRICS_MINIMIZE = 2


def readJSONFile(file_name):
    '''
    Takes a file name (str) and returns a json dump 
    '''
    file = open(file_name)
    j = json.load(file)
    return j

def mAnd(*args):
    '''
    Short for MaybeAnd.
    Helper Function to simplify formulas passed to Z3, but mostly to make debugging output more comprehensible.
    Only applies the And function if there are actually multiple arguments.
    '''
    newArgs = []
    for i in args:
        if i:
            newArgs.append(i)
    if len(newArgs) == 0:
        return True
    elif len(newArgs) == 1:
        return newArgs[0]
    else:
        return SMTLib.SMT_And(*newArgs)

def mOr(*args):
    '''
    Similar to mAnd
    '''
    newArgs = []
    for i in args:
        if i:
            newArgs.append(i)
    if len(newArgs) == 0:
        return False
    elif len(newArgs) == 1:
        return newArgs[0]
    else:
        return SMTLib.SMT_Or(*newArgs)

def preventSameModel(cfr, solver, model):
    #from constraints import Operations
    #print(model.eval(Operations.EXPR))
    #print(model.eval(Operations.EXPR2))
    block = []
    for i in cfr.cfr_sorts.values():
        for j in i.instances:
            block.append(SMTLib.SMT_NE(j, SMTLib.SMT_IntConst(model[j.var])))
        if i.refs:
            for j in i.refs:
                block.append(SMTLib.SMT_NE(j, SMTLib.SMT_IntConst(model[j.var])))

    if block == []:
        #input was an empty clafer model (no concretes)
        solver.add(SMTLib.SMT_BoolConst(False))
    else:
        solver.add(SMTLib.SMT_Or(*block))

def getConstraintUID():
    '''
    Used to generate unique booleans for UNSAT core
    '''
    global CONSTRAINT_ID
    CONSTRAINT_ID = CONSTRAINT_ID + 1
    return CONSTRAINT_ID

def getStringUID():
    '''
    Used to generate unique booleans for UNSAT core
    '''
    global STRING_ID
    STRING_ID = STRING_ID + 1
    return STRING_ID

def reset():
    '''
    Only needed for running test suites.
    '''
    CONSTRAINT_ID = 0
    STRING_ID = 0

def is_power2(num):
    return num != 0 and ((num & (num - 1)) == 0)

def min2(l,r):
    '''
    returns the min of two integers
    '''
    return SMTLib.SMT_If(SMTLib.SMT_LE(l, r), l, r)

def max2(l,r):
    '''
    returns the min of two integers
    '''
    return SMTLib.SMT_If(SMTLib.SMT_LE(l, r), r, l)

def load(file):
    if file.endswith(".cfr"):
        print("Running 'clafer --mode=python " + str(file) + "' first.")
        try:
            subprocess.call(["clafer", "-sm" , "python", file]);
        except Exception as err:
            print(err)
        file = file[:-4] + ".py"
    file = imp.load_source("module", str(file))
    module = file.getModule()
    return module
    
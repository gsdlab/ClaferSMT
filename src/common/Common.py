'''
Created on Apr 28, 2013

@author: ezulkosk
'''

from z3 import If, And, Or, Int, is_array, is_real
from z3consts import Z3_UNINTERPRETED_SORT
from z3types import Z3Exception
import imp
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
MODE = NORMAL
BREAK = False
FUNCTION_ID = 0 
CONSTRAINT_ID = 0
STRING_ID = 0
FLAG = False
string_map = {}
STRCONS_SUB = "STRCONS_SUB"
FIRST_REPL_LOOP = True
STANDARD_DELIMETER="=== Instance "

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
        return And(*newArgs)

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
        return Or(*newArgs)

def preventSameModel(z3inst, solver, model):
    #from constraints import Operations
    #print(model.eval(Operations.EXPR))
    #print(model.eval(Operations.EXPR2))
    block = []
    for i in z3inst.z3_sorts.values():
        for j in i.instances:
            block.append(j != model[j])
        if i.refs:
            for j in i.refs:
                block.append(j != model[j])

    if block == []:
        #input was an empty clafer model (no concretes)
        solver.add(False)
    else:
        solver.add(Or(block))
    '''
    block = []
    for d in model:
        # d is a declaration
        if d.arity() > 0:
            continue #raise Z3Exception("uninterpreted functions are not supported")
        # create a constant from declaration
        c = d()
        if (str(c)).startswith("z3name!") or is_real(c):
            continue
        if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
            raise Z3Exception("arrays and uninterpreted sorts are not supported")
        block.append(c != model[d])
        #print(str(d) + " = " + str(m[d]))
    if block == []:
        #input was an empty clafer model (no concretes)
        solver.add(False)
    else:
        solver.add(Or(block))
    '''

def debug_print(string):
    '''
    Only prints the string if in DEBUG mode.
    '''
    if(MODE == DEBUG):
        print(string)
        
def standard_print(string):
    '''
    Prints the string if **not** in TEST mode.
    '''
    if(MODE != TEST and MODE != EXPERIMENT):
        print(string)
        
def experiment_print(string=""):
    if MODE == EXPERIMENT:
        print(string)

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


def min2(l,r):
    '''
    returns the min of two integers
    '''
    return If(l <= r, l, r)

def max2(l,r):
    '''
    returns the min of two integers
    '''
    return If(l <= r, r, l)

def load(file):
    if file.endswith(".cfr"):
        sys.exit("Run 'clafer --mode=python " + str(file) + "' first.")
    file = imp.load_source("module", str(file))
    module = file.getModule()
    return module
    
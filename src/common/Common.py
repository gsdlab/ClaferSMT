'''
Created on Apr 28, 2013

@author: ezulkosk
'''
from z3 import If, And, Or

NORMAL = 0
DEBUG = 1
TEST = 2
ONE = 3
MODE = NORMAL
BREAK = False
FUNCTION_ID = 0 
CONSTRAINT_ID = 0
FLAG = False

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
    if(MODE != TEST):
        print(string)

def getConstraintUID():
    '''
    Used to generate unique booleans for UNSAT core
    '''
    global CONSTRAINT_ID
    CONSTRAINT_ID = CONSTRAINT_ID + 1
    return CONSTRAINT_ID

def reset():
    '''
    Only needed for running test suites.
    '''
    CONSTRAINT_ID = 0


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
    
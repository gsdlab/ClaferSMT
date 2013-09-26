'''
Created on Apr 28, 2013

@author: ezulkosk
'''
from z3 import If, Function, BoolSort, IntSort

NORMAL = 0
DEBUG = 1
TEST = 2
MODE = NORMAL

FUNCTION_ID = 0 
CONSTRAINT_ID = 0

bool2Int = None

def debug_print(string):
    if(MODE == DEBUG):
        print(string)
        
def standard_print(string):
    if(MODE != TEST):
        print(string)

#used to generate unique Z3 function names -- that was a fun bug...
def getFunctionUID():
        global FUNCTION_ID
        FUNCTION_ID = FUNCTION_ID + 1
        return FUNCTION_ID
    
#used to generate unique booleans for UNSAT core
def getConstraintUID():
    global CONSTRAINT_ID
    CONSTRAINT_ID = CONSTRAINT_ID + 1
    return CONSTRAINT_ID

def reset():
    FUNCTION_ID = 0
    CONSTRAINT_ID = 0

def bool2Int():
    return bool2Int

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
    
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

#canBeOff conditionals
DEFINITELY_OFF = -1
UNKNOWN = 0
DEFINITELY_ON = 1


def aggregate_polarity(p1, p2):
    #unknown or unknown => unknown
    #unknown or off => unknown
    #unknown or on => on
    #...
    #on or off => on
    return max(p1, p2)


#tests
MY_TESTS = 1 # my tests from debugging
POSITIVE_TESTS = 2 # tests from test/positive in the Clafer repository
STRING_REALS_TESTS = 3 #tests that involve strings / string constraints
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

def stripPrefix(s):
    try:
        return s.split('_', maxsplit=1)[1]
    except:
        return s
    

def evalForNum(model, expr):
    val = model.eval(expr)
    if not val:
        return val
    else:
        strval = str(val)
    try:
        val = int(strval)
    except:
        val = float(strval)
    return val

def computeCacheKeys(flattenedJoin):
    #print("FLATTENED:")
    first = flattenedJoin.pop(0)
    key = list(first.clafers.keys())
    key = sorted(key)
    #print(key)
    firstkeys = [key]
    sort = key[0][0]
    while sort.superSort:
        index = sort.indexInSuper
        newkey = []
        for (s,i) in key:
            newkey.append((s.superSort, i + index))
        firstkeys.append(newkey)
        sort = sort.superSort
    #print(firstkeys)
    #sys.exit()
    for j in flattenedJoin:
        try:
            currKey = j.value
        except:
            currKey = str(list(j.clafers.keys())[0][0])
        firstkeys = [key + [currKey] for key in firstkeys]
    #print(firstkeys)
    return [tuple(key) for key in firstkeys]

def isBoolConst(b):
    return isinstance(b, SMTLib.SMT_BoolConst) or isinstance(b, bool)

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
    args = list(args)
    newArgs = []
    while(args):
        i = args.pop()
        if isinstance(i, SMTLib.SMT_And):
            for j in i.children():
                args.append(j)
            continue
        if i:
            if str(i) == "True":
                continue
            if str(i) == "False":
                return SMTLib.SMT_BoolConst(False)
            newArgs.append(i)
    if len(newArgs) == 0:
        return SMTLib.SMT_BoolConst(True)
    elif len(newArgs) == 1:
        return newArgs[0]
    else:
        return SMTLib.SMT_And(*newArgs)

def mOr(*args):
    '''
    Similar to mAnd
    '''
    args = list(args)
    newArgs = []
    while(args):
        i = args.pop()
        if isinstance(i, SMTLib.SMT_Or):
            #print(i)
            for j in i.children():
                #print(j)
                args.append(j)
            continue
        if i:
            if isinstance(i, SMTLib.SMT_BoolConst):
                if str(i) == "False":
                    continue
                else:
                    return SMTLib.SMT_BoolConst(True)
            newArgs.append(i)
    if len(newArgs) == 0:
        return SMTLib.SMT_BoolConst(False)
    elif len(newArgs) == 1:
        return newArgs[0]
    else:
        return SMTLib.SMT_Or(*newArgs)

def preventSameModel(cfr, solver, model):
    block = []
    for i in cfr.cfr_sorts.values():
        for j in i.instances:
            block.append(SMTLib.SMT_NE(j, SMTLib.SMT_IntConst(int(str(model[j.var])))))
        if i.refs:
            for j in i.refs:
                try:
                    val = model[j.var]
                except:
                    #happens if a primitive ref is totally unrestricted
                    continue 
                if not val:
                    continue
                else:
                    block.append(SMTLib.SMT_NE(j, SMTLib.SMT_IntConst(val)))

    if block == []:
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
    
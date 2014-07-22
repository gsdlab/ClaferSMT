'''
Created on Oct 6, 2013

@author: ezulkosk
'''

from common import Common
import argparse
import sys


'''
========
| TODO |
========
* Fix any ops left in Operations
* Real Numbers
* Strings
* Change DoubleLiteral to RealLiteral
* Traversal of quantified formulas is exponential...
* Fix quantifier symmetry breaker, if two locals FROM THE SAME QUANTIFIER are on the left and right of a func, not symmetric
* Documentation
* Need to treat ints and reals "the same" if in the same set.
* Fix bag problem for everything, (look at ints for correct)
'''

GLOBAL_SCOPE = 1

MODE = Common.NORMAL # Common.[EXPERIMENT | MODELSTATS | NORMAL | DEBUG | TEST | ONE | ALL], where ONE outputs one model from each test
SOLVER = "z3"

PRINT_CONSTRAINTS = True
STRING_CONSTRAINTS = False
GOAL = False
NUM_INSTANCES = 10 # -1 to produce all instances
INFINITE = -1 
PROFILING = True # True to output the translation time, and time to get first model
CPROFILING = False #invokes the standard python profiling method (see Z3Run.py)
BREAK_QUANTIFIER_SYMMETRY = False
EXTEND_ABSTRACT_SCOPES = True
FILE = ""
TEST_SET = Common.MY_TESTS 
UNIQUE_NAMES = False
SHOW_INHERITANCE = False
DELIMETER=""
INDENTATION="  "
MAGNIFYING_GLASS = False
OUTPUT_MODE=""
PRODUCE_UNSAT_CORE = False
USE_BITVECTORS = False
IGNORE_GOALS = False
SUPPRESS_MODELS = False

SCOPE_FILE = ""
SCOPE_MAP_FILE = ""


''' parallel options '''
CORES=1
TIME_OUT = 0
SAP=1
FEATURE_MODEL= 2
NO_SPLIT=2
SPLIT="no_split"
SERVER=""
SERVICE=""
NUM_SPLIT=1
HEURISTICS = []
EXPERIMENT_NUM_SPLIT = []
MODEL_CLASS = FEATURE_MODEL
VERBOSE_PRINT=False
LEARNING_ENVIRONMENT="local"

modeMap = {
           'experiment' : Common.EXPERIMENT,
           'modelstats' : Common.MODELSTATS,
           'normal'     : Common.NORMAL,
           'debug'      : Common.DEBUG,
           'test'       : Common.TEST,
           'one'        : Common.ONE,
           'all'        : Common.ALL,
           'repl'        : Common.REPL,
           }

testMap = {
           'edstests'     : Common.MY_TESTS,
           'positive'     : Common.POSITIVE_TESTS,
           'string'       : Common.STRING_REALS_TESTS,
           'optimization' : Common.OPTIMIZATION_TESTS,
           'all'          : Common.ALL_TESTS
           }

def debug_print(string):
    '''
    Only prints the string if in DEBUG mode.
    '''
    if(MODE == Common.DEBUG):
        print(string)
        
def standard_print(string):
    '''
    Prints the string if **not** in TEST mode.
    '''
    if(MODE != Common.TEST and MODE != Common.EXPERIMENT):
        print(string)
        
def experiment_print(string=""):
    if MODE == Common.EXPERIMENT:
        print(string)

def setCommandLineOptions(learner = False):
    from parallel.heuristics import GeneralHeuristics
    parser = argparse.ArgumentParser(description='Process a clafer model with Z3.')
    parser.add_argument('file', help='the clafer python file', nargs='?')
    parser.add_argument('--mode', '-m', dest='mode', default='normal',
                       choices=['experiment', 'modelstats', 'normal', 'debug', 'test', 'one', 'repl', 'all'])
    parser.add_argument('--printconstraints', '--pc', dest='printconstraints', default=False, const = True, action='store_const', help='print all Z3 constraints (for debugging)')
    parser.add_argument('--profiling', '-p', dest='profiling', action='store_const', default = False,  const=True,  help='basic profiling of phases of the solver')
    parser.add_argument('--cprofiling', dest='cprofiling',action='store_const', default=False, const=True,  help='uses cprofile for profiling functions of the translation')
    parser.add_argument('--numinstances', '-n', dest='numinstances', type=int, default='1', help='the number of models to be displayed (-1 for all)')
    parser.add_argument('--globalscope', '-g', dest='globalscope', type=int, default='1', help='the global scope for unbounded clafers (note that this does not match regular clafer)')
    parser.add_argument('--testset', '-t', dest='test_set', default='edstests', help='The test set to be used for modes [experiment | test | one | all], or the number of tests to generate')#,
    parser.add_argument('--stringconstraints' , '-s', default=False, dest='stringconstraints',action='store_const',  const=True,  help='Flag to output to Z3-Str format instead')
    parser.add_argument('--solver', dest='solver', default='z3', choices=['z3', 'cvc4', 'smt2'], help='Backend solver')
    parser.add_argument('--printuniquenames', '-u', default=False, dest='unique_names',action='store_const',  const=True,  help='Print clafers with unique prefixes')
    parser.add_argument('--showinheritance', default=False, dest='show_inheritance',action='store_const',  const=True,  help='Show super-clafers explicitly')
    parser.add_argument('--version', '-v', default=False, dest='version',action='store_const',  const=True,  help='Print version number.')
    parser.add_argument('--delimeter', default=Common.STANDARD_DELIMETER, dest='delimeter', help='Delimeter between instances.')
    parser.add_argument('--indentation', dest='indentation', default='doublespace', choices=['doublespace', 'tab'])
    parser.add_argument('--magnifyingglass', default=False, dest='magnifying_glass',action='store_const',  const=True,  help='Print equally optimal solutions if optimizing')
    parser.add_argument('--produceunsatcore', dest='produceunsatcore', default=False, const = True, action='store_const', help='produce unsat core for UNSAT specifications')
    parser.add_argument('--usebitvectors', dest='usebitvectors', default=False, const = True, action='store_const', help='Use bitvectors to represent clafer instances')
    parser.add_argument('--ignoregoals', dest='ignoregoals', default=False, const = True, action='store_const', help='Ignore optimization objectives (for testing purposes)')
    parser.add_argument('--suppressmodels', dest='suppressmodels', default=False, const = True, action='store_const', help='Do not output satisfying solutions (for test mode)')
    parser.add_argument('--scopefile', default="", dest='scopefile', help='Scope file produced by `clafer --meta-data`. Requires the map file as well.')
    parser.add_argument('--scopemapfile', default="", dest='scopemapfile', help='Scope map file produced by `clafer --meta-data`. Requires the scope file as well.')
    
    ''' parallel '''
    parser.add_argument('--cores', '-c', dest='cores', type=int, default='1', help='the number of cores for parallel processing')
    parser.add_argument('--server', default="Server", dest='server', help='The name of the Server clafer in SAP problems (used for parallelization)')
    parser.add_argument('--service', default="Service", dest='service', help='The name of the Service clafer in SAP problems (used for parallelization)')
    parser.add_argument('--split', dest='split', default='no_split', choices=list(GeneralHeuristics.heuristics) + ['NO_SPLIT'])
    parser.add_argument('--numsplit', dest='numsplit', type=int, default='-1', help='The number of splits to perform (default = #cores)')
    parser.add_argument('--heuristicsfile', dest='heuristics_file', default='all', help='File containing the heuristics to be tested. If none given, all will be used')
    parser.add_argument('--experimentnumsplits', dest='experimentnumsplits', type=int, default='-1', nargs='*', help='List of the number of splits to perform (default = #cores)')
    parser.add_argument('--modelclass', dest='model_class', default='featuremodel', choices=['featuremodel'])
    parser.add_argument('--classifier', dest='classifier', default='ldac', choices=['ldac', 'svm', 'classtree'], help='The learning technique to be applied')
    parser.add_argument('--learningiterations', dest='learning_iterations', type=int, default='10', help='the number of iterations through the learning process')
    
    parser.add_argument('--timeout', dest='time_out', type=float, default='0', help='The time out for consumers')
    
    args = parser.parse_args()
    if args.version:
        print("ClaferZ3 0.3.6.04-04-2014")
        sys.exit()
    if not args.file and not (args.mode in ['experiment', 'test', 'one', 'all'] or learner):
        parser.print_help()
        sys.exit("\nERROR: If no file is given, mode must be set to [experiment | test | one | all].")
    else:
        global FILE
        FILE = args.file
    global MODE
    MODE = modeMap[args.mode]
    global PRINT_CONSTRAINTS
    PRINT_CONSTRAINTS = args.printconstraints
    
    global PROFILING
    PROFILING = (args.profiling or learner) 
    global CPROFILING
    CPROFILING = args.cprofiling
    global NUM_INSTANCES
    NUM_INSTANCES = args.numinstances
    global GLOBAL_SCOPE
    GLOBAL_SCOPE = args.globalscope
    global TEST_SET
    try:
        TEST_SET = testMap[args.test_set]
    except:
        TEST_SET = args.test_set
    global STRING_CONSTRAINTS
    STRING_CONSTRAINTS= args.stringconstraints
    global MAGNIFYING_GLASS
    MAGNIFYING_GLASS= args.magnifying_glass
    global UNIQUE_NAMES
    UNIQUE_NAMES = args.unique_names
    global SHOW_INHERITANCE
    SHOW_INHERITANCE = args.show_inheritance
    global DELIMETER
    if args.delimeter =="\"\"":
        args.delimeter = ""
    DELIMETER = args.delimeter
    global CORES
    CORES = args.cores
    global INDENTATION
    if args.indentation == "tab":
        INDENTATION = "\t"
    global SERVER
    SERVER = args.server
    global SERVICE
    SERVICE = args.service
    global SPLIT
    SPLIT = args.split
    global TIME_OUT
    TIME_OUT = args.time_out
        
    global NUM_SPLIT
    if args.numsplit == -1:
        NUM_SPLIT = CORES
    else:
        NUM_SPLIT = args.numsplit
    global EXPERIMENT_NUM_SPLIT
    if args.experimentnumsplits == -1:
        EXPERIMENT_NUM_SPLIT = [CORES]
    elif isinstance(args.experimentnumsplits, int):
        EXPERIMENT_NUM_SPLIT = [args.experimentnumsplits]
    else:
        EXPERIMENT_NUM_SPLIT = args.experimentnumsplits
        
    global USE_BITVECTORS
    USE_BITVECTORS = args.usebitvectors
    global SOLVER
    SOLVER = args.solver.strip()
    global PRODUCE_UNSAT_CORE
    PRODUCE_UNSAT_CORE = args.produceunsatcore    
    global IGNORE_GOALS
    IGNORE_GOALS = args.ignoregoals
    global SCOPE_FILE
    SCOPE_FILE = args.scopefile
    global SCOPE_MAP_FILE
    SCOPE_MAP_FILE = args.scopemapfile
    global SUPPRESS_MODELS
    SUPPRESS_MODELS = args.suppressmodels
    return args    
    
        
    
    



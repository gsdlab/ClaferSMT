'''
Created on Oct 6, 2013

@author: ezulkosk
'''

from common import Common
from optparse import OptionParser
from parallel.heuristics import GeneralHeuristics
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

'''
POSITIVE TEST SUITE RUN WITH A GLOBAL_SCOPE OF 6.
'''

GLOBAL_SCOPE = 1#this obviously has to change

ECLIPSE = False 

MODE = Common.NORMAL # Common.[EXPERIMENT | MODELSTATS | NORMAL | DEBUG | TEST | ONE | ALL], where ONE outputs one model from each test
PRINT_CONSTRAINTS = True
STRING_CONSTRAINTS = False
CNF = False
GOAL = False
NUM_INSTANCES = 10 # -1 to produce all instances
INFINITE = -1 #best variable name.
PROFILING = True # True to output the translation time, and time to get first model
CPROFILING = False #invokes the standard python profiling method (see Z3Run.py)
GET_ISOMORPHISM_CONSTRAINT = False #efficiency bugs in quantified formulas are preventing this from working
BREAK_QUANTIFIER_SYMMETRY = False
EXTEND_ABSTRACT_SCOPES = True
FILE = ""
MY_TESTS = 1 # my tests from debugging
POSITIVE_TESTS = 2 # tests from test/positive in the Clafer repository
STRING_TESTS = 3 #tests that involve strings / string constraints
TEST_SET = MY_TESTS 
DIMACS_FILE="dimacs"
UNIQUE_NAMES = False
SHOW_INHERITANCE = False
DELIMETER=""
INDENTATION="  "
MAGNIFYING_GLASS = False

''' parallel options '''
CORES=1

SAP=1
NO_SPLIT=2
SPLIT=SAP
SERVER=""
SERVICE=""
NUM_SPLIT=1
HEURISTICS = []

def MODULE():
    from test import simple_feature_model, cc_example, all_threes, i147refdisambiguation, simp

    MODULE = ""
    #MODULE = bracketedconstraint_this.getModule()
    #MODULE = multiple_joins.getModule()
    #MODULE = this_dot_parent.getModule()
    #MODULE = arithmetic.getModule()
    #MODULE = relations.getModule()
    #MODULE = boolean_connectives.getModule()
    #MODULE = union.getModule()
    #MODULE = simple_abstract.getModule()
    #MODULE = phpscript.getModule()
    #MODULE = some.getModule()
    #MODULE = paths.getModule()
    #MODULE = mypaths.getModule()
    #MODULE = simple_set.getModule()
    #MODULE = zoo.getModule()
    #MODULE = simple_zoo.getModule()
    #MODULE = integer_refs.getModule()
    #MODULE = minimal_integer_refs.getModule()
    #MODULE = phone_feature_model.getModule()
    #MODULE = higher_inheritance.getModule()
    #MODULE = this_integer_relation.getModule()
    #MODULE = equal_references.getModule()
    #MODULE = dag_test.getModule()
    #MODULE = books_tutorial.getModule()
    #MODULE = simple_books.getModule()
    #MODULE = teststring.getModule()
    #MODULE = testunion.getModule()
    #MODULE = subbooks.getModule()
    #MODULE = int_ref_set.getModule()
    #MODULE = one_plus_one_equals_one.getModule()
    #MODULE = iso.getModule()
    #MODULE = isowithcons.getModule()
    #MODULE = all_alls.getModule()
    #MODULE = some_somes.getModule()
    #MODULE = constraints.getModule()
    #MODULE = constraintswithbounds.getModule()
    #MODULE = AADL_simplified_with_lists.getModule()
    #MODULE = all_threes.getModule()
    #MODULE = i101.getModule()
    #MODULE = top_level_constraints_with_relational_joins.getModule()
    #MODULE = telematics.getModule()
    #MODULE = i17.getModule()
    #MODULE = i188sumquantifier.getModule()
    #MODULE = i78_transitiveclosure.getModule()
    #MODULE = scope_test.getModule()
    #MODULE = i131incorrectscope.getModule()
    #MODULE = enforcingInverseReferences.getModule()
    #MODULE = trivial.getModule()
    #MODULE = i72sharedreference.getModule()
    #MODULE = trivial2.getModule()
    #MODULE = simple_real.getModule()
    #MODULE = Phone.getModule()
    #MODULE = check_unique_ref_names_with_inheritance.getModule()
    #MODULE = maximize.getModule()
    #MODULE = two_objective_min.getModule()
    #MODULE = two_objective_max.getModule()
    MODULE = simple_feature_model.getModule()
    #MODULE = simp.getModule()
    #MODULE = i147refdisambiguation.getModule()
    #MODULE = "" 
    
    MODULE = cc_example.getModule()
    return MODULE

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
           'edstests'   : MY_TESTS,
           'positive'   : POSITIVE_TESTS,
           'string'     : STRING_TESTS
           }


def foo_callback(option, opt, value, parser):
    print("A")
    setattr(parser.values, option.dest, value.split(','))


def setCommandLineOptions():
    parser = argparse.ArgumentParser(description='Process a clafer model with Z3.')
    parser.add_argument('file', help='the clafer python file', nargs='?')
    parser.add_argument('--mode', '-m', dest='mode', default='normal',
                       choices=['experiment', 'modelstats', 'normal', 'debug', 'test', 'one', 'repl', 'all'])
    parser.add_argument('--printconstraints', '--pc', dest='printconstraints', default=False, const = True, action='store_const', help='print all Z3 constraints (for debugging)')
    parser.add_argument('--profiling', '-p', dest='profiling', action='store_const', default = False,  const=True,  help='basic profiling of phases of the solver')
    parser.add_argument('--cprofiling', dest='cprofiling',action='store_const', default=False, const=True,  help='uses cprofile for profiling functions of the translation')
    parser.add_argument('--numinstances', '-n', dest='numinstances', type=int, default='1', help='the number of models to be displayed (-1 for all)')
    parser.add_argument('--globalscope', '-g', dest='globalscope', type=int, default='1', help='the global scope for unbounded clafers (note that this does not match regular clafer)')
    parser.add_argument('--testset', '-t', dest='testset', default='edstests', help='The test set to be used for modes [experiment | test | one | all]',
                        choices=['edstests', 'positive', 'string'])
    parser.add_argument('--stringconstraints' , '-s', default=False, dest='stringconstraints',action='store_const',  const=True,  help='Flag to output to Z3-Str format instead')
    parser.add_argument('--cnf', default=False, dest='cnf',action='store_const',  const=True,  help='Outputs CNF of formula.')
    parser.add_argument('--dimacs', default="dimacs", dest='dimacs', help='Output DIMACS')
    parser.add_argument('--printuniquenames', '-u', default=False, dest='unique_names',action='store_const',  const=True,  help='Print clafers with unique prefixes')
    parser.add_argument('--showinheritance', default=False, dest='show_inheritance',action='store_const',  const=True,  help='Show super-clafers explicitly')
    parser.add_argument('--version', '-v', default=False, dest='version',action='store_const',  const=True,  help='Print version number.')
    parser.add_argument('--delimeter', default="", dest='delimeter', help='Delimeter between instances.')
    parser.add_argument('--indentation', dest='indentation', default='doublespace', choices=['doublespace', 'tab'])
    parser.add_argument('--magnifyingglass', default=False, dest='magnifying_glass',action='store_const',  const=True,  help='Print equally optimal solutions if optimizing')
    
    parser.add_argument('--cores', '-c', dest='cores', type=int, default='1', help='the number of cores for parallel processing')
    parser.add_argument('--server', default="Server", dest='server', help='The name of the Server clafer in SAP problems (used for parallelization)')
    parser.add_argument('--service', default="Service", dest='service', help='The name of the Service clafer in SAP problems (used for parallelization)')
    parser.add_argument('--split', dest='split', default='NO_SPLIT', choices=list(GeneralHeuristics.HeuristicsMap.keys()) + ['NO_SPLIT'])
    parser.add_argument('--numsplit', dest='numsplit', type=int, default='-1', help='The number of splits to perform (default = #cores)')
    parser.add_argument('--heuristics', dest='heuristics', default='NO_SPLIT', nargs='*', choices=list(GeneralHeuristics.HeuristicsMap.keys()) + ['NO_SPLIT'])
    
    
    parser.add_argument('--classifier', dest='classifier', default='svm',
                       choices=['svm', 'classtree'])
    parser.add_argument('--learningiterations', dest='learning_iterations', type=int, default='10', help='the number of iterations through the learning process')
    
    args = parser.parse_args()
    if args.version:
        print("ClaferZ3 0.3.6.04-04-2014")
        sys.exit()
    global ECLIPSE
    if ECLIPSE:
        ECLIPSE = True 
        return
    else:
        ECLIPSE = False
    if not args.file and not (args.mode in ['experiment', 'test', 'one', 'all']):
        parser.print_help()
        sys.exit("\nERROR: If no file is given, mode must be set to [experiment | test | one | all].")
    else:
        global FILE
        FILE = args.file
    global MODE
    MODE = modeMap[args.mode]
    global PRINT_CONSTRAINTS
    PRINT_CONSTRAINTS = args.printconstraints
    global HEURISTICS
    HEURISTICS = args.heuristics
    global PROFILING
    PROFILING = args.profiling
    global CPROFILING
    CPROFILING = args.cprofiling
    global NUM_INSTANCES
    NUM_INSTANCES = args.numinstances
    global GLOBAL_SCOPE
    GLOBAL_SCOPE = args.globalscope
    global TEST_SET
    TEST_SET = testMap[args.testset]
    global STRING_CONSTRAINTS
    STRING_CONSTRAINTS= args.stringconstraints
    global CNF
    CNF= args.cnf
    global MAGNIFYING_GLASS
    MAGNIFYING_GLASS= args.magnifying_glass
    global DIMACS_FILE
    DIMACS_FILE = args.dimacs
    global UNIQUE_NAMES
    UNIQUE_NAMES = args.unique_names
    global SHOW_INHERITANCE
    SHOW_INHERITANCE = args.show_inheritance
    global DELIMETER
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
    if args.split == "SAP":
        SPLIT=SAP
    else:
        SPLIT=NO_SPLIT
    global NUM_SPLIT
    if args.numsplit == -1:
        NUM_SPLIT = CORES
    else:
        NUM_SPLIT = args.numsplit
    return args    
    
        
    
    



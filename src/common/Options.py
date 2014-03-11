'''
Created on Oct 6, 2013

@author: ezulkosk
'''

from common import Common
from optparse import OptionParser
'''
from test import i188sumquantifier, multiple_joins, bracketedconstraint_this, \
    this_dot_parent, arithmetic, relations, boolean_connectives, union, \
    simple_abstract, some, simple_set, integer_refs, higher_inheritance, \
    this_integer_relation, equal_references, all_alls, all_threes, zoo, \
    books_tutorial, check_unique_ref_names_with_inheritance, constraints, \
    enforcingInverseReferences, i101, i10, i121comments, i122CVL, i126empty, \
    i131incorrectscope, i137_parsing, i147refdisambiguation, i14, i17, i18, i19, \
    i205refdisambiguationII, i23, i40_integers_strings_assignment, i40textequality, \
    i49_parentReduce, i49_resolve_ancestor, i50_stop_following_references, i55, \
    i57navParent, i61cardinalities, i70, i71, i72sharedreference, \
    i78_transitiveclosure, i83individualscope, i98_toplevelreferences, layout, \
    negative, paths, personRelatives, person_tutorial, resolution, simp, \
    subtypingprimitivetypes, telematics, test_neg_typesystem, simple_books, \
    one_plus_one_equals_one, scope_test, trivial, trivial2, mypaths, \
    AADL_simplified_with_lists, teststring, testunion, simple_real, Phone, \
    int_ref_set, phpscript, iso, maximize, two_objective_min, two_objective_max, \
    Cruise, small
'''
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
* Fix printer
* Traversal of quantified formulas is exponential...
* Fix quantifier symmetry breaker, if two locals FROM THE SAME QUANTIFIER are on the left and right of a func, not symmetric
* Documentation
* Need to treat ints and reals "the same" if in the same set.
'''

'''
POSITIVE TEST SUITE RUN WITH A GLOBAL_SCOPE OF 6.
'''

GLOBAL_SCOPE = 1#this obviously has to change

ECLIPSE = False

MODE = Common.NORMAL # Common.[EXPERIMENT | MODELSTATS | NORMAL | DEBUG | TEST | ONE | ALL], where ONE outputs one model from each test
PRINT_CONSTRAINTS = False
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
MODULE=""
#MODULE = small.getModule()
'''
my_tests = [ 
          (multiple_joins, 1),
          (bracketedconstraint_this, 6),
          (this_dot_parent, 2),
          (arithmetic, 2),
          (relations, 1),
          (boolean_connectives, 2),
          (union, 6),
          (simple_abstract, 0),
          (some, 1),
          (integer_refs, 1),
          (higher_inheritance, 1),
          (this_integer_relation, 2),
          (equal_references, 2),
          (all_alls, 1),
          (all_threes, 1),
          (simple_real, 1),
          (zoo, INFINITE)
         ]

positive_tests = [
        (books_tutorial,INFINITE),
        (constraints,INFINITE),
        (enforcingInverseReferences,INFINITE),
        (i101, 1),
        (i10,INFINITE),
        (i121comments, 2),
        (i122CVL,INFINITE),
        (i126empty, 1),
        (i131incorrectscope, 10),
        (i137_parsing, 1),
        (i147refdisambiguation, 3),
        (i14, 1),
        (i17, 1),
        (i188sumquantifier,INFINITE),
        (i19,INFINITE),
        (i205refdisambiguationII,INFINITE),
        (i23,INFINITE),
        (i49_parentReduce, 1),
        (i49_resolve_ancestor,INFINITE),
        (i50_stop_following_references, 1),
        (i55, 1),
        (i57navParent, 1),
        (i61cardinalities,INFINITE),
        (i70, 3),
        (i71,INFINITE),
        (i72sharedreference, 10),
        (i78_transitiveclosure, 0),
        (i83individualscope,INFINITE),
        (i98_toplevelreferences, 1),
        (layout, 1),
        (negative, 1),
        (paths, 10),
        (personRelatives,INFINITE),
        (person_tutorial,INFINITE),
        (resolution,INFINITE),
        (simp, 1),
        (telematics, 1),
        (test_neg_typesystem,INFINITE)
                  ]

string_tests = [
                (check_unique_ref_names_with_inheritance, 1),
                (i18, 2),
                (i40_integers_strings_assignment, 6),
                (i40textequality, 1),
                (subtypingprimitivetypes, 1)
                ]

'''
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
    parser.add_argument('--stringconstraints' , '-s', default=False, dest='stringconstraints',action='store_const',  const=True,  help='Flag to output to Z3-Str format instead.')
    parser.add_argument('--cnf', default=False, dest='cnf',action='store_const',  const=True,  help='Outputs CNF of formula.')
    parser.add_argument('--dimacs', default="dimacs", dest='dimacs', help='Output DIMACS.')
    parser.add_argument('--printuniquenames', '-u', default=False, dest='unique_names',action='store_const',  const=True,  help='Print clafers with unique prefixes.')
    parser.add_argument('--showinheritance', default=False, dest='show_inheritance',action='store_const',  const=True,  help='Show super-clafers explicitly.')
    parser.add_argument('--version', '-v', default=False, dest='version',action='store_const',  const=True,  help='Print version number.')
    parser.add_argument('--delimeter', default="", dest='delimeter', help='Output DIMACS.')
    
    args = parser.parse_args()
    if args.version:
        print("ClaferZ3 0.3.6.06-03-2014")
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
    global DIMACS_FILE
    DIMACS_FILE = args.dimacs
    global UNIQUE_NAMES
    UNIQUE_NAMES = args.unique_names
    global SHOW_INHERITANCE
    SHOW_INHERITANCE = args.show_inheritance
    global DELIMETER
    DELIMETER = args.delimeter
    



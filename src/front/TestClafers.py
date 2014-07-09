'''
Created on Sep 15, 2013

@author: ezulkosk
'''
from common import Options, Common
from common.Clock import Clock
from common.Options import INFINITE
from front.ClaferModel import ClaferModel
import sys
import traceback

SEPARATOR = "========================================================" 
def print_separate(x):
    print("\n" + SEPARATOR + "\n| " + x + "\n" +  SEPARATOR + "\n")

def getTestSet():   
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
        Cruise, small, cc_examplemod, minmax, cc_example, optimization_ssap
    
    
    my_tests = [ 
          (multiple_joins, 1),
          (bracketedconstraint_this, 6),
          (this_dot_parent, 2),
          (arithmetic, 2),
          (relations, 1),
          (boolean_connectives, 2),
          (union, 1),
          (simple_abstract, 1),
          (some, 1),
          (integer_refs, 1),
          (higher_inheritance, 1),
          (this_integer_relation, 1),
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
        (i131incorrectscope, 16),
        (i137_parsing, 1),
        (i147refdisambiguation, INFINITE),
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
        (i72sharedreference, 90),
        (i78_transitiveclosure, 4),
        (i83individualscope,INFINITE),
        (i98_toplevelreferences, 1),
        (layout, 1),
        (negative, 1),
        (paths, 724),
        (personRelatives,INFINITE),
        (person_tutorial,INFINITE),
        (resolution,INFINITE),
        (telematics, 1),
        (test_neg_typesystem,INFINITE)
                  ]
            
    optimization_tests = [
                    (minmax, 1),
                    (cc_example, 18),
                    (optimization_ssap, 1)
                    ]

    string_tests = [
                (check_unique_ref_names_with_inheritance, 1),
                (i18, 2),
                (i40_integers_strings_assignment, 6),
                (i40textequality, 1),
                (subtypingprimitivetypes, 1)
                ]
    
    if Options.TEST_SET == Common.MY_TESTS:
        return my_tests
    elif Options.TEST_SET == Common.POSITIVE_TESTS:
        return positive_tests
    elif Options.TEST_SET == Common.OPTIMIZATION_TESTS:
        return optimization_tests
    elif Options.TEST_SET == Common.ALL_TESTS:
        return my_tests + positive_tests + optimization_tests
        
def run():
    '''
    Runs the Z3-translator on each pair (file, numInstances) in tests, 
    and ensures that the number of generated models equals numInstances.
    '''
    clock = Clock()
    tests = getTestSet()
    num_passed = 0
    exceptions = 0
    exception_list = []
    failed_list = []
    temp_model_count = Options.NUM_INSTANCES
    for t in tests:
        (file, expected_model_count) = t
        try:
            if expected_model_count == Options.INFINITE and Options.NUM_INSTANCES < 0:
                #will change it back after the test runs
                Options.NUM_INSTANCES = 5
            module = file.getModule()
            print_separate("Attempting: " + str(file.__name__))
            clock.tick("Total Z3 Run Time")
            cfr = ClaferModel(module)
            actual_model_count = cfr.run()
            clock.tack("Total Z3 Run Time")
            clock = clock.combineClocks(cfr.clock)
            if(expected_model_count == actual_model_count or 
               (expected_model_count == Options.INFINITE and actual_model_count == Options.NUM_INSTANCES)):
                print("PASSED: " + str(file.__name__))
                num_passed = num_passed + 1
            else:
                failed_list.append(str(file.__name__))
                print("FAILED: " + str(file.__name__) + " " + str(expected_model_count) + " " + str(actual_model_count))
        except:
            print("FAILED: " + str(file.__name__) + " " + "\nException raised.")
            traceback.print_exc()
            exception_list.append(str(file.__name__))
            exceptions = exceptions + 1
        Options.NUM_INSTANCES = temp_model_count    
    print_separate("Results: " + str(num_passed) + "/" + str(len(tests)) + "\n| " + 
                   "Failed List: " + str(failed_list) + "\n| " +
                   "Exceptions: " + str(exceptions) + "/" + str(len(tests)) + "\n| " +
                   "Exception List: " + str(exception_list))
    clock.printEvents()
       
def runForOne():  
    '''
    Runs the Z3-translator on each pair file in tests, 
    and outputs one model for each, if satisfiable.
    '''  
    Options.NUM_INSTANCES = 1
    Options.MODE = Common.NORMAL
    run()
    
def runForAll():
    '''
    Runs the Z3-translator on each pair file in tests, 
    and outputs all model for each, if satisfiable (limited if infinite models).
    '''
    Options.MODE = Common.NORMAL
    run()
'''

'''
'''
Created on Sep 15, 2013

@author: ezulkosk
'''
from common import Z3Instance, Options
from test import multiple_joins, bracketedconstraint_this, this_dot_parent, \
    arithmetic, relations, boolean_connectives, union, simple_abstract, some, \
    simple_set, integer_refs, higher_inheritance, this_integer_relation, \
    equal_references
from test.positive import books_tutorial, \
    check_unique_ref_names_with_inheritance, constraints, enforcingInverseReferences, \
    i101, i10, i137_parsing, i14, i17, i18, i19, i23, \
    i40_integers_strings_assignment, i49_parentReduce, i49_resolve_ancestor, \
    i50_stop_following_references, i55, i70, i71, layout, negative, paths, \
    personRelatives, person_tutorial, resolution, simp, telematics, \
    test_neg_typesystem, top_level_constraints_with_relational_joins, i121comments, \
    i122CVL, i126empty, i131incorrectscopediag, i131incorrectscope, \
    i147refdisambiguation, i188sumquantifier, i40textequality, i57navParent, \
    i61cardinalities, i72sharedreference, i78_transitiveclosure, i83individualscope, \
    i84referencespointingtothesameobject, i98_toplevelreferences, \
    referencesshouldbeunique, subtypingprimitivetypes, i205refdisambiguationII


my_tests = [ 
          (multiple_joins, 1),
          (bracketedconstraint_this, 6),
          (this_dot_parent, 2),
          (arithmetic, 2),
          (relations, 1),
          (boolean_connectives, 1),
          (union, 6),
          (simple_abstract, 0),
          (some, 1),
          (simple_set, 6),
          (integer_refs, 1),
          (higher_inheritance, 1),
          (this_integer_relation, 36),
          (equal_references, 2)
         ]

positive_tests = [
        (books_tutorial, 1),
        (check_unique_ref_names_with_inheritance, 1),
        (constraints, 1),
        (enforcingInverseReferences, 1),
        (i101, 1),
        (i10, 1),
        (i121comments, 1),
        (i122CVL, 1),
        (i126empty, 1),
        (i131incorrectscopediag, 1),
        (i131incorrectscope, 1),
        (i137_parsing, 1),
        (i147refdisambiguation, 1),
        (i14, 1),
        (i17, 1),
        (i188sumquantifier, 1),
        (i18, 1),
        (i19, 1),
        (i205refdisambiguationII, 1),
        (i23, 1),
        (i40_integers_strings_assignment, 1),
        (i40textequality, 1),
        (i49_parentReduce, 1),
        (i49_resolve_ancestor, 1),
        (i50_stop_following_references, 1),
        (i55, 1),
        (i57navParent, 1),
        (i61cardinalities, 1),
        (i70, 1),
        (i71, 1),
        (i72sharedreference, 1),
        (i78_transitiveclosure, 1),
        (i83individualscope, 1),
        (i84referencespointingtothesameobject, 1),
        (i98_toplevelreferences, 1),
        (layout, 1),
        (negative, 1),
        (paths, 1),
        (personRelatives, 1),
        (person_tutorial, 1),
        (referencesshouldbeunique, 1),
        (resolution, 1),
        (simp, 1),
        (subtypingprimitivetypes, 1),
        (telematics, 1),
        (test_neg_typesystem, 1),
        (top_level_constraints_with_relational_joins, 1)
                  ]

def run():
    '''
    Runs the Z3-translator on each pair (file, numInstances) in tests, 
    and ensures that the number of generated models equals numInstances.
    '''
    if Options.TEST_SET == Options.MY_TESTS:
        tests = my_tests
    elif Options.TEST_SET == Options.POSITIVE_TESTS:
        tests = positive_tests
    
    count = 0
    for t in tests:
        count = count+1
        (file, expected_model_count) = t
        module = file.getModule()
        print("Attempting: " + str(file))
        z3 = Z3Instance.Z3Instance(module)
        actual_model_count = z3.run()
        
        if(expected_model_count == actual_model_count):
            print("PASSED: " + str(file))
        else:
            print("FAILED: " + str(file) + " " + str(expected_model_count) + " " + str(actual_model_count))
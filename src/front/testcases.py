'''
Created on Mar 12, 2014

@author: ezulkosk
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
    Cruise, small, cc_examplemod
    
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
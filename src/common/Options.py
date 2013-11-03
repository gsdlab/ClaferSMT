'''
Created on Oct 6, 2013

@author: ezulkosk
'''
from common import Common
from test import bracketedconstraint_this, multiple_joins, this_dot_parent, \
    arithmetic, relations, boolean_connectives, union, simple_abstract, some, \
    simple_set, zoo, simple_zoo, integer_refs, phone_feature_model, \
    higher_inheritance, this_integer_relation, equal_references, dag_test, subbooks, \
    int_ref_set, iso, isowithcons, all_alls, some_somes
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

'''
========
| TODO |
========
* Fix any ops left in BracketedConstraint
* Int refs... possible solution: Int ClaferSort (hopefully there is an easier way...) 
* Real Numbers
* Traversal of quantified formulas is exponential...
* Improve support for debugging constraints
* Fix quantifier symmetry breaker, if two locals FROM THE SAME QUANTIFIER are on the left and right of a func, not symmetric
* Documentation
* Scopes
* Change DoubleLiteral to RealLiteral, since that is most likely the Z3 construct that will be used.
'''


GLOBAL_SCOPE = 2 #this obviously has to change

MODE = Common.TEST   # Common.[NORMAL | DEBUG | TEST | ONE | ALL], where ONE outputs one model from each test
PRINT_CONSTRAINTS = True
NUM_INSTANCES = 10 # -1 to produce all instances
INFINITE = -1 #best variable name.
PROFILING = True # True to output the translation time, and time to get first model
CPROFILING = False #invokes the standard python profiling method (see Z3Run.py)
GET_ISOMORPHISM_CONSTRAINT = False
BREAK_QUANTIFIER_SYMMETRY = False
EXTEND_ABSTRACT_SCOPES = True

MY_TESTS = 1 # my tests from debugging
POSITIVE_TESTS = 2 # tests from test/positive in the Clafer repository
TEST_SET = POSITIVE_TESTS 

#MODULE = bracketedconstraint_this.getModule()
#MODULE = multiple_joins.getModule()
#MODULE = this_dot_parent.getModule()
#MODULE = arithmetic.getModule()
#MODULE = relations.getModule()
#MODULE = boolean_connectives.getModule()
#MODULE = union.getModule()
#MODULE = simple_abstract.getModule()
#MODULE = some.getModule()
#MODULE = simple_set.getModule()
#MODULE = zoo.getModule()
#MODULE = simple_zoo.getModule()
#MODULE = integer_refs.getModule()
#MODULE = phone_feature_model.getModule()
#MODULE = higher_inheritance.getModule()
#MODULE = this_integer_relation.getModule()
#MODULE = equal_references.getModule()
#MODULE = dag_test.getModule()
#MODULE = books_tutorial.getModule()
#MODULE = subbooks.getModule()
#MODULE = int_ref_set.getModule()
#MODULE = iso.getModule()
#MODULE = isowithcons.getModule()
#MODULE = all_alls.getModule()
#MODULE = some_somes.getModule()
MODULE = constraints.getModule()

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
          (this_integer_relation, 2),
          (equal_references, 2),
          (all_alls, 1),
          (zoo, INFINITE)
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




'''
Created on Oct 6, 2013

@author: ezulkosk
'''
from common import Common
from test import bracketedconstraint_this, multiple_joins, this_dot_parent, \
    arithmetic, relations, boolean_connectives, union, simple_abstract, some, \
    simple_set, zoo, simple_zoo, integer_refs, phone_feature_model, \
    higher_inheritance, this_integer_relation, equal_references, dag_test

#this obviously has to change
GLOBAL_SCOPE = 5

MODE = Common.NORMAL # 
NUM_INSTANCES = 1 # -1 to produce all instances
PROFILING = False # True to output the translation time, and time to get first model
GET_ISOMORPHISM_CONSTRAINT=False

MY_TESTS = 1
POSITIVE_TESTS = 2
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
MODULE = dag_test.getModule()

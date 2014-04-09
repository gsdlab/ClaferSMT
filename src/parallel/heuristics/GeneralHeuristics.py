'''
Created on Apr 4, 2014

@author: ezulkosk
'''
from common import Common, API
from common.Common import mAnd
from parallel.heuristics.SAP import random_unique_service_random_server
from visitors import CreateBracketedConstraints
import operator
import random
import sys




def no_split(z3inst, module, num_split):
    return [True for _ in range(num_split)]
    
def random_optional_gcard_clafer_toggle(z3inst, module,  num_split):
    '''
    only considers clafers with card = [0,1], AND numInstances = 1
    num_split must be a power of 2
    '''
    assert(Common.is_power2(num_split))
    opts = []
    for i in z3inst.z3_sorts:
        claferSort = z3inst.z3_sorts[i]
        lowerCard = claferSort.lowerCardConstraint
        upperCard = claferSort.upperCardConstraint
        if lowerCard == 0 and upperCard == 1 and claferSort.numInstances == 1 and not claferSort.element.isAbstract:
            opts.append(claferSort)
    random.shuffle(opts)
    constraints = [True]
    try:
        while num_split != 1:
            num_split = num_split // 2
            currSort = opts.pop(0)
            newConstraints = []
            for i in constraints:
                newConstraints.append(mAnd(i, currSort.instances[0] == 0))
            for i in constraints:
                newConstraints.append(mAnd(i, currSort.instances[0] == 1))
            constraints = newConstraints
    except:
        raise HeuristicFailureException("Not enough optionals gcards for heuristic random_optional_gcard_clafer_toggle")
    return constraints

def biggest_range_split(z3inst, module, num_split):
    sys.exit("INCOMPLETE: need to figure out what to do when run out of splits")
    #only consider ranges of top level abstracts that are referring to the same type of concretes
    pairs = []
    for i in z3inst.z3_sorts.values():
        glCardRange = i.numInstances - i.element.glCard[0].value
        pairs.append((i, glCardRange))
    random.shuffle(pairs)
    pairs.sort(key=operator.itemgetter(1))
    pairs.reverse()
    constraints = []
    while num_split > 0 and pairs:
        (claferSort, glRange) = pairs.pop(0)
        for i in range(claferSort.element.glCard[0].value, claferSort.numInstances + 1):
            left = API.createCard(API.createArg(claferSort.element.uid, claferSort))
            right = API.createInteger(i)
            
            bc = CreateBracketedConstraints.CreateBracketedConstraints(z3inst, True)
            constraint = bc.generatedConstraintVisit(API.createEquals(left, right))
            constraints.append(constraint)
            print(constraints)
            sys.exit()
            pass
        num_split = num_split - glRange
    raise HeuristicFailureException("biggest_range_split failed")
        
    print(constraints)
    return constraints
    
def divide_biggest_ranges_in_two(z3inst, module, num_split):
    pass
    
heuristics = {
              "NO_SPLIT" : no_split,
              "random_optional_gcard_clafer_toggle" : random_optional_gcard_clafer_toggle,
              "biggest_range_split" : biggest_range_split,
              "divide_biggest_ranges_in_two" : divide_biggest_ranges_in_two
             }

class HeuristicFailureException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
'''
Created on Apr 4, 2014

@author: ezulkosk
'''
from common import Common
from common.Common import mAnd
from parallel.heuristics.SAP import random_unique_service_random_server
import random
import sys




def no_split(z3inst, module, num_split):
    return [True for _ in range(num_split)]
    
def random_optional_clafer_toggle(z3inst, module,  num_split):
    '''
    only considers clafers with card = [0,1], AND numInstances = 1
    num_split must be a power of 2
    '''
    assert(Common.is_power2(num_split))
    opts = []
    for i in z3inst.z3_sorts:
        claferSort = z3inst.z3_sorts[i]
        print(claferSort)
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
        print("Not enough optionals, fix this")
        return None
    return constraints

def biggest_range_split(z3inst, module, num_split):
    pass
    
    
heuristics = {
              "NO_SPLIT" : no_split,
              "random_optional_clafer_toggle" : random_optional_clafer_toggle,
              "biggest_range_split" : biggest_range_split
             }
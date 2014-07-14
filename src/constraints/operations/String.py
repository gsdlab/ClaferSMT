'''
Created on Jul 14, 2014

@author: ezulkosk
'''
from common import Common, SMTLib
from structures.ExprArg import IntArg, BoolArg
import sys

''' need to improve to handle multiple strings'''

def op_concat(left, right):
    (_, left_mask) = left.getInstanceSort(0)
    left_i = left_mask.get(0)
    (_, right_mask) = right.getInstanceSort(0)
    right_i = right_mask.get(0)
    return IntArg(["Concat$" + left_i + "$" + right_i])

def op_length(arg):
    (_, mask) = arg.getInstanceSort(0)
    arg_i = mask.get(0)
    stringID = Common.STRCONS_SUB + str(Common.getStringUID())
    Common.string_map[stringID] = arg_i
    return IntArg([SMTLib.SMT_Int("Length$" + str(stringID))])

def op_substring(whole_string, left_index, right_index):
    (_, whole_mask) = whole_string.getInstanceSort(0)
    whole_i = whole_mask.get(0)
    left_stringID = Common.STRCONS_SUB + str(Common.getStringUID())
    right_stringID = Common.STRCONS_SUB + str(Common.getStringUID())
    Common.string_map[left_stringID] = left_index
    Common.string_map[right_stringID] = right_index
    return IntArg(["Substring$" + whole_i + "$" + left_stringID + "$" + right_stringID])

def op_replace(whole_string, from_string, to_string):
    (_, whole_mask) = whole_string.getInstanceSort(0)
    whole_i = whole_mask.get(0)
    (_, from_mask) = from_string.getInstanceSort(0)
    from_i = from_mask.get(0)
    (_, to_mask) = to_string.getInstanceSort(0)
    to_i = to_mask.get(0)
    return IntArg(["Replace$" + whole_i + "$" + from_i + "$" + to_i])

def op_split(left, right):
    sys.exit("Split not implemented.")

def op_contains(left, right):
    (_, left_mask) = left.getInstanceSort(0)
    left_i = left_mask.get(0)
    (_, right_mask) = right.getInstanceSort(0)
    right_i = right_mask.get(0)
    return BoolArg(["Contains$" + left_i + "$" + right_i])

def op_indexof(left, right):
    (_, mask) = left.getInstanceSort(0)
    left_i = mask.get(0)
    (_, mask) = right.getInstanceSort(0)
    right_i = mask.get(0)
    return IntArg([SMTLib.SMT_Int("Indexof$" + left_i + "$" + right_i)])

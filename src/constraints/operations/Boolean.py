'''
Created on Jul 14, 2014

@author: ezulkosk
'''
from common import SMTLib
from common.Common import mAnd, mOr
from constraints.operations.Set import op_implies
from structures.ExprArg import ExprArg, BoolArg


def op_not(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Boolean negation of arg.
    '''
    assert isinstance(arg, ExprArg)
    (_, mask) = arg.getInstanceSort(0)
    val = mask.pop_value()
    return BoolArg(SMTLib.SMT_Not(val))

def op_and(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean conjunction of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg(mAnd(lval, rval))  

def op_or(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean disjunction of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg(mOr(lval, rval))  

def op_xor(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean XOR of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg(SMTLib.SMT_Xor(lval, rval))  

def op_equivalence(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that an element of left is *on* iff it is *on* in right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg(SMTLib.SMT_And(op_implies(left, right).getBool(), op_implies(right,left).getBool()))

def op_ifthenelse(cond, ifExpr, elseExpr):
    '''
    :param cond:
    :type cond: :class:`~ExprArg`
    :param ifExpr:
    :type ifExpr: :class:`~ExprArg`
    :param elseExpr:
    :type elseExpr: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Returns the corresponding Z3 If-construct over the instances of the arguments.
    '''
    assert isinstance(cond, ExprArg)
    assert isinstance(ifExpr, ExprArg)
    assert isinstance(elseExpr, ExprArg)
    
    (_, cond_mask) = cond.getInstanceSort(0)
    (_, if_mask) = ifExpr.getInstanceSort(0)
    (_, else_mask) = elseExpr.getInstanceSort(0)
    return BoolArg(SMTLib.SMT_If(cond_mask.pop_value(), if_mask.pop_value(), else_mask.pop_value()))


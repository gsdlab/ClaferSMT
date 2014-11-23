'''
Created on Jul 14, 2014

@author: ezulkosk
'''
from common import SMTLib
from common.Common import mAnd, mOr
from constraints.operations.Set import op_implies
from structures.ExprArg import ExprArg, BoolArg, IntArg


def op_not(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Boolean negation of arg.
    '''
    assert isinstance(arg, ExprArg)
    val = arg.getBool()
    return BoolArg(SMTLib.createNot(val))

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
    lval = left.getBool()
    rval = right.getBool()
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
    lval = left.getBool()
    rval = right.getBool()
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
    lval = left.getBool()
    rval = right.getBool()
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
    return BoolArg(mAnd(op_implies(left, right).getBool(), op_implies(right,left).getBool()))

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
    
    condVal = cond.getBool()
    if isinstance(ifExpr, IntArg):
        ifExprVal = ifExpr.getInts()[0][0]
        elseExprVal = elseExpr.getInts()[0][0]
        return IntArg(SMTLib.SMT_If(condVal, ifExprVal, elseExprVal))
    else:
        ifExprVal = ifExpr.getBool()
        elseExprVal = elseExpr.getBool()
        return BoolArg(SMTLib.SMT_If(condVal, ifExprVal, elseExprVal))


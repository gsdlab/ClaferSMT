'''
Created on Jul 14, 2014

@author: ezulkosk
'''
from common import SMTLib
from structures.ExprArg import ExprArg, IntArg, BoolArg
import sys

def getArithValue(vals):
    return SMTLib.SMT_Sum(vals)

def op_add(left,right):
    '''
    :param left:
    :type left: :class:`~IntArg`
    :param right:
    :type right: :class:`~IntArg`
    :returns: :class:`~IntArg` 
    
    Returns left + right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    lval = left.getInt()
    rval = right.getInt()
    return IntArg(SMTLib.SMT_Plus(lval, rval))  

def op_sub(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left - right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    lval = left.getInt()
    rval = right.getInt()
    return IntArg(SMTLib.SMT_Minus(lval, rval))  

def op_mul(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left * right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    lval = left.getInt()
    rval = right.getInt()
    return IntArg(SMTLib.SMT_Times(lval, rval))  

#integer division
def op_div(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    Returns left / right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    lval = left.getInt()
    rval = right.getInt()
    return IntArg(SMTLib.SMT_Divide(lval, rval)
                   if((not isinstance(lval, SMTLib.SMT_IntConst)) or (not isinstance(rval, SMTLib.SMT_IntConst)))
                             else SMTLib.SMT_IntDivide(lval, rval))
    
    
def op_un_minus(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Negates arg.
    '''
    assert isinstance(arg, IntArg)
    val = arg.getInt()
    return IntArg(SMTLib.SMT_Neg(val))  
   
def op_sum(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    Computes the sum of all integer instances in arg. May not match the semantics of the Alloy backend.
    '''
    sys.exit("sum TODO need to figure out new semantics of cardinalityMasks")
    assert isinstance(arg, ExprArg)
    all_vals = []
    for i in arg.getInstanceSorts():
        (_, mask) = i
        all_vals.append(getArithValue(list(mask.values())))
    return IntArg(getArithValue(all_vals))

def op_lt(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left < right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    lval = left.getInt()
    rval = right.getInt()
    return BoolArg(SMTLib.SMT_LT(lval, rval))  
        
def op_le(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    Invariant: left and right have exactly one int
    Ensures that the left <= right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    lval = left.getInt()
    rval = right.getInt()
    return BoolArg(SMTLib.SMT_LE(lval, rval))  

def op_gt(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left > right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_lt(right, left)

def op_ge(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left >= right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_le(right, left)


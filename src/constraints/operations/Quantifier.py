'''
Created on Jul 14, 2014

@author: ezulkosk
'''
from common import SMTLib, Common
from common.Common import mOr, mAnd
from structures.ExprArg import BoolArg

def getQuantifierConditionList(exprs):
    '''
    Iterates over all values in all masks, 
    and returns a list of Booleans, indicating whether
    each instance is on (or true), or not. 
    '''
    finalList = []
    for i in exprs:
        for expr in i:
            if isinstance(expr, BoolArg):
                finalList.append(expr.getBool())
                continue
            condList = []
            for k in expr.getInstances().values():
                (e, pol) = k
                if pol != Common.DEFINITELY_ON:
                    condList.append(e)
                else:
                    condList.append(SMTLib.SMT_BoolConst(True))
                    break
            finalList.append(mOr(*condList))
    return finalList

def quant_some(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [mAnd(i, j) for i,j in zip(ifConstraints, condList)]
    return mOr(*condList)

def quant_all(exprs, ifConstraints):
    
    
    if ifConstraints:
        cond = mAnd(*[SMTLib.SMT_Implies(i, j[0].getBool()) for i,j in zip(ifConstraints,exprs)])
    else:
        cond = mAnd(*[i[0].getBool() for i in exprs])
    return cond

def quant_no(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [mAnd(i, j) for i,j in zip(ifConstraints, condList)]
    return SMTLib.createNot(mOr(*condList))

EXPR = ""
EXPR2 = ""

def quant_one(exprs, ifConstraints):
    '''
    There's probably a better way to do this.
    '''
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [mAnd(i, j) for i,j in zip(ifConstraints, condList)]
    exprList = []
    for i in range(len(condList)):
        exprList.append(SMTLib.SMT_If(condList[i], SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
    return SMTLib.SMT_EQ(SMTLib.createSum(*exprList), SMTLib.SMT_IntConst(1))
    
def quant_lone(exprs, ifConstraints):
    return SMTLib.SMT_Or(quant_no(exprs, ifConstraints), quant_one(exprs, ifConstraints))
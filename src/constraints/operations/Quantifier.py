'''
Created on Jul 14, 2014

@author: ezulkosk
'''
from common import SMTLib
from common.Common import mOr, mAnd

def getQuantifierConditionList(exprs):
    '''
    Iterates over all values in all masks, 
    and returns a list of Booleans, indicating whether
    each instance is on (or true), or not. 
    '''
    finalList = []
    for i in exprs:
        for expr in i:
            condList = []
            for k in expr.getInstanceSorts():
                (sort, mask) = k
                for l in mask.keys():
                    condList.append(sort.isOn(mask.get(l)))

            finalList.append(mOr(*condList))
    return finalList

def quant_some(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [SMTLib.SMT_And(i, j) for i,j in zip(ifConstraints, condList)]
    return mOr(*condList)

def quant_all(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [SMTLib.SMT_Implies(i, j) for i,j in zip(ifConstraints, condList)]
    return mAnd(*condList)

def quant_no(exprs, ifConstraints):
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [SMTLib.SMT_And(i, j) for i,j in zip(ifConstraints, condList)]
    return SMTLib.SMT_Not(SMTLib.SMT_Or(*condList))

EXPR = ""
EXPR2 = ""

def quant_one(exprs, ifConstraints):
    '''
    There's probably a better way to do this.
    '''
    condList = getQuantifierConditionList(exprs)
    if ifConstraints:
        condList = [SMTLib.SMT_And(i, j) for i,j in zip(ifConstraints, condList)]
    exprList = []
    for i in range(len(condList)):
        exprList.append(SMTLib.SMT_If(condList[i], SMTLib.SMT_IntConst(1), SMTLib.SMT_IntConst(0)))
    return SMTLib.SMT_EQ(SMTLib.SMT_Sum(*exprList), SMTLib.SMT_IntConst(1))
    
def quant_lone(exprs, ifConstraints):
    return SMTLib.SMT_Or(quant_no(exprs, ifConstraints), quant_one(exprs, ifConstraints))
'''
Created on Apr 8, 2014

@author: ezulkosk
'''
from ast import Exp, ClaferId, LocalDeclaration, IntegerLiteral, Declaration, \
    FunExp, DeclPExp


zero_pos = ((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), 
            (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))

def createArg(arg_id, clafersort = None):
        return Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=zero_pos, \
                       iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id=arg_id, isTop=False, claferSort=clafersort)]) 
    
def createLocalDecl(arg):
    return LocalDeclaration.LocalDeclaration(arg)

def createInteger(arg):
    return IntegerLiteral.IntegerLiteral(int(arg))

def createDeclaration(local, sort):
    return Declaration.Declaration(isDisjunct=False, localDeclarations=local,  body=
    Exp.Exp(expType="Body", exptype="Set", parentId="", pos=zero_pos, iExpType="IClaferId", \
            iExp=[ClaferId.ClaferId(moduleName="", my_id=sort, isTop=True)]))

def createFunExpr(op, elems):
    return FunExp.FunExp(operation = op, elements=elems) 

def createJoin(left, right):
    return createFunExpr(".", [left,right])
 
def createCard(arg):
    return createFunExpr("#", [arg])  

def createEquals(left, right):
    return createFunExpr("=", [left,right])  

def createLE(left, right):
    return createFunExpr("<=", [left,right])  

def createLT(left, right):
    return createFunExpr("<", [left,right])  

def createIn(left, right):
    return createFunExpr("in", [left,right])   

def createNotEquals(self, left, right):
    return createFunExpr("!=", [left,right])   

def createAnd(self, left, right):
    return createFunExpr("&&", [left,right])   

def createNot(self, arg):
    return createFunExpr("!", [arg])  

def createSome(self, decl):
    return DeclPExp.DeclPExp(quantifier="Some", declaration=decl, bodyParentExp=None)
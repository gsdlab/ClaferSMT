'''
Created on Mar 26, 2013

@author: ezulkosk
'''
import ast.Clafer, ast.Module, ast.ClaferId, ast.Constraint, ast.Declaration, ast.DeclPExp, ast.Exp, \
      ast.FunExp, ast.GCard, ast.Goal, ast.LocalDeclaration, ast.Supers, ast.IntegerLiteral, ast.DoubleLiteral, \
      ast.StringLiteral



def visit(visitor, element):
    if isinstance(element, ast.Clafer.Clafer):
        visitor.claferVisit(element)
    elif isinstance(element, ast.ClaferId.ClaferId):
        visitor.claferidVisit(element)
    elif isinstance(element, ast.Constraint.Constraint):
        visitor.constraintVisit(element)
    elif isinstance(element, ast.Declaration.Declaration):
        visitor.declarationVisit(element)
    elif isinstance(element, ast.DeclPExp.DeclPExp):
        visitor.declpexpVisit(element)
    elif isinstance(element, ast.Exp.Exp):
        visitor.expVisit(element)
    elif isinstance(element, ast.FunExp.FunExp):
        visitor.funexpVisit(element)
    elif isinstance(element, ast.GCard.GCard):
        visitor.gcardVisit(element)
    elif isinstance(element, ast.Goal.Goal):
        visitor.goalVisit(element)
    elif isinstance(element, ast.LocalDeclaration.LocalDeclaration):
        visitor.localdeclarationVisit(element)
    elif isinstance(element, ast.Module.Module):
        visitor.moduleVisit(element)
    elif isinstance(element, ast.Supers.Supers):
        visitor.supersVisit(element)
    elif isinstance(element, ast.IntegerLiteral.IntegerLiteral):
        visitor.integerliteralVisit(element)
    elif isinstance(element, ast.DoubleLiteral.DoubleLiteral):
        visitor.doubleliteralVisit(element)
    elif isinstance(element, ast.StringLiteral.StringLiteral):
        visitor.stringliteralVisit(element)
    elif element == None:
        visitor.noneVisit()
    else:
        print("Error")
    
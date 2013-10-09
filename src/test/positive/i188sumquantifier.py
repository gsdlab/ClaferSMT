from ast import Module
from ast import GCard
from ast import Supers
from ast import Clafer
from ast import Exp
from ast import Declaration
from ast import LocalDeclaration
from ast import IRConstraint
from ast import FunExp
from ast import ClaferId
from ast import DeclPExp
from ast import Goal

from ast import IntegerLiteral
from ast import DoubleLiteral
from ast import StringLiteral
def getModule():
	stack = []
	module = Module.Module("")
	stack.append(module)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="a"
	uid="c1_a"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Ref", parentId="", pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c2_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(9))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="in", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c3_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(4))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(9))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c4_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(9))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_a", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(9))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(9))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="in", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(4))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(9))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(9))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_a", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(9))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(21)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="b"
	uid="c8_b"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Ref", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(13))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(21))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="sum", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(21))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_a", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c8_b", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c17_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c20_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c21_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c22_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(8))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(4))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c23_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(4))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c8_b", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(4))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c24_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(8))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])]))
	stack[-1].addElement(constraint)
	return module
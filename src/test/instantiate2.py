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
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="A"
	uid="c1_A"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(2))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(2))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="B"
	uid="c2_B"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(3))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(6))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="C"
	uid="c3_C"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(2))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(12))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c4_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(12))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(8))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(8))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(6))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(4))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(6))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(8))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_C", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(12))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(15)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="a0"
	uid="c12_a0"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(30))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("x")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(17))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c17_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(30))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(26))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(26))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c20_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(24))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c21_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(25)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(26))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_C", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c22_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(29)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(30))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c23_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(15))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c24_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c25_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c26_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(9))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c27_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(11))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c28_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(15))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c29_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(8))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c30_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(4))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c31_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(4))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c32_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(8))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))
	stack[-1].addElement(constraint)
	return module
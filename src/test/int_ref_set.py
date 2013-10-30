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
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(23)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="D"
	uid="c1_D"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Ref", parentId="", pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))
	globalCard=(IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(6)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="A"
	uid="c2_A"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(6))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_D", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(6)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="B"
	uid="c3_B"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(6))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_D", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(6)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="C"
	uid="c4_C"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(6))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_D", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(3))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(11))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(3))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_B", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(11))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c17_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(3))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c4_C", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(11))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(3)])])]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(8)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="E"
	uid="c20_E"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Ref", parentId="", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(8))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="int", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c21_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c22_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c23_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(3))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c20_E", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c24_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c25_exp", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(11))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c26_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c27_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(25))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="--", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c28_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(16))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="--", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c29_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c30_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(3))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_D", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c31_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c32_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(16))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c33_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c34_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(16))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c35_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(25))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c36_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c20_E", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c37_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(25))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c38_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(28)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(29))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(5)])])]))
	stack[-1].addElement(constraint)
	return module
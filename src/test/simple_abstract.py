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
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(10)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="B"
	uid="c1_B"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(3))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(7)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="cost"
	uid="c2_cost"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(10)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="value"
	uid="c3_value"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(21)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="A"
	uid="c4_A"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(4))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_B", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(3))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(21))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(17))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(17))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(11))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(12)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(17))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_value", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(21))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(13))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(9))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(9))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(4))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c4_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(9))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_cost", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(12)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(13))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])]))
	stack[-1].addElement(constraint)
	return module
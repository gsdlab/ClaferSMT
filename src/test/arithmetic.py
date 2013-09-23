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
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(36)))
	isAbstract=False
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
	pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(9)))
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
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c3_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c4_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(9))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="/", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(31))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="*", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(24))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="-", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(17))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(4)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(21)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(24))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="+", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(21)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(22))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(24))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(29)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(31))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(10)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(35)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(36))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(5)])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
	return module
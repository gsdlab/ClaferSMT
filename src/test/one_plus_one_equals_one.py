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
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(15)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="A"
	uid="c1_A"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c2_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(15))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c3_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c4_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(11))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(15))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(24))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="++", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(7))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(12))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(24))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(20))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c17_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(21)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(24))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))
	stack[-1].addElement(constraint)
	return module
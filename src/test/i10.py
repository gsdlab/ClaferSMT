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
	pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(28)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="A"
	uid="c1_A"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(28)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="x"
	uid="c2_x"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(20))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c3_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(28))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=">=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(23))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c4_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(27)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(28))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(0)])])]))
	stack[-1].addElement(constraint)
	stack.pop()
	stack.pop()
	return module
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
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(16)))
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
	pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="B"
	uid="c2_B"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Ref", parentId="", pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(2))
	globalCard=(IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(2))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c3_exp", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(44))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("a")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_A", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(44))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(17))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="a", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_B", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(44))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(31))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(27))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(27))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(31))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(35)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(44))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(35)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(40))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c17_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(35)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(36))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(37)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(40))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(43)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(44))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])])])]))]))]))
	stack[-1].addElement(constraint)
	return module
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
	pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="AliceAge"
	uid="c1_AliceAge"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(16))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="int", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c2_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_AliceAge", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c4_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c5_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c6_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c7_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="BobAge"
	uid="c11_BobAge"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="int", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c11_BobAge", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c17_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c20_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(15)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="BobsBirthday"
	uid="c21_BobsBirthday"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c22_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(57))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c23_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(52))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=>else", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c24_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(18))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c25_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(18))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c21_BobsBirthday", isTop=True)]))]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c26_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(34))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c27_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(30))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c11_BobAge", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c28_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(31)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(34))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c29_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(40)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(52))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c30_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(40)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(48))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_AliceAge", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c31_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(49)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(52))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c32_exp", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(56)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(57))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(5)])])]))
	stack[-1].addElement(constraint)
	return module
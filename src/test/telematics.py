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
	pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(29)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="options"
	uid="c1_options"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=True, interval=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)))
	id="size"
	uid="c2_size"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="small"
	uid="c3_small"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="large"
	uid="c4_large"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(20)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="cache"
	uid="c5_cache"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(20)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="size"
	uid="c6_size"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(20)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="fixed"
	uid="c7_fixed"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c8_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=>", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c9_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c10_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(11))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c11_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_size", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_small", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c12_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(20))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c13_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c5_cache", isTop=False)])])]))])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c14_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(29))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c5_cache", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c6_size", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c7_fixed", isTop=False)])])]))])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(30)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="comp"
	uid="c16_comp"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(30)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="version"
	uid="c17_version"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(22))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="integer", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(30))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c17_version", isTop=False)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c20_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(25)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(30))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="+", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c21_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(25)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(26))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c22_exp", pos=((IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(29)), (IntegerLiteral.IntegerLiteral(15),IntegerLiteral.IntegerLiteral(30))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(20)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="ECU"
	uid="c23_ECU"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(20))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c16_comp", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(19),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(36)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="display"
	uid="c24_display"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(19),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(19),IntegerLiteral.IntegerLiteral(24))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c16_comp", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(20),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(20),IntegerLiteral.IntegerLiteral(18)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="server"
	uid="c25_server"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(20),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(20),IntegerLiteral.IntegerLiteral(18))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c23_ECU", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c26_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c25_server", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c28_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c29_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c30_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c31_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c32_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c33_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c34_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(21),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(21),IntegerLiteral.IntegerLiteral(13)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="options"
	uid="c35_options"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_options", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c36_exp", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=">=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c37_exp", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(18))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c38_exp", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(10))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(18))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c39_exp", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(18))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c17_version", isTop=False)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(18))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c40_exp", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c41_exp", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(28))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c25_server", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c42_exp", pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(29)), (IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c17_version", isTop=False)]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(30),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="plaECU"
	uid="c43_plaECU"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(30),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(30),IntegerLiteral.IntegerLiteral(22))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c23_ECU", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="display"
	uid="c44_display"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c24_display", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(2))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c45_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c46_exp", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(25))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c47_exp", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(16))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c25_server", isTop=False)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c48_exp", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(25))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="parent", isTop=True)])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c49_exp", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="No", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c50_exp", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c51_exp", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(18))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c35_options", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c52_exp", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c5_cache", isTop=False)])])]))])])]))
	stack[-1].addElement(constraint)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(35),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(35),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="ECU1"
	uid="c53_ECU1"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(35),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(35),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c43_plaECU", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(38),IntegerLiteral.IntegerLiteral(19)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="ECU2"
	uid="c54_ECU2"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(8)), (IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c43_plaECU", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(38),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(38),IntegerLiteral.IntegerLiteral(19)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="master"
	uid="c55_master"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", my_type="", parentId="", pos=((IntegerLiteral.IntegerLiteral(38),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(38),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c53_ECU1", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c56_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c55_master", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c58_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c59_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c60_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c61_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c62_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c63_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c64_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(42),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(50)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="telematicsSystem"
	uid="c65_telematicsSystem"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(45),IntegerLiteral.IntegerLiteral(13)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=True, interval=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)))
	id="channel"
	uid="c66_channel"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(44),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(44),IntegerLiteral.IntegerLiteral(15)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="single"
	uid="c67_single"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(45),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(45),IntegerLiteral.IntegerLiteral(13)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="dual"
	uid="c68_dual"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(47),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(47),IntegerLiteral.IntegerLiteral(19)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="extraDisplay"
	uid="c69_extraDisplay"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(49),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(51),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=True, interval=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)))
	id="size"
	uid="c70_size"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(50),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(50),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="small"
	uid="c71_small"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(51),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(51),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="large"
	uid="c72_large"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c73_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c74_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c75_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c76_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c77_exp", pos=((IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c78_exp", pos=((IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(10))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c79_exp", pos=((IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(10))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c66_channel", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c68_dual", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c80_exp", pos=((IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(19))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c81_exp", pos=((IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(53),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c54_ECU2", isTop=True)]))])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c82_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(40))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c83_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(18))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c84_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(18))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c69_extraDisplay", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c85_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(40))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c86_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c87_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c88_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(28))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c53_ECU1", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c89_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(29)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(36))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c44_display", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c90_exp", pos=((IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(39)), (IntegerLiteral.IntegerLiteral(54),IntegerLiteral.IntegerLiteral(40))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c91_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(49))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c92_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(18))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c93_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(18))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c69_extraDisplay", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c94_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(49))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=>", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c95_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(28))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c96_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(28))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c54_ECU2", isTop=True)]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c97_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(49))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c98_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(45))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="#", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c99_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(33)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(45))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c100_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(33)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(37))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c54_ECU2", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c101_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(38)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(45))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c44_display", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", my_type="Integer", parentId="c102_exp", pos=((IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(48)), (IntegerLiteral.IntegerLiteral(55),IntegerLiteral.IntegerLiteral(49))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(2)])])])])])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c103_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(50))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c104_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(11))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c105_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c70_size", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c72_large", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c106_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(50))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="No", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c107_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(50))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c108_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(44))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c109_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(39))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c110_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(31))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c111_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c43_plaECU", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c112_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(31))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c44_display", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c113_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(39))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c35_options", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c114_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(40)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(44))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_size", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c115_exp", pos=((IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(45)), (IntegerLiteral.IntegerLiteral(56),IntegerLiteral.IntegerLiteral(50))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_small", isTop=False)])])]))])])])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c116_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(50))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c117_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(11))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c118_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(6)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(11))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c70_size", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c71_small", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c119_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(50))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="No", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c120_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(50))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c121_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(44))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c122_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(39))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c123_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(31))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c124_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c43_plaECU", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c125_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(31))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c44_display", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c126_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(39))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c35_options", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c127_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(40)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(44))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_size", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c128_exp", pos=((IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(45)), (IntegerLiteral.IntegerLiteral(57),IntegerLiteral.IntegerLiteral(50))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c4_large", isTop=False)])])]))])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c129_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c130_exp", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c131_exp", pos=((IntegerLiteral.IntegerLiteral(60),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(60),IntegerLiteral.IntegerLiteral(6))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c132_exp", pos=((IntegerLiteral.IntegerLiteral(60),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(60),IntegerLiteral.IntegerLiteral(6))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c65_telematicsSystem", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c66_channel", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c68_dual", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c133_exp", pos=((IntegerLiteral.IntegerLiteral(61),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(61),IntegerLiteral.IntegerLiteral(14))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c134_exp", pos=((IntegerLiteral.IntegerLiteral(61),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(61),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c65_telematicsSystem", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c69_extraDisplay", isTop=False)])])]))])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c135_exp", pos=((IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(29))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c136_exp", pos=((IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c137_exp", pos=((IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(23))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c138_exp", pos=((IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(18))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c65_telematicsSystem", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c139_exp", pos=((IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c70_size", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c140_exp", pos=((IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(62),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c72_large", isTop=False)])])]))])])]))
	stack[-1].addElement(constraint)
	return module
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
	pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Type"
	uid="c0_Type"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Optional"
	uid="c0_Optional"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Type", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Mandatory"
	uid="c0_Mandatory"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Type", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(38)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Feature"
	uid="c0_Feature"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(12))
	globalCard=(IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(12))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(15)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="type"
	uid="c0_type"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(15))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Type", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(12))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e0_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_type", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e2_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e3_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e4_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e5_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e6_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e7_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e8_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e9_", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(52))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e10_", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e11_", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(8))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_type", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e12_", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Optional", isTop=True)])])]),
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e13_", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(52))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="in", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e14_", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(28))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(52))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e15_", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(52))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_OptionalCardFeatures", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(52))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e16_", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(54))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e17_", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(20))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e18_", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(8))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_type", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e19_", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(20))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Mandatory", isTop=True)])])]),
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e20_", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(25)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(54))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="in", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e21_", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(25)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(33)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(54))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e22_", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(33)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(54))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_MandatoryCardFeatures", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(33)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(54))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="level"
	uid="c0_level"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(14))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="int", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(12))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(46)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="parent_feature"
	uid="c0_parent_feature"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(21)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(28))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(12))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e23_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(46))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e24_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e25_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(7)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(13))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="parent", isTop=True)])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e26_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e27_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(46))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="+", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e28_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(42))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e29_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(36))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e30_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(37)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(42))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e31_", pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(45)), (IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(46))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(1)])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e32_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_parent_feature", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e34_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e35_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e36_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e37_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e38_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e39_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e40_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e41_", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(15))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=">=", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e42_", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(10))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e43_", pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(15))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(0)])])]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e44_", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(33))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="<=>", elements=[
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e45_", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=">", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e46_", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(10))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e47_", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(14))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(0)])])]),
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e48_", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(33))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Set", parentId="e49_", pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(33))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_parent_feature", isTop=False)])])]))])])]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e50_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(38))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=>", elements=[
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e51_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e52_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(10))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e53_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(13)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(14))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(0)])])]),
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e54_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(38))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e55_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(26))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e56_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(22))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_type", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e57_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(26))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e58_", pos=((IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(29)), (IntegerLiteral.IntegerLiteral(14),IntegerLiteral.IntegerLiteral(38))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Mandatory", isTop=True)])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(34)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="OptionalCardFeatures"
	uid="c0_OptionalCardFeatures"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(25)), (IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(32))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(4))
	globalCard=(IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(4))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e59_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_OptionalCardFeatures", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e61_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e62_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e63_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e64_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e65_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e66_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e67_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(35)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="MandatoryCardFeatures"
	uid="c0_MandatoryCardFeatures"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(26)), (IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(33))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(8))
	globalCard=(IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e68_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_MandatoryCardFeatures", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e70_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e71_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e72_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e73_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e74_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e75_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e76_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="ConType"
	uid="c0_ConType"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Include"
	uid="c0_Include"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_ConType", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Exclude"
	uid="c0_Exclude"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_ConType", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(22),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(26)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Constraint"
	uid="c0_Constraint"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))
	globalCard=(IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(23),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(23),IntegerLiteral.IntegerLiteral(21)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="conType"
	uid="c0_conType"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(23),IntegerLiteral.IntegerLiteral(14)), (IntegerLiteral.IntegerLiteral(23),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_ConType", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e77_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_conType", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e79_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e80_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e81_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e82_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e83_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e84_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e85_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(24),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(24),IntegerLiteral.IntegerLiteral(18)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="left"
	uid="c0_left"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(24),IntegerLiteral.IntegerLiteral(11)), (IntegerLiteral.IntegerLiteral(24),IntegerLiteral.IntegerLiteral(18))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e86_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_left", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e88_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e89_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e90_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e91_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e92_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e93_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e94_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(19)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="right"
	uid="c0_right"
	my_supers = Supers.Supers(isOverlapping=True, elements=[
		Exp.Exp(expType="Super", exptype="", parentId="", pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(12)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(3))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e95_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_right", isTop=False)])])])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e97_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e98_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e99_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e100_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e101_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e102_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e103_", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e104_", pos=((IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(26))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e105_", pos=((IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(13))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e106_", pos=((IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(9))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_left", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e107_", pos=((IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(10)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(13))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e108_", pos=((IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(26))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e109_", pos=((IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(22))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_right", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e110_", pos=((IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(23)), (IntegerLiteral.IntegerLiteral(26),IntegerLiteral.IntegerLiteral(26))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e111_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(140))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="No", declaration=
		Declaration.Declaration(isDisjunct=True, localDeclarations=[LocalDeclaration.LocalDeclaration("x"), LocalDeclaration.LocalDeclaration("y")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Constraint", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e113_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(140))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e114_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(81))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="||", elements=[
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e115_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(53))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e116_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(40))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e117_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(36))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e118_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(31))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e119_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(36))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_left", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e120_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(37)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(40))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e121_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(43)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(53))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e122_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(43)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(49))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e123_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(43)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(44))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e124_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(45)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(49))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_left", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e125_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(50)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(53))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e126_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(57)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(81))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e127_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(57)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(67))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e128_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(57)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(63))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e129_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(57)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(58))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e130_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(59)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(63))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_left", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e131_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(64)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(67))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e132_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(70)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(81))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e133_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(70)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(77))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e134_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(70)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(71))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e135_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(72)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(77))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_right", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e136_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(78)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(81))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])]),
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e137_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(87)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(140))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="||", elements=[
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e138_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(87)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(111))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e139_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(87)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(98))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e140_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(87)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(94))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e141_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(87)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(88))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e142_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(89)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(94))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_right", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e143_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(95)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(98))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e144_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(101)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(111))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e145_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(101)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(107))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e146_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(101)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(102))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e147_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(103)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(107))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_left", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e148_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(108)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(111))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Boolean", parentId="e149_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(115)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(140))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e150_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(115)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(126))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e151_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(115)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(122))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e152_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(115)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(116))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="x", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e153_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(117)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(122))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_right", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e154_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(123)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(126))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e155_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(129)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(140))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e156_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(129)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(136))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e157_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(129)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(130))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="y", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e158_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(131)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(136))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_right", isTop=False)])])]),
		Exp.Exp(expType="Argument", exptype="Set", parentId="e159_", pos=((IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(137)), (IntegerLiteral.IntegerLiteral(29),IntegerLiteral.IntegerLiteral(140))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])])])])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e160_", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(31))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="One", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("f")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e162_", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(31))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e163_", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(27))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e164_", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="f", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(27))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e165_", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(27))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(27))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e166_", pos=((IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(30)), (IntegerLiteral.IntegerLiteral(32),IntegerLiteral.IntegerLiteral(31))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(0)])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e167_", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(33))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("f")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e169_", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(33))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="=", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e170_", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e171_", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="f", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e172_", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e173_", pos=((IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(33),IntegerLiteral.IntegerLiteral(33))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(6)])])]))]))
	stack[-1].addElement(constraint)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", exptype="Boolean", parentId="e174_", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(33))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="No", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("f")],  body=
		Exp.Exp(expType="Body", exptype="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_Feature", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", exptype="Boolean", parentId="e176_", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(33))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=">", elements=[
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e177_", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e178_", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(22)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(23))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="f", isTop=True)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(29))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", exptype="Set", parentId="e179_", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c0_level", isTop=False)]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(24)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(29))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="ref", isTop=False)])])])])]),
		Exp.Exp(expType="Argument", exptype="Integer", parentId="e180_", pos=((IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(32)), (IntegerLiteral.IntegerLiteral(34),IntegerLiteral.IntegerLiteral(33))), iExpType="IIntExp", iExp=[IntegerLiteral.IntegerLiteral(6)])])]))]))
	stack[-1].addElement(constraint)
	return module
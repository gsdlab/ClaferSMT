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
	pos=((IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(11)))
	isAbstract=True
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="Phone"
	uid="c1_Phone"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(2),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(10)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="networking"
	uid="c2_networking"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(3),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="wifi"
	uid="c3_wifi"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(4),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="typeB"
	uid="c4_typeB"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(5),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="typeG"
	uid="c5_typeG"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(6),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="typeN"
	uid="c6_typeN"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(7),IntegerLiteral.IntegerLiteral(16)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="bluetooth"
	uid="c7_bluetooth"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(8),IntegerLiteral.IntegerLiteral(13)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="mobile"
	uid="c8_mobile"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(9),IntegerLiteral.IntegerLiteral(10)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="nfc"
	uid="c9_nfc"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(10),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=True, interval=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1)))
	id="location"
	uid="c10_location"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(11),IntegerLiteral.IntegerLiteral(13)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="gps"
	uid="c11_gps"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(5)), (IntegerLiteral.IntegerLiteral(12),IntegerLiteral.IntegerLiteral(14)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="agps"
	uid="c12_agps"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(8))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(3)), (IntegerLiteral.IntegerLiteral(13),IntegerLiteral.IntegerLiteral(11)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="gpu"
	uid="c13_gpu"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="clafer", isTop=False)])])
	card=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(2))
	globalCard=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(16))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
	stack.pop()
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(7)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="PhoneWithGps"
	uid="c14_PhoneWithGps"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(17),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_Phone", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c15_exp", pos=((IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(7))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c16_exp", pos=((IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(18),IntegerLiteral.IntegerLiteral(7))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c10_location", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c11_gps", isTop=False)])])]))]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(24),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(25)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="PhoneWithWifi"
	uid="c17_PhoneWithWifi"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(24),IntegerLiteral.IntegerLiteral(17)), (IntegerLiteral.IntegerLiteral(24),IntegerLiteral.IntegerLiteral(22))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_Phone", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c18_exp", pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(25))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c19_exp", pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(25))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c20_exp", pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(19))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c21_exp", pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(14))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_networking", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c22_exp", pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(15)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_wifi", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c23_exp", pos=((IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(25),IntegerLiteral.IntegerLiteral(25))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c6_typeN", isTop=False)])])]))]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(30),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(37)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="PhonewithWifiAndGpsNoBluetoothOrNfc"
	uid="c24_PhonewithWifiAndGpsNoBluetoothOrNfc"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(30),IntegerLiteral.IntegerLiteral(39)), (IntegerLiteral.IntegerLiteral(30),IntegerLiteral.IntegerLiteral(44))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_Phone", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c25_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(37))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c26_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(15))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="&&", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c27_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(8))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c28_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(8))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_networking", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c3_wifi", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c29_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(12)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(15))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c30_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(12)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(15))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c10_location", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c11_gps", isTop=False)])])]))])])]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c31_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(19)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(37))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="!", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c32_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(21)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(37))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation="||", elements=[
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c33_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(21)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(30))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c34_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(21)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(30))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_networking", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c7_bluetooth", isTop=False)])])]))]),
		Exp.Exp(expType="Argument", my_type="Boolean", parentId="c35_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(34)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(37))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c36_exp", pos=((IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(34)), (IntegerLiteral.IntegerLiteral(31),IntegerLiteral.IntegerLiteral(37))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_networking", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c9_nfc", isTop=False)])])]))])])])])])])]))
	stack[-1].addElement(constraint)
	stack.pop()
##### clafer #####
	pos=((IntegerLiteral.IntegerLiteral(36),IntegerLiteral.IntegerLiteral(1)), (IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(12)))
	isAbstract=False
	groupCard = GCard.GCard(isKeyword=False, interval=(IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(-1)))
	id="PhoneWithGpu"
	uid="c37_PhoneWithGpu"
	my_supers = Supers.Supers(isOverlapping=False, elements=[
		Exp.Exp(expType="Super", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(36),IntegerLiteral.IntegerLiteral(16)), (IntegerLiteral.IntegerLiteral(36),IntegerLiteral.IntegerLiteral(21))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_Phone", isTop=True)])])
	card=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	globalCard=(IntegerLiteral.IntegerLiteral(1),IntegerLiteral.IntegerLiteral(1))
	currClafer = Clafer.Clafer(pos=pos, isAbstract=isAbstract, gcard=groupCard, ident=id, uid=uid, my_supers=my_supers, card=card, glCard=globalCard)
	stack[-1].addElement(currClafer)
	stack.append(currClafer)
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c38_exp", pos=((IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(4)), (IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(12))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c39_exp", pos=((IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(9)), (IntegerLiteral.IntegerLiteral(37),IntegerLiteral.IntegerLiteral(12))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="this", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c13_gpu", isTop=False)])])]))]))
	stack[-1].addElement(constraint)
	stack.pop()
##### constraint #####
	constraint = IRConstraint.IRConstraint(isHard=True , exp=
		Exp.Exp(expType="ParentExp", my_type="Boolean", parentId="c40_exp", pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(2)), (IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(37))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="All", declaration=
		Declaration.Declaration(isDisjunct=False, localDeclarations=[LocalDeclaration.LocalDeclaration("p")],  body=
		Exp.Exp(expType="Body", my_type="Set", parentId="", pos=((IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0)), (IntegerLiteral.IntegerLiteral(0),IntegerLiteral.IntegerLiteral(0))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c1_Phone", isTop=True)])),bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Boolean", parentId="c42_exp", pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(37))), iExpType="IDeclarationParentExp", iExp=[DeclPExp.DeclPExp(quantifier="Some", declaration=None, bodyParentExp=
		Exp.Exp(expType="BodyParentExp", my_type="Set", parentId="c43_exp", pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(37))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c44_exp", pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(30))), iExpType="IFunctionExp", iExp=[FunExp.FunExp(operation=".", elements=[
		Exp.Exp(expType="Argument", my_type="Set", parentId="c45_exp", pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(18)), (IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(19))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="p", isTop=True)]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c46_exp", pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(20)), (IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(30))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c2_networking", isTop=False)])])]),
		Exp.Exp(expType="Argument", my_type="Set", parentId="c47_exp", pos=((IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(31)), (IntegerLiteral.IntegerLiteral(43),IntegerLiteral.IntegerLiteral(37))), iExpType="IClaferId", iExp=[ClaferId.ClaferId(moduleName="", my_id="c8_mobile", isTop=False)])])]))]))]))
	stack[-1].addElement(constraint)
	return module
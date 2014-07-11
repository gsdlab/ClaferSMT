'''
Created on Jul 10, 2014

@author: ezulkosk
'''
import z3

'''
TODO:
    Implement my own ForAll or declare sort to incorporate QFLIA approach
'''

def declareSort(claferSort):
    if not claferSort.superSort:
        return z3.DeclareSort(claferSort.element.uid)
    return None

def declareBoundedSort(claferSort):
    if not claferSort.superSort:
        return z3.EnumSort(claferSort.element.uid, [claferSort.element.uid + "_" + str(i) for i in range(12)])
    return None

def isOn(claferSort):
    if not claferSort.superSort:
        return z3.Function("isOn_" + claferSort.element.uid, claferSort.sort, z3.BoolSort())
    
def T(claferSort):
    if not claferSort.superSort:
        return claferSort
    else:
        currSort = claferSort.superSort
        while currSort:
            if currSort.superSort:
                currSort = currSort.superSort
            else:
                return currSort

def isName(claferSort):
    return z3.Function("isName_" + str(claferSort.element.uid), T(claferSort).sort, z3.BoolSort())

def isA(model, s1, s2):
    i = T(s1).consts[0]
    model.constraints.append(z3.ForAll(i, z3.Implies(s1.isName(i), s2.isName(i))))


def getRelationName(s1, s2):
    return "r$" + s1.element.uid + "$" + s2.element.uid

#for hierarchy, s1 = child, s2 = parent
def relation(model, s1, s2, lone=False, some=False):
    rname = getRelationName(s1, s2)
    r = model.relations.get(rname)
    c1 = T(s1).consts[0]
    p1 = T(s2).consts[0]
    p2 = T(s2).consts[1]
    if not r:
        r = z3.Function(rname, T(s1).sort, T(s2).sort, z3.BoolSort())
        model.relations[rname] = r
        constraint = z3.ForAll([c1,p1], z3.Implies(r(c1,p1), z3.And(s1.isName(c1), s2.isName(p1))))
        model.constraints.append(constraint)
    if lone:
        constraint = z3.ForAll([c1,p1,p2], z3.Implies(z3.And(r(c1,p1), r(c1,p2)), p1 == p2))
        model.constraints.append(constraint)
    if some:
        constraint = z3.ForAll(c1, z3.And(z3.Implies(T(s1).isOn(c1), z3.Exists(p1, r(c1,p1))),
                                          z3.Implies(z3.Exists(p1, r(c1,p1)), T(s1).isOn(c1))))
        model.constraints.append(constraint)
    return r

def And(s1, s2):
    return z3.And(s1, s2)
    

#TODO ensure 0 upper bound case?
def setCard(model, s):
    (lcard, ucard) = s.element.card
    (lcard, ucard) = (lcard.value, ucard.value)
    if lcard <= 0 and ucard < 0:
        return
    if ucard >= 0:
        consts = s.getConsts(ucard+1)
    else:
        consts = s.getConsts(lcard+1)
    if s.parent:
        p = s.parent.getNewConst()
        r = model.relations[getRelationName(s, s.parent)]
    if ucard > 0:
        if s.parent:
            constraint = z3.ForAll(p, z3.Not(z3.Exists(consts, z3.And(z3.Distinct(consts), *[r(i,p) for i in consts]))))
        else:
            constraint = z3.Not(z3.Exists(consts, z3.And(z3.Distinct(consts), *[T(s).isOn(i) for i in consts])))
        model.constraints.append(constraint)
    if lcard > 0:
        if s.parent:
            constraint = z3.ForAll(p, z3.Exists(consts[:lcard], 
                                                z3.And(z3.Distinct(consts[:lcard]), *[r(i,p) for i in consts[:lcard]])))
        else:
            constraint = z3.Exists(consts[:lcard], z3.Distinct(consts[:lcard]))
        model.constraints.append(constraint)
    
    
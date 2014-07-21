
import sys

numCalls = 0
def toStr(root, indent=0):
    global numCalls
    numCalls += 1
    print(indent * "  " + str(root))
    for i in root.children():
        toStr(i, indent + 1)

def createIf(b,t,f):
    if str(b) == "True":
        return t
    elif str(b) == "False":
        return f
    else:
        return SMT_If(b,t,f)

class SMT_If():
    def __init__(self, b, t, f):
        self.bool_expr = b
        self.true_expr = t
        self.false_expr = f

    def children(self):
        return [self.bool_expr, self.true_expr, self.false_expr]

    def convert(self, converter):
        return converter.if_expr(self)

    def __str__(self):
        return "If"

class SMT_Implies():
    def __init__(self, l, r, unsat_core_implies=False):
        self.left = l
        self. right = r
        self.unsat_core_implies = unsat_core_implies
        

    def children(self):
        return [self.left, self.right]

    def convert(self, converter):
        return converter.implies_expr(self)

    def __str__(self):
        return "Implies"
        
class SMT_And():
    def __init__(self, *l):
        self.list = l
        for i in self.list:
            if isinstance(i, bool) and not i:
                self.list = [SMT_BoolConst(False)]
        self.list = [i for i in self.list if not isinstance(i, bool)]

    def children(self):
        return self.list
        
    def convert(self, converter):
        return converter.and_expr(self)

    def __str__(self):
        return "And"
        
class SMT_Or():
    def __init__(self, *l):
        self.list = l
        for i in self.list:
            if isinstance(i, bool) and i:
                self.list = [SMT_BoolConst(True)]
        self.list = [i for i in self.list if not isinstance(i, bool)]

    def children(self):
        return self.list

    def convert(self, converter):
        return converter.or_expr(self)

    def __str__(self):
        return "Or"

class SMT_Xor():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]
        
    def convert(self, converter):
        return converter.xor_expr(self)

    def __str__(self):
        return "Xor"

def createNot(e):
    if str(e) == "True":
        return SMT_BoolConst(False)
    elif str(e) == "False":
        return SMT_BoolConst(True)
    else:
        return SMT_Not(e)

class SMT_Not():
    def __init__(self, e):
        self.value = e

    def children(self):
        return [self.value]
        
    def convert(self, converter):
        return converter.not_expr(self)

    def __str__(self):
        return "Not"


def createNeg(e):
    if isinstance(e, SMT_IntConst):
        return SMT_IntConst(-e.value)
    else:
        return SMT_Neg(e)

class SMT_Neg():

    def __init__(self, e):
        self.value = e

    def children(self):
        return [self.value]

    def convert(self, converter):
        return converter.neg_expr(self)

    def __str__(self):
        return "-"

class SMT_LE():
    def __init__(self, l, r):
        self.left = l
        self.right = r
        

    def children(self):
        return [self.left, self.right]

    def convert(self, converter):
        return converter.le_expr(self)

    def __str__(self):
        return "<="
    
class SMT_GE():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]
        
    def convert(self, converter):
        return converter.ge_expr(self)

    def __str__(self):
        return ">="
        
class SMT_LT():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]
        
    def convert(self, converter):
        return converter.lt_expr(self)

    def __str__(self):
        return "<"
    
class SMT_GT():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]
        
    def convert(self, converter):
        return converter.gt_expr(self)

    def __str__(self):
        return ">"
    
class SMT_EQ():
    def __init__(self, l, r):
        self.left = l
        self. right = r
        if isinstance(l, int) or isinstance(r, int):
            print(l)
            print(r)
            raise Exception

    def children(self):
        return [self.left, self.right]
        
    def convert(self, converter):
        return converter.eq_expr(self)

    def __str__(self):
        return "=="

def createNE(l, r):
    createNot(SMT_EQ(l,r))
    
class SMT_NE():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]
        
    def convert(self, converter):
        return converter.ne_expr(self)

    def __str__(self):
        return "!="

def createSum(l):
    if len(l) == 1:
        return l[0]
    else:
        return SMT_Sum(l)
    
        
class SMT_Sum():
    def __init__(self, l):
        self.list = list(l)

    def children(self):
        return self.list

    def convert(self, converter):
        return converter.sum_expr(self)

    def __str__(self):
        return "Sum"
   
class SMT_Int():
    def __init__(self, uid, bits=None):
        self.bits = bits
        self.id = uid
        self.var = None

    def children(self):
        return []

    def convert(self, converter):
        if not self.var:
            self.var = converter.int_var(self)
        return self.var

    def __str__(self):
        if self.bits:
            return self.id + ":" + str(self.bits)
        else:
            return self.id

class SMT_IntConst():
    def __init__(self, val):
        self.value = val

    def children(self):
        return []

    def convert(self, converter):
        return converter.int_const(self)

    def __str__(self):
        return str(self.value)
    
class SMT_BoolConst():
    def __init__(self, val):
        self.value = val

    def children(self):
        return []

    def convert(self, converter):
        return converter.bool_const(self)

    def __str__(self):
        return str(self.value)

class SMT_Real():
    def __init__(self, uid):
        self.id = uid
        self.var = None

    def children(self):
        return []

    def convert(self, converter):
        if not self.var:
            self.var = converter.real_var(self)
        return self.var

    def __str__(self):
        return self.id
    
class SMT_RealConst():
    def __init__(self, val):
        self.value = val

    def children(self):
        return []

    def convert(self, converter):
        return converter.real_const(self)

    def __str__(self):
        return str(self.value)
        
class SMT_Bool():
    def __init__(self, v):
        self.id = v
        self.var = None

    def children(self):
        return []
        
    def convert(self, converter):
        if not self.var:
            self.var = converter.bool_var(self)
        return self.var

    def __str__(self):
        return str(self.id)

class SMT_Plus():
    def __init__(self, l, r):
        self.left = l
        self.right = r
        

    def children(self):
        return [self.left, self.right]

    def convert(self, converter):
        return converter.plus_expr(self)

    def __str__(self):
        return "+"

class SMT_Minus():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]

    def convert(self, converter):
        return converter.minus_expr(self)

    def __str__(self):
        return "-"

class SMT_Times():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]

    def convert(self, converter):
        return converter.times_expr(self)

    def __str__(self):
        return "*"

class SMT_Divide():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]

    def convert(self, converter):
        return converter.divide_expr(self)

    def __str__(self):
        return "/"
    
class SMT_IntDivide():
    def __init__(self, l, r):
        self.left = l
        self.right = r

    def children(self):
        return [self.left, self.right]

    def convert(self, converter):
        return converter.intdivide_expr(self)

    def __str__(self):
        return "//"

def SMT_IntVector(uid, count, bits=None):
    return [SMT_Int(str(uid) + "__" + str(i), bits) for i in range(count)]
    
def SMT_RealVector(uid, count):
    return [SMT_Real(str(uid) + "__" + str(i)) for i in range(count)]

        



class SMT_If():
    def __init__(self, b, t, f):
        self.bool_expr = b
        self.true_expr = t
        self.false_expr = f
    
    def convert(self, converter):
        return converter.if_expr(self)

class SMT_Implies():
    def __init__(self, l, r):
        self.left = l
        self. right = r
        
    def convert(self, converter):
        return converter.implies_expr(self)
        
class SMT_And():
    def __init__(self, *l):
        self.list = l
        
    def convert(self, converter):
        return converter.and_expr(self)
        
class SMT_Or():
    def __init__(self, *l):
        self.list = l
        
    def convert(self, converter):
        return converter.or_expr(self)

class SMT_Xor():
    def __init__(self, l, r):
        self.left = l
        self.right = r
        
    def convert(self, converter):
        return converter.xor_expr(self)
        
class SMT_Not():
    def __init__(self, e):
        self.expr = e
        
    def convert(self, converter):
        return converter.not_expr(self)    
    
class SMT_LE():
    def __init__(self, l, r):
        self.left = l
        self. right = r
        
    def convert(self, converter):
        return converter.le_expr(self)
    
class SMT_GE():
    def __init__(self, l, r):
        self.left = r
        self. right = l
        
    def convert(self, converter):
        return converter.le_expr(self)
        
class SMT_LT():
    def __init__(self, l, r):
        self.left = l
        self. right = r
        
    def convert(self, converter):
        return converter.lt_expr(self)
    
class SMT_GT():
    def __init__(self, l, r):
        self.left = r
        self. right = l
        
    def convert(self, converter):
        return converter.lt_expr(self)
    
class SMT_EQ():
    def __init__(self, l, r):
        self.left = r
        self. right = l
        
    def convert(self, converter):
        return converter.eq_expr(self)
    
class SMT_NE():
    def __init__(self, l, r):
        self.left = r
        self. right = l
        
    def convert(self, converter):
        return converter.ne_expr(self)
        
class SMT_Sum():
    def __init__(self, l):
        self.list = l
        
    def convert(self, converter):
        return converter.sum_expr(self)
   
class SMT_Int():
    def __init__(self, uid):
        self.id = uid  
    
    def convert(self, converter):
        return converter.int_var(self)
    
class SMT_Real():
    def __init__(self, uid):
        self.id = uid  
    
    def convert(self, converter):
        return converter.real_var(self)
        
class SMT_Bool():
    def __init__(self, uid):
        self.id = uid    
        
    def convert(self, converter):
        return converter.bool_var(self)
    
def SMT_IntVector(uid, count):
    return [SMT_Int(str(uid) + "__" + str(i)) for i in range(count)]
    
def SMT_RealVector(uid, count):
    return [SMT_Real(str(uid) + "__" + str(i)) for i in range(count)]

        

from abc import ABCMeta,abstractmethod
from vartree2 import Bintree
from machine import Instruction,Print,Initialize,Load,Store,Compute

class Exprtree(metaclass = ABCMeta):
    def __str__(self):
        return ' '.join( str(x) for x in iter(self))
    
    @abstractmethod
    def __iter__(self):
        """an inorder iterator for this tree node, for display"""
        pass
    @abstractmethod
    def postfix(self):
        """a post-order iterator to create a postfix expression"""
        pass
    @abstractmethod
    def evaluate(self, variables, functions):
        """evaluate using the existing variables"""
        pass

class Var(Exprtree):
    def __init__(self, n):
        self._name = n
    def __iter__(self):
        yield self._name
    def postfix(self):
        yield self._name
    def evaluate(self, variables,functions):
        return variables.lookup(self._name)
    def givename(self):
        return self._name
    def comp(self,variables,program):
        if variables.locate(self._name) != -1:
            reg = program.next_reg()
            inst = Load(reg,variables.locate(self._name))
            program.code.append(inst)
            return reg

        


class Value(Exprtree):
    def __init__(self,v):
        self._value = v
    def __iter__(self):
        yield self._value
    def postfix(self):
        yield self._value
    def evaluate(self,variables,functions):
        return self._value
    def comp(self,variables,program):
        reg = program.next_reg()
        inst = Initialize(reg,self._value)
        program.code.append(inst)
        return reg
        
class Oper(Exprtree):
    def __init__(self,left,oper,right):
        self._left = left
        self._right = right
        self._parent = oper
    def __iter__(self):
        yield from self._left
        yield self._parent
        yield from self._right
    def postfix(self):
        yield from self._left.postfix()
        yield from self._right.postfix()
        yield self._parent
    def evaluate(self,v1,v2):
        if self._parent == "+":
            return self._left.evaluate(v1,v2) + self._right.evaluate(v1,v2)
        elif self._parent == "*":
            return self._left.evaluate(v1,v2) * self._right.evaluate(v1,v2)
        elif self._parent == "/":
            return self._left.evaluate(v1,v2) / self._right.evaluate(v1,v2)
        elif self._parent == "-":
            return self._left.evaluate(v1,v2) - self._right.evaluate(v1,v2)
        elif self._parent == "%":
            return self._left.evaluate(v1,v2) % self._right.evaluate(v1,v2)
        elif self._parent == "=":
            v1.assign(self._left.givename(),self._right.evaluate(v1,v2))
            return self._right.evaluate(v1,v2)
        elif self._parent == "<=":
            if self._left.evaluate(v1,v2) <= self._right.evaluate(v1,v2):
                return True
            else:
                return False
        elif self._parent == ">=":
            if self._left.evaluate(v1,v2) >= self._right.evaluate(v1,v2):
                return True
            else:
                return False
        elif self._parent == ">":
            if self._left.evaluate(v1,v2) > self._right.evaluate(v1,v2):
                return True
            else:
                return False
        elif self._parent == "<":
            if self._left.evaluate(v1,v2) < self._right.evaluate(v1,v2):
                return True
            else:
                return False
        elif self._parent == "==":
            if self._left.evaluate(v1,v2) == self._right.evaluate(v1,v2):
                return True
            else:
                return False
        elif self._parent == "!=":
            if self._left.evaluate(v1,v2) != self._right.evaluate(v1,v2):
                return True
            else:
                return False
        elif self._parent == "and":
            if self._left.evaluate(v1,v2) == True and self._right.evaluate(v1,v2) == True:
                return self._left.evaluate(v1,v2) or self._right.evaluate(v1,v2)
        elif self._parent == "or":
            if self._left.evaluate(v1,v2) == True or self._right.evaluate(v1,v2) == True:
                return self._left.evaluate(v1,v2) or self._right.evaluate(v1,v2)

    def comp(self,variables,program):
        if self._parent == "=":
            reg1 = self._right.comp(variables,program)
            v1 = Bintree()
            v2 = Bintree()
            variables.assign(self._left.givename(),self._right.evaluate(v1,v2))
            reg = program.last_temp
            inst = Store(reg ,variables.locate(self._left.givename()))
            program.code.append(inst)
            return reg 
        else:
            reg1 = self._left.comp(variables,program)
            reg2 = self._right.comp(variables,program)
            reg = program.next_reg()
            inst = Compute(reg, self._parent, reg1, reg2)
            program.code.append(inst)
            return reg
        


class Func(Exprtree):
    def __init__(self,name,args):
        self._name = name
        self._args = args
    def __iter__(self):
        yield self._name
        yield "("
        if len(self._args) > 0:
            yield self._args[0]
            for x in range(1,len(self._args)):
                yield ","
                yield self._args[x]
        yield ")"
    def postfix(self):
        pass
    def evaluate(self,variables,functions):
        if functions.lookup(self._name) != 0:
            params, body = functions.lookup(self._name)
            v1 = Bintree()
            for x in range (0,len(params)):
                v1.assign(params[x] , self._args[x].evaluate(variables,functions))
            return body.evaluate(v1,functions)


class Cond(Exprtree):
    def __init__(self,cond,true,false):
        self._condition = cond
        self._true = true
        self._false = false
    def __iter__(self):
        yield from self._condition
        yield "?"
        yield from self._true
        yield ":"
        yield from self._false
    def postfix(self):
        pass
    def evaluate(self,v1,v2):
        if (self._condition.evaluate(v1,v2) == True):
            return self._true.evaluate(v1,v2)
        else:
            return self._false.evaluate(v1,v2)

        
        
            
if __name__ == '__main__':
    V = Bintree()
    VA = Var("A")
    Sum = Oper(Value(2),'+',Value(3))
    print(Sum.evaluate(V))
    A = Oper(VA,'=',Sum)
    print( "Infix iteration: ", list(A) )
    print( "String version ", A )
    print( "Postfix iteration: ", list(A.postfix()) )
    print( "Execution: ", A.evaluate(V) )
    print( "Afterwards, A = ", VA.evaluate(V) )

    CondTest = Cond(Oper(VA,'==',Value(5)),Oper(VA,'+',Value(2)),Value(3))
    print(CondTest,'-->',CondTest.evaluate(V))
    

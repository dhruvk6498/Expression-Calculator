class Instruction:
    """Simple instructions representative of a RISC machine

    These instructions are mostly immutable -- once constructed,
    they will not be changed -- only displayed and executed
    """
    def __init__(self, t):      # default constructor
        self._temp = t          # every instruction has a register
    def get_temp(self):         #     which holds its answer
        return self._temp

class Print(Instruction):
    """A simple non-RISC output function to display a value"""
    def __str__(self):
        return "print T" + str(self._temp)
    def execute(self,temps,stack,pc,sp):
        print( temps[self._temp] )

class Initialize(Instruction):
    def __init__(self,t,v):
        super().__init__(t)
        self._value = v
    def __str__(self):
        return "T" + str(self.get_temp()) + " = " + str(self._value)
    def execute(self,temps,stack,pc,sp):
        temps[self.get_temp()] = self._value 

class Load(Instruction):
    def __init__(self,t,loc):
        super().__init__(t)
        self._location = loc
    def __str__(self):
        return "T" + str(self.get_temp()) + " = " + "stack[" + str(self._location) + "]"
    def execute(self,temps,stack,pc,sp):
        temps[self.get_temp()] = stack[self._location]

class Store(Instruction):
    def __init__(self,t,loc):
        super().__init__(t)
        self._location = loc
    def __str__(self):
        return "stack[" + str(self._location) + "]" + " = " + "T" + str(self.get_temp())
    def execute(self,temps,stack,pc,sp):
        stack[self._location] = temps[self.get_temp()]
        
class Compute(Instruction):
    def __init__(self,t,op,op1loc,op2loc):
        super().__init__(t)
        self._oper = op
        self._op1 = op1loc
        self._op2 = op2loc
    def __str__(self):
        return "T" + str(self.get_temp()) + " = " + "T" + str(self._op1) + str(self._oper) + "T" + str(self._op2)
    def execute(self,temps,stack,pc,sp):
        temps[self.get_temp()] = eval(str(temps[self._op1]) + self._oper + str(temps[self._op2]))



if __name__ == "__main__":
    instruction = Load(0,5)
    
    
    
        

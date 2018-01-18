"""This module is the front end to a final project
It allows a tester to name a program file with infix expressions
and function definitions, which are ultimately compiled into
instructions for an emulated machine.

After the input has been examined and compiled,
it is executed on the simulated machine and the results displayed.

This module is intended for the benefit of the students
taking CMPSC 122 at the Pennsylvania State University
during the Spring Semester of 2017, and is not intended
for any other audience, or to distributed outside of the course.

Roger Christman, Pennsylvania State University
"""
from vartree2 import Bintree
from peekable import Peekable, peek
from newsplit2 import new_split_iter
from infixtotree2 import to_expr_tree
from machine import Print

class Program:
    def __init__(self):
        self.first_stmt = -1        # 'main' not yet found
        self.last_temp  = 0         # no registers yet claimed
        self.functions = Bintree()  # no functions yet
        self.variables = Bintree()  # no global variables yet
        self.code = []              # no instructions yet
    def next_reg(self):
        self.last_temp += 1
        return self.last_temp

def compile_line(program,expr):
    """Define a new function, or evaluate an expression

    If the first word in the line "deffn", it should appear as
          deffn <function name> ( <parameters> ) = <function body>
    otherwise the input line is evaluated in an expression tree
    """
    iterator = Peekable(new_split_iter(expr))
    if peek(iterator) == "deffn":
        name, parms, body = define_func(iterator)
        local_variables = Bintree()
        code_line = len(program.code)
        program.functions.assign(name, (parms, body, code_line, local_variables))
        body.comp( local_variables, program )
    else:
        if program.first_stmt == -1:        # if 'main' not yet assigned
            program.first_stmt = len(program.code)  #    start executing here
        to_expr_tree(iterator).comp( program.variables, program )
        program.code.append( Print( program.code[-1].get_temp() ) )
        
def run_program(program):
    """run the program that has been compiled into the prog array
    starting at the first line that is not within any function
    after setting aside enough space for temporary registers and stack
    """
    print()
    for i in range(len(program.code)):
        print(i,':',program.code[i])
    print()
    temps = 100*[0]                 # a 'large' number of registers
    stack = 200*[0]                 # a 'large' stack in case of recursion
    pc = program.first_stmt         # start at the first statement
    sp = 100                        # initialize stack pointer (unused here)
    while pc < len(program.code):   # run to the bottom
        inst = program.code[pc]     #     fetch an instruction
        pc += 1                     #     increment to refer to next
        chg = inst.execute(temps, stack, pc, sp)  #     execute the instruction
        if chg is not None:         # see if anything new was returned
            pc, sp = chg            # only if either changed (extra credit)

def run_file(filename):
    """Run the program stored in the given file"""
    program = Program() 
    for line in open(filename):
        print(line,end='')
        compile_line(program,line)
    run_program(program)

if __name__ == "__main__":
    testfile = open("test.txt","w")

    print("a = 3",file=testfile)
    print("b = a+2",file=testfile)
    print("(b+1)*(b+1)+a",file=testfile)

    testfile.close()
    run_file("test.txt")


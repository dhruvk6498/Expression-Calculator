from exprtree3 import Exprtree,Var,Value,Oper,Cond,Func
from peekable import Peekable, peek
from newsplit2 import new_split_iter
from vartree2 import Bintree

def postfix_assign(iterator):
    op1 = postfix_conditional(iterator)
    oper = peek(iterator)
    while(oper == "="):
        next(iterator)
        op2 = postfix_assign(iterator)
        Node = Oper(op1,oper,op2)
        op1 = Node
        oper = peek(iterator)
    return op1

def postfix_conditional(iterator):
    op1 = postfix_relational(iterator)
    oper = peek(iterator)
    while(oper == "?"):
        next(iterator)
        op2 = postfix_conditional(iterator)
        oper = peek(iterator)
        while(oper == ":"):
            next(iterator)
            op3 = postfix_conditional(iterator)
            oper = peek(iterator)
        Node = Cond(op1,op2,op3)
        op1 = Node
        oper = peek(iterator)
    return op1


def postfix_relational(iterator):
    op1 = postfix_sum(iterator)
    oper = peek(iterator)
    while(oper == "<=" or oper == ">=" or oper == "==" or oper == "!=" or oper == ">" or oper == "<" or oper == "and" or oper == "or"):
        next(iterator)
        op2 = postfix_sum(iterator)
        Node = Oper(op1,oper,op2)
        op1 = Node
        oper = peek(iterator)
    return op1

def postfix_sum(iterator):
    op1 = postfix_product(iterator)
    oper = peek(iterator)
    while(oper == "+" or oper == "-"):
        next(iterator)
        op2 = postfix_product(iterator)
        Node = Oper(op1,oper,op2)
        op1 = Node
        oper = peek(iterator)
    return op1
  
def postfix_product(iterator):
    op1 = postfix_factor(iterator)
    oper = peek(iterator)
    while(oper == "*" or oper == "/" or oper == "%"):
        next(iterator)
        op2 = postfix_factor(iterator)
        Node = Oper(op1,oper,op2)
        op1 = Node
        oper = peek(iterator)
    return op1


def postfix_factor(iterator):
    if (peek(iterator) == "("):
        next(iterator)
        Node = postfix_assign(iterator)
        next(iterator)
    elif (peek(iterator).isdigit() == True):
        Node = Value(int(peek(iterator)))
        next(iterator)
    elif (peek(iterator).isalpha() == True):
        name = peek(iterator)
        next(iterator)
        if peek(iterator) == "(":
            next(iterator)
            params = [postfix_assign(iterator)]
            while peek(iterator) == ",":
                next(iterator)
                params.append(postfix_assign(iterator))
            Node = Func(name,params)
        else:
            Node = Var(name)
    return Node
            

def postfix_iter(iterator):
    return postfix_assign(Peekable(iterator))
        
def to_postfix(expr):
    return postfix_iter(new_split_iter(expr))

def tree_assign(iterator):
    return postfix_iter(iterator)

def to_expr_tree(iterator):
    return postfix_iter(iterator)
 

if __name__ == "__main__":
    v1 = Bintree()
    v2 = Bintree()
    print(to_postfix("abc = (3*4)").evaluate(v1,v2))
    print(to_postfix("b = abc < 0 ? abc+1 : abc-1").evaluate(v1,v2))
    print(to_postfix("abc + 4").evaluate(v1,v2))

   
    
    


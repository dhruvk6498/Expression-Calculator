from vartree2 import Bintree
from peekable import Peekable, peek
from newsplit2 import new_split_iter
from infixtotree2 import to_expr_tree, tree_assign

def define_func(iterator):
    """ Define a new function, which should appear as
          deffn <function name> ( <parameters> ) = <function body>
          a VarTree will associate the function name with
            a list of parameters (at least one, maybe more)
            and a tree representing the function body
    """
    next(iterator)              # "deffn"
    name = next(iterator)       # function name
    next(iterator)              # (
    parms = [next(iterator)]    # first argument
    while next(iterator)==',':
        parms.append(next(iterator))
    next(iterator)              # =
    return name, parms, tree_assign(iterator)

def evaluate(expr):
    """Define a new function, or evaluate an expression
       The decision is based on the first token in the input line
    """
    iterator = Peekable(new_split_iter(expr))
    if peek(iterator) == "deffn":
        name, parms, body = define_func(iterator)
        functions.assign(name, (parms, body))
    else:
        print(expr,':',to_expr_tree(iterator).evaluate(variables, functions))


functions = Bintree()
variables = Bintree()
if __name__ == "__main__":
    evaluate("deffn sqr(x) = x*x")
    evaluate("deffn abs(x) = x > 0 ? x : 0-x")
    evaluate("deffn fact(n) = n <= 1 ? 1 : n * fact(n-1)")
    evaluate("sqr(4)")
    evaluate("abs(3-5)")
    evaluate("fact(5)")
    evaluate("fact(0)")


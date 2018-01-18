def new_split_iter( expr ):
    expr = expr + ";"
    pos = 0
    while expr[pos] != ";":
        if(expr[pos] != " "):
            number = ""
            while(expr[pos].isdigit() == True):
                    number += expr[pos]
                    pos += 1
            if(number != ""):
                yield number
            word = ""
            while(expr[pos].isalpha() == True):
                word += expr[pos]
                pos += 1
            if(word != ""):
                yield word 
            if(expr[pos] == "=" and expr[pos+1] == "="):
                yield expr[pos] + expr[pos+1]
                pos += 2
            elif(expr[pos] == "+" or expr[pos] == "-" or expr[pos] == "*" or expr[pos] == "/" or expr[pos] == "%" or expr[pos] == "(" or expr[pos] == ")" or expr[pos] == "=" or expr[pos] == "?" or expr[pos] == ":"):
                yield expr[pos]
                pos += 1
            elif(expr[pos] == "<" and expr[pos+1] == "="):
                yield expr[pos] + expr[pos + 1]
                pos += 2
            elif(expr[pos] == ">" and expr[pos+1] == "="):
                yield expr[pos] + expr[pos + 1]
                pos += 2
            elif(expr[pos] == "!" and expr[pos+1] == "="):
                yield expr[pos] + expr[pos + 1]
                pos += 2
            elif(expr[pos] == "<" or expr[pos] == ">"):
                yield expr[pos]
                pos += 1
            elif(expr[pos] == " "):
                pos += 1
                continue
            elif(expr[pos] == ";"):
                break 
            else:
                yield expr[pos]
                pos += 1
        else:
            pos += 1 


if __name__ == "__main__":
    expression = "x = 1 + (y = 4)"
    for x in new_split_iter(expression):
        print(x)
    expression = "b = a > 0 and a < 5 ? a+1 : a-1"
    for x in new_split_iter(expression):
        print(x)
    expression = "n <= 1 ? 1 : n * fact ( n - 1 ) "
    for x in new_split_iter(expression):
        print(x)
    
    



   

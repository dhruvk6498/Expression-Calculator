class Bintree(object):
    class Node(object):
        """__slots__ == "_name" , "_value" , "_left" , "_right"""
        def __init__(self,n,v,l,r,loc):
            self._name = n
            self._value = v
            self._left = l
            self._right = r
            self._loc = loc
            
    def __init__(self):
        self._root = None
        self._size = 0

    def _search(self,here,var):
        if here is None:
            return None 
        elif here._name == var:
             return here
        elif here._name > var:
            return self._search(here._left, var)
        elif here._name < var:
            return self._search(here._right, var)

    def _insert(self,here,var,value):
        if self._size == 0:
            self._root = self.Node(var,value,None,None,0)
            here = self._root
            self._size += 1
        elif here is None:
            here = self.Node(var,value,None,None,self._size)
            self._size += 1
            return here
        elif here._name == var:
            here._value == value
        elif here._name > var:
            here._left = self._insert(here._left,var,value)
        elif here._name < var:
            here._right = self._insert(here._right,var,value)
        return here

    def is_empty(self):
        if self._size == 0:
            return True
        else:
            return False

    def assign(self,var,value):
        return self._insert(self._root,var,value)


    def lookup(self,var):
        if self._search(self._root,var) is None:
            self.assign(var,0)
            return 0
        else:
            x = self._search(self._root,var)
            return x._value

    def locate(self,var):
        if self._search(self._root,var) is None:
            self.assign(var,0)
            return -1
        else:
            x = self._search(self._root,var)
            return x._loc

    def __len__(self):
        return self._size

    def __iter__(self):
        yield from self.evaliter(self._root)

    def evaliter(self,here):
        current = here
        if current is not None:
            if current._left is not None:
                yield from self.evaliter(current._left)
            yield current._value
            if current._right is not None:
                yield from self.evaliter(current._right)
            
            
    def __str__(self):
        return self.evalstr(self._root)

    def evalstr(self,here):
        current = here
        exp = ""
        if current is not None:
            exp += str(current._value) + " " + self.evalstr(current._left) + self.evalstr(current._right) 
        return exp

            
            
     
if __name__ == "__main__":
    a = Bintree()
    x = a.assign("x",3)
    print(x._value)
    print(a.lookup("x"))
    print(a)
    a.assign("y",4)
    a.assign("a",5)
    a.assign("b",2)
    print(a)
    print(a.__len__())
    print(a.is_empty())
    for x in a:
        print(x)
    


        
        
        



 
    

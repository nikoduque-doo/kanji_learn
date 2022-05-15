from Node import Node

class LinkList:

    head = None
    tail = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0
    
    def __str__(self) -> str:
        s = ""
        if not self.isEmpty():
            current = self.head
            while current is not None:
                s += "{} - ".format(current.getValue())
                current = current.getNext()
        else:
            s = "List is empty"
        
        return s


    def pushFront(self, val):
        n = Node(val)
        if self.isEmpty():
            self.tail = n
        else:
            n.setNext(self.head)
        self.head = n
        self.count = self.count + 1
    
    def pushBack(self, val):
        n = Node(val)
        if self.isEmpty():
            self.head = n
        else:
            self.tail.setNext(n)
        self.tail = n
        self.count = self.count + 1
    
    def topFront(self):
        if self.head is not None:
            return self.head.getValue()

    def topBack(self):
        if self.tail is not None:
            return self.tail.getValue()

    def popFront(self):
        if not self.isEmpty():
            ret = self.head.getValue()
            self.head = self.head.getNext()
            self.count = self.count - 1
            return ret

    def popBack(self):
        if not self.isEmpty():
            ret = self.tail.getValue()
            if self.tail is not self.head:
                prev = self.head
                while prev is not None and prev.getNext() is not self.tail:
                    prev = prev.getNext()
                prev.setNext(None)
                self.tail = prev
            else:
                self.head = None
                self.tail = None
            self.count = self.count - 1
            return ret

    def addBefore(self, position, val):
        if not self.isEmpty():
            if position is self.head:
                self.pushFront(val)
            else:
                n = Node(val)
                prev = self.head
                while prev is not None and prev.getNext() is not position:
                    prev = prev.getNext()
                if prev is not None:
                    prev.setNext(n)
                    n.setNext(position)
                else: 
                    raise IndexError
                self.count = self.ccount + 1
        else:
            raise IndexError
        
    def addAfter(self, position, val):
        if not self.isEmpty():
            if position is self.tail:
                self.pushBack(val)
            else:
                if self.searchByRef(position):
                    n = Node(val)
                    n.setNext(position.getNext())
                    position.setNext(n)
                    self.count = self.count - 1
                else:
                    raise IndexError
        else:
            raise IndexError

    def isEmpty(self):
        return self.head is None

    def size(self):
        return self.count
    
    def search(self, val):
        found = False
        actual = self.head
        while actual is not None and not found:
            if val in actual.getValue().keys():
                found = True
            else:
                actual = actual.getNext()
        return found

    def searchByRef(self, ref):
        found = False
        actual = self.head
        while actual is not None and not found:
            if actual is ref:
                found = True
            else:
                actual = actual.getNext()
        return found
    
    def index(self, val):
        ret = None
        if self.search(val):
            found = False
            actual = self.head
            while actual is not None and not found:
                if val in actual.getValue().keys():
                    found = True
                    ret = actual
                else:
                    actual = actual.getNext()
        return ret

    def remove(self, val):
        if not self.isEmpty():
            actual = self.index(val)
            if actual is self.head:
                self.popFront()
            elif actual is self.tail:
                self.popBack()
            else:
                prev = self.head
                while prev is not None and prev.getNext() is not actual:
                    prev = prev.getNext()
                prev.setNext(actual.getNext())
                self.count = self.count - 1
        else:
            raise ValueError

    def printList(self):
        if not self.isEmpty():
            current = self.head
            while current is not None:
                print(current.getValue())
                current = current.getNext()
        else:
            print("List is empty") 

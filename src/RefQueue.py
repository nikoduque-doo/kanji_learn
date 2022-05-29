from Nodes import Node

class RefQueue():
  def __init__(self):
    self.head = None
    self.tail = None
    self.itemCount = 0
    
  def __str__(self):
    s = "< "
    point = self.head
    while point != None:
      s += str(point.getValue()) + " < "
      point = point.getNext()
    return s

  def traverse(self, f):
    point = self.head
    while point != None:
      f(point.getValue())
      point = point.getNext()

  def getSize(self):
    return self.itemCount

  def enqueue(self, data):
    tempVar = Node(data)
    self.itemCount += 1
    if not self.isEmpty():
      self.tail.setNext(tempVar)
    else: 
      self.head = tempVar
    self.tail = tempVar

  def dequeue(self):
    if not self.isEmpty():
      self.itemCount -= 1
      tempVar = self.head.getValue()
      self.head = self.head.getNext()
      if self.isEmpty():
        self.tail = None
      return tempVar

  def isEmpty(self):
    return self.head == None
  
  def isFull(self):
    return False

  def peek(self):
    if not self.isEmpty():
      return self.head.getValue()
    return None

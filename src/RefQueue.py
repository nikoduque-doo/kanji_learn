import Node

class RefQueue():
  def __init__(self):
    self.head = None
    self.tail = None
    
  def __str__(self):
    s = "< "
    point = self.head
    while point != None:
      s += str(point.getValue()) + " < "
      point = point.getNext()
    return s
    
  def enqueue(self, data):
    tempVar = Node(data)
    if not self.isEmpty():
      self.tail.setNext(tempVar)
    else: 
      self.head = tempVar
    self.tail = tempVar

  def dequeue(self):
    if not self.isEmpty():
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
import Node

class RefQueue():
  def __init__(self):
    self.head = None
    self.tail = None
    self.count = 0
    
  def enqueue(self, data):
    tempVar = Node(data)
    if not self.isEmpty():
      self.tail.setNext(tempVar)
    else: 
      self.head = tempVar
    self.tail = tempVar
    self.count += 1

  def dequeue(self):
    if not self.isEmpty():
      tempVar = self.head
      self.head = self.head.getNext()
      self.count -= 1
      if self.isEmpty():
        self.tail = None
      return tempVar

  def isEmpty(self):
    return self.head == None
  
  def isFull(self):
    return False

  def peek(self):
    return self.head

  def __str__(self):
    s = "< "
    point = self.head
    while point != None:
      s += str(point.getValue())+" < "
      point = point.getNext()
    return s

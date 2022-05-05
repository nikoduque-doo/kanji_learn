import Node

class RefQueue():
  def __init__(self):
    self.head = None
    self.tail = None
    
  def enqueue(self, data):
    tempVar = Node(data)
    if not self.isEmpty():
      self.tail.setNext(tempVar)
    else: 
      self.head = tempVar
    self.tail = tempVar

  def dequeue(self):
    if not self.isEmpty():
      tempVar = self.head
      self.head = self.head.getNext()
      if self.isEmpty():
        self.tail = None
      return tempVar

  def isEmpty(self):
    return self.head == None
  
  def isFull(self):
    return False

  def peek(self):
    return self.head

  def read(self):
    point = self.head
    while point != None:
      print(point, end=" ")
      point = point.getNext()
    print("<- tail")

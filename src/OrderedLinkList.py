from Nodes import Node

class OrderedLinkList():
  def __init__(self):
    self.head = None
    self.itemCount = 0
    self.position = self.head

  def __str__(self):
    s = "["
    if not self.isEmpty():
      s += str(self.head.getValue())
      pointer = self.head.getNext()
      while pointer != None:
        s += ", " + str(pointer.getValue())
        pointer = pointer.getNext()
    return s + "]"

  def traverse(self, f):
    pointer = self.head
    while pointer != None:
      f(pointer.getValue())
      pointer = pointer.getNext()

  def isFull(self):
    return False

  def isEmpty(self):
    return self.head == None

  def getSize(self):
    return self.itemCount

  def find(self, data):
    if not self.isEmpty():
      pointer = self.head
      while pointer.getNext() != None and pointer.getNext().getValue() < data:
        pointer = pointer.getNext()
      self.position = pointer
      #if pointer value > data --> pointer is head
      if pointer.getNext() != None and pointer.getNext().getValue() == data:
        return True
      if pointer.getValue() == data:
        return True
    return False

  def insert(self, data):
    if self.isEmpty():
      self.head = Node(data)
      self.position = self.head
      self.itemCount += 1
    else:
      if not self.find(data):
        tempNode = Node(data)
        self.itemCount += 1
        if self.position.getValue() > data:
          tempNode.setNext(self.position)
          self.head = tempNode
        else:
          tempNode.setNext(self.position.getNext())
          self.position.setNext(tempNode)
        self.position = tempNode
  
  def delete(self, data):
    if self.find(data):
      self.itemCount -= 1
      if self.position.getValue() == data:
        self.head = self.position.getNext()
        self.position = self.head
      else:
        self.position.setNext(self.position.getNext().getNext())

  def first(self):
    self.pointer = self.head

  def next(self):
    if self.position != None:
      self.position = self.position.getNext()

  def rangeSearch(self, min, max):
    l = []
    self.find(min)
    while self.position != None and self.position.getValue() <= max:
      if self.position.getValue() >= min:
        l.append(self.position.getValue())
      self.next()
    return l
  
  def clear(self):
    self.head = None
    self.itemCount = 0
    self.position = self.head

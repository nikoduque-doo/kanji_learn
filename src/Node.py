class Node():
  def __init__(self, value):
    self._value = value
    self._next = None
    
  def __str__(self):
    return str(self._value)

  def setNext(self, value):
    self._next = value 

  def getNext(self):
    return self._next

  def setValue(self, value):
    self._value = value 

  def getValue(self):
    return self._value

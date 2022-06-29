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

class BSTNode:
  def __init__(self, k):
    self._key = k
    self._left = None
    self._right = None
    self._parent = None
  
  def __gt__(self, other):
    if type(other) == AVLNode or type(other) == BSTNode:
      return self._key > other._key
    return self._key > other

  def __ge__(self, other):
    if type(other) == AVLNode or type(other) == BSTNode:
      return self._key >= other._key
    return self._key >= other

  def __lt__(self, other):
    if type(other) == AVLNode or type(other) == BSTNode:
      return self._key < other._key
    return self._key < other

  def __le__(self, other):
    if type(other) == AVLNode or type(other) == BSTNode:
      return self._key <= other._key
    return self._key <= other

  def __eq__(self, other):
    if type(other) == AVLNode or type(other) == BSTNode:
      return self._key == other._key
    return self._key == other
  
  def __str__(self):
    return str(self._key)

  def getKey(self):
    return self._key
  
  def getLeft(self):
    return self._left
  
  def getRight(self):
    return self._right
  
  def getParent(self):
    return self._parent

  def setKey(self, k):
    self._key = k
  
  def setLeft(self, n):
    self._left = n
  
  def setRight(self, n):
    self._right = n
  
  def setParent(self, n):
    self._parent = n
    
class AVLNode(BSTNode):
  def __init__(self, k):
    BSTNode.__init__(self, k)
    self._height = 1
  
  def getHeight(self):
    return self._height
  
  def setHeight(self, num):
    self._height = num
  
  def __iadd__(self, num):
    self._height += num
    return self
  
  def __isub__(self, num):
    self._height -= num
    return self

class Tag():
  def __init__(self, key, dynArray):
    self.key = key
    self.words = dynArray

  def __str__(self):
    return "Key: " + self.key.__str__() + " Words:" + self.words.__str__()

  def setKey(self, key):
    self.key = key

  def setWords(self, dynArr):
    self.words = dynArr

  def getKey(self):
    return self.key

  def getWords(self):
    return self.words

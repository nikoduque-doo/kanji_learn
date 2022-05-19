class TNode:
  def __init__(self, k):
    self._key = k
    self._left = None
    self._right = None
    self._parent = None
    self._height = 1

  def __iadd__(self, num):
    self._height += num
    return self
  
  def __gt__(self, other):
    if type(other) == TNode:
      return self._key > other._key
    return self._key > other

  def __lt__(self, other):
    if type(other) == TNode:
      return self._key < other._key
    return self._key < other

  def __eq__(self, other):
    if type(other) == TNode:
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
  
  def getHeight(self):
    return self._height

  def setKey(self, k):
    self._key = k
  
  def setLeft(self, n):
    self._left = n
  
  def setRight(self, n):
    self._right = n
  
  def setParent(self, n):
    self._parent = n

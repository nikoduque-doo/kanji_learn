from Nodes import BSTNode
from StaticStack import ArrStack

class BST:
  def __init__(self):
    self.root = None
    self.itemCount = 0

  def __str__(self):
    if self.root != None:
      return self.inOrder(self.root)+"]"
    return "[]"

  def inOrder(self, node, s = "["):
    if node.getLeft() != None:
      s = self.inOrder(node.getLeft(), s)
    if s == "[":
      s += str(node.getKey())
    else:
      s += ", " + str(node.getKey())
    if node.getRight() != None:
      s = self.inOrder(node.getRight(), s)
    return s
  
  def traverse(self, f):
    if(self.itemCount != 0):
      self.recursiveTraverse(f, node = self.root)

  def recursiveTraverse(self, f, node):
    if node.getLeft() != None:
      self.recursiveTraverse(f, node.getLeft())
    f(node.getKey())
    if node.getRight() != None:
      self.recursiveTraverse(f, node.getRight())

  def toStack(self):
    stack = ArrStack(size = self.itemCount)
    self.recursiveToStack(stack, self.root)
    return stack

  def recursiveToStack(self, stack, node):
    if node.getLeft() != None:
      self.recursiveToStack(stack, node.getLeft())
    stack.push(node.getKey())
    if node.getRight() != None:
      self.recursiveToStack(stack, node.getRight())


  def getSize(self):
    return self.itemCount

  def find(self, k, root):
    if root != None:
      if root > k and root.getLeft() != None:
          return self.find(k, root.getLeft())
      elif root < k and root.getRight() != None:
          return self.find(k, root.getRight())
    return root
  
  def search(self, k):
    result = self.find(k, self.root)
    if result != None:
      if result.getKey() == k:
        return result.getKey()
    return None

  def leftDescendant(self, node):
    if node.getLeft() != None:
      return self.leftDescendant(node.getLeft())
    return node

  def getMin(self, node):
    return self.leftDescendant(node).getKey()

  def rightAncestor(self, node):
    if node.getParent() != None:
      if node < node.getParent():
        return node.getParent()
      return self.rightAncestor(node.getParent())
    return None
  
  def getNext(self, node):
    if node.getRight() != None:
      return self.leftDescendant(node.getRight())
    return self.rightAncestor(node)

  def insert(self, k):
    if self.root != None:
      lot = self.find(k, self.root)
      if lot > k:
        lot.setLeft(BSTNode(k))
        lot.getLeft().setParent(lot)
        self.itemCount += 1
        return lot.getLeft()
      elif lot < k:
        lot.setRight(BSTNode(k))
        lot.getRight().setParent(lot)
        self.itemCount += 1
        return lot.getRight()
    else:
      self.root = lot = BSTNode(k)
      self.itemCount += 1
    return lot
  
  def delete(self, k):
    node = self.find(k, self.root)
    if node == k:
      self.itemCount -= 1
      if node.getRight() != None:
        nxt = self.getNext(node)
        node.setKey(nxt.getKey())
        if nxt.getParent() == node:
          nxt.getParent().setRight(nxt.getRight())
        else:
          nxt.getParent().setLeft(nxt.getRight())
        if nxt.getRight() != None:
          nxt.getRight().setParent(nxt.getParent())
      else:
        if node.getParent() != None:
          if node < node.getParent():
            node.getParent().setLeft(node.getLeft())
          else:
            node.getParent().setRight(node.getLeft())
          if node.getLeft() != None:
            node.getLeft().setParent(node.getParent())
        else:
          self.root = node.getLeft()

  def rangeSearch1(self, min, max):
    l = []
    node = self.find(min, self.root)
    while node != None and node <= max:
      if node >= min:
        l.append(node.getKey())
      node = self.getNext(node)
    return l

  def rangeSearch(self, min, max):
    s = ArrStack(100)
    node = self.find(min, self.root)
    while node != None and node <= max:
      if node >= min:
        s.push(node.getKey())
      node = self.getNext(node)
    return s

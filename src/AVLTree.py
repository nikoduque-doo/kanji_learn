from Nodes import AVLNode
from BST import BST

class AVLTree(BST):
  def __init__(self, k):
    BST.__init__(self, k)
    self.root = AVLNode(k)

  def __str__(self):
    return self.inOrder(self.root)+"]"

  def inOrder(self, node, s = "["):
    if node.getLeft() != None:
      s = self.inOrder(node.getLeft(), s)
    s += " " + str(node.getKey())+","+ str(node.getHeight())
    if node.getRight() != None:
      s = self.inOrder(node.getRight(), s)
    return s

  def fixHeavyLeft(self, node):
    left = node.getLeft()
    if left.getRight() != None:
      if left.getLeft() == None or left.getLeft().getHeight() < left.getRight().getHeight():
        self.rotateLeft(left)
    self.rotateRight(node)

  def fixHeavyRight(self, node):
    right = node.getRight()
    if right.getLeft() != None:
      if right.getRight() == None or right.getLeft().getHeight() > right.getRight().getHeight():
        self.rotateRight(right)
    self.rotateLeft(node)

  def rebalance(self, node):
    if node.getLeft() != None:
      if node.getRight() != None:
        if node.getLeft().getHeight() > node.getRight().getHeight() + 1:
          self.fixHeavyLeft(node)
        elif node.getRight().getHeight() > node.getLeft().getHeight() + 1:
          self.fixHeavyRight(node)
      else:
        if node.getLeft().getHeight() > 1:
          self.fixHeavyLeft(node)
    elif node.getRight() != None:
      if  node.getRight().getHeight() > 1:
        self.fixHeavyRight(node)
    if node.getParent() != None:
      self.rebalance(node.getParent())

  def rotateRight(self, pivot):
    tempRoot = pivot.getParent()
    uprisen = pivot.getLeft()
    leftover = uprisen.getRight() if uprisen != None else None
    uprisen.setParent(tempRoot)
    if tempRoot != None:
      if tempRoot > uprisen:
        tempRoot.setLeft(uprisen)
      else:
        tempRoot.setRight(uprisen)
    else:
      self.root = uprisen
    pivot.setParent(uprisen)
    uprisen.setRight(pivot)
    pivot.setLeft(leftover)
    if leftover != None:
      leftover.setParent(pivot)
    self.setNodeHeight(pivot)
    self.setNodeHeight(uprisen)
    if tempRoot != None:
      self.setNodeHeight(tempRoot)

  def rotateLeft(self, pivot):
    tempRoot = pivot.getParent()
    uprisen = pivot.getRight()
    leftover = uprisen.getLeft() if uprisen != None else None
    uprisen.setParent(tempRoot)
    if tempRoot != None:
      if tempRoot > uprisen:
        tempRoot.setLeft(uprisen)
      else:
        tempRoot.setRight(uprisen)
    else:
      self.root = uprisen
    pivot.setParent(uprisen)
    uprisen.setLeft(pivot)
    pivot.setRight(leftover)
    if leftover != None:
      leftover.setParent(pivot)
    self.setNodeHeight(pivot)
    self.setNodeHeight(uprisen)
    if tempRoot != None:
      self.setNodeHeight(tempRoot)

  def setNodeHeight(self, node):
    if node.getLeft() != None:
      left = node.getLeft()
      if node.getRight() != None:
        right = node.getRight()
        if left.getHeight() > right.getHeight():
          node.setHeight(left.getHeight() + 1)
        else:
          node.setHeight(right.getHeight() + 1)
      else:
        node.setHeight(left.getHeight() + 1)
    elif node.getRight() != None:
      node.setHeight(node.getRight().getHeight() + 1)
    else:
      node.setHeight(1)
    return node.getHeight()
  
  def updateInsertHeight(self, node):
    if node.getParent() != None and node.getHeight() >= node.getParent().getHeight():
      parent = node.getParent()
      parent += 1
      self.updateInsertHeight(node.getParent())

  def updateDeleteHeight(self, node):
    if node != None:
      currentHeight = node.getHeight()
      newHeight = self.setNodeHeight(node)
      node = node.getParent()
      while node != None and newHeight != currentHeight:
        currentHeight = node.getHeight()
        newHeight = self.setNodeHeight(node)
        node = node.getParent()

  def insert(self, k):
    lot = self.find(k, self.root)
    toBeUpdated = lot 
    if lot > k:
      lot.setLeft(AVLNode(k))
      lot.getLeft().setParent(lot)
      toBeUpdated = lot.getLeft()
    elif lot < k:
      lot.setRight(AVLNode(k))
      lot.getRight().setParent(lot)
      toBeUpdated = lot.getRight()
    self.updateInsertHeight(toBeUpdated)
    self.rebalance(toBeUpdated)

  def delete(self, k):
    node = self.find(k, self.root)
    if node == k:
      if node.getRight() != None:
        nxt = self.getNext(node)
        node.setKey(nxt.getKey())
        if nxt.getParent() == node:
          nxt.getParent().setRight(nxt.getRight())
        else:
          nxt.getParent().setLeft(nxt.getRight())
        if nxt.getRight() != None:
          nxt.getRight().setParent(nxt.getParent())
        self.updateDeleteHeight(nxt.getParent())
        self.rebalance(nxt.getParent())
      else:
        if node.getParent() != None:
          if node < node.getParent():
            node.getParent().setLeft(node.getLeft())
          else:
            node.getParent().setRight(node.getLeft())
          if node.getLeft() != None:
            node.getLeft().setParent(node.getParent())
          self.updateDeleteHeight(node.getParent())
          self.rebalance(node.getParent())
        else:
          self.root = node.getLeft()

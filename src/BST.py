from TNode import TNode

class BST:
  def __init__(self, k):
    self.root = TNode(k)

  def __str__(self):
    return self.inOrder(self.root)+"]"

  def inOrder(self, node, s = "["):
    if node.getLeft() != None:
      s = self.inOrder(node.getLeft(), s)
    s += " " + str(node.getKey())
    if node.getRight() != None:
      s = self.inOrder(node.getRight(), s)
    return s
  
  def find(self, k, root):
    if root > k and root.getLeft() != None:
        return self.find(k, root.getLeft())
    elif root < k and root.getRight() != None:
        return self.find(k, root.getRight())
    return root

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
    return self.rightAncestor()

  def insert(self, k):
    lot = self.find(k, self.root)
    if lot > k:
      lot.setLeft(TNode(k))
      lot.getLeft().setParent(lot)
    elif lot < k:
      lot.setRight(TNode(k))
      lot.getRight().setParent(lot)

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

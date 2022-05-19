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
  
  def insert(self, k):
    lot = self.find(k, self.root)
    if lot > k:
      lot.setLeft(TNode(k))
    elif lot < k:
      lot.setRight(TNode(k))

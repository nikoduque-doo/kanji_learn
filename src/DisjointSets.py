class DisjointSets():
  def __init__(self, size = 4):
    self.parent = [None]*size
    self.rank = [None]*size
    self.itemCount = 0
    self.maxSize = size

  def setSet(self, value):
    if self.itemCount >= self.maxSize:
      self.maxSize *= 2
      tempParent = [None]*maxSize
      tempRank = [None]*maxSize
      for i in range(self.itemCount):
        tempParent[i] = self.parent[i]
        tempRank[i] = self.rank[i]
      self.parent = tempParent
      self.rank = tempRank
    self.parent[value] = value
    self.itemCount += 1

  def find(self, index):
    while index != self.parent[index]:
      index = self.parent[index]
    return index

  def union(self, a, b):
    if a != b:
      aIndex = self.find(a)
      bIndex = self.find(b)
      if self.rank(aIndex) < self.rank(aIndex):
        self.parent[a] = b
      else:
        if self.rank(aIndex) == self.rank(aIndex):
          self.rank[b] += 1
        self.parent[b] = a

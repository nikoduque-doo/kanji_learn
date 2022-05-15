class ArrStack():
  def __init__(self, size=100):
    self.itemCount = 0 
    self.size = size
    self.arr = [None]*(size)
    
  def __str__(self):
    if not self.isEmpty():
      s = "["
      for i in range(self.itemCount-1):
        s += str(self.arr[i]) + ", "
      return s + str(self.arr[self.itemCount-1]) + ">"
    else:
      return "[>"

  def isFull(self):
    return self.itemCount == self.size

  def isEmpty(self):
    return self.itemCount == 0

  def pop(self):
    if not self.isEmpty():
      self.itemCount -= 1
      return self.arr[self.itemCount]
    return None

  def push(self, item):
    if not self.isFull():
      self.arr[self.itemCount] = item
      self.itemCount += 1
    else:
      print("Overflow.")

  def top(self):
    if not self.isEmpty():
      return self.stackArray[self.itemCount - 1]
    return None

  def getSize(self):
    return self.itemCount

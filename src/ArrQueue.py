class ArrQueue():
  def __init__(self, size=100):
    self.size = size + 1
    self.write = 0
    self.erase = 0
    self.arr = [None]*(size+1)
    
  def enqueue(self, item):
    if not self.isFull():
      self.arr[self.write] = item
      self.write = (self.write + 1) % self.size

  def dequeue(self):
    if not self.isEmpty():
      tempVar = self.arr[self.erase]
      self.erase = (self.erase + 1) % self.size
      return tempVar
    return None
  
  def peek(self):
    return self.arr[self.erase]

  def isEmpty(self):
    return self.write == self.erase

  def isFull(self):
    return (self.write + 1) % self.size == self.erase

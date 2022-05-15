from random import randint

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
      return self.arr[self.itemCount - 1]
    return None

  def getSize(self):
    return self.itemCount


"""
  Call like this:
    myArrStack = stack_search(data, myArrStack) 
    
  If item found, returns stack with item at the top.
  Else, returns stack with "None" at the top.
"""
def stack_search(item, s):
  if s.isFull():
    s2 = ArrStack(s.size+1)
  else:
    s2 = ArrStack(s.size)
  while (not s.isEmpty()) and (item != next(iter(s.top().keys()))):
    s2.push(s.pop())
  if s.isEmpty():
    s2.push(None)
    return s2
  else:
    foundItem = s.pop()
    if s.getSize() < s2.getSize():
      while not s.isEmpty():
        s2.push(s.pop())
      s2.push(foundItem)
      return s2
    else:
      while not s2.isEmpty():
        s.push(s2.pop())
      s.push(foundItem)
      return s

"""
  Call like this:
    myArrStack = stack_delete(data, myArrStack) 
"""
def stack_delete(item, s):
  s = stack_search(item, s)
  s.pop()
  return s

def stack_get_rand(s):
  rand = randint(0, s.getSize()-1)
  s2 = ArrStack(s.getSize())
  for i in range(rand):
    s2.push(s.pop())
  returnVal = s.top()
  while not s2.isEmpty():
    s.push(s2.pop())
  return returnVal

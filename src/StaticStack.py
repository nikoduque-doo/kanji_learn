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


def stack_search(item, s):
  found = False
  temp = None
  s2 = ArrStack(s.getSize())
  while (not s.isEmpty()) and (item != next(iter(s.top().keys()))):
    s2.push(s.pop())
  if not s.isEmpty():
    found = True
    temp = s.pop()
  while not s2.isEmpty():
    s.push(s2.pop())
  if found:
    s.push(temp)
  return found

def stack_delete(item, s):
  if stack_search(item, s):
    s.pop()
    return True
  return False

def stack_get_rand(s):
  rand = randint(0, s.getSize()-1)
  s2 = ArrStack(s.getSize())
  for i in range(rand):
    s2.push(s.pop())
  returnVal = s.top()
  while not s2.isEmpty():
    s.push(s2.pop())
  return returnVal

test = ArrStack(5)
test.push({1:1})
test.push({2:2})
test.push({3:3})
test.push({4:4})
test.push({5:5})
print(test)
stack_delete(3,test)
print(test)

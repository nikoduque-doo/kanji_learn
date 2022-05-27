from random import randint

class ArrQueue():
  def __init__(self, size=100):
    self.size = size + 1
    self.write = 0
    self.erase = 0
    self.arr = [None]*(size+1)
    
  def __str__(self):
    string = "< "
    eye = self.erase
    while eye != self.write:
      string += str(self.arr[eye]) + " < "
      eye = (eye + 1) % self.size
    return string
    
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

  def get_size(self):
    return self.size

def queue_search(item, q):
  first_element = q.peek()
  if first_element == None:
    return False
  elif first_element.english == item:
    return True
  else:
    q.enqueue(q.dequeue())
    while first_element != q.peek():
      if q.peek().english == item:
        return True
      q.enqueue(q.dequeue())
    return False

def queue_delete(item, q):
  if queue_search(item, q):
    q.dequeue()
    
def queue_get_rand(q):
  first_element = q.peek()
  counter = 0
  if not q.isEmpty():
    q.enqueue(q.dequeue())
    counter += 1
    while first_element != q.peek():
      q.enqueue(q.dequeue())
      counter += 1
  else:
    return None
  num = randint(0,counter - 1)
  for i in range(0,num):
    q.enqueue(q.dequeue())
  return q.peek()

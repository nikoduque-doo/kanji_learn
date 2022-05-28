from math import log
from Vocabulary import JWord

class BinaryHeap:
  def __init__(self, size = 32):
    if isinstance(size, list):
      self.arr = size
      self.maxSize = self.itemCount = len(size)
    else:
      self.arr = [None]*size
      self.maxSize = size
      self.itemCount = 0

  def __str__(self):
    s = "| "
    if self.itemCount > 0:
      for i in range(int(log(self.itemCount, 2)+1)):
        for j in range(2**i):
          index = 2**i + j - 1
          if self.arr[index] != None:
            try:
              s += str(self.arr[index]) + " | "
            except:
              break
        if i != int(int(log(self.itemCount, 2))):
          s += "\n| "
    else:
      s += "|"
    return s
  
  def parent(self, i):
    return int((i-1)/2)

  def leftChild(self, i):
    return (2 * i) + 1

  def rightChild(self, i):
    return 2 * (i + 1)

  def peek(self):
    if self.itemCount > 0:
      return self.arr[0]
    return None

  def swap(self, a, b):
    self.arr[a], self.arr[b] = self.arr[b], self.arr[a]

  def siftUp(self, i):
    if type(self.arr[i]) == JWord:
      while i > 0 and self.arr[self.parent(i)].getDueDay() > self.arr[i].getDueDay():
        self.swap(self.parent(i), i)
        i = self.parent(i)
    else:
      while i > 0 and self.arr[self.parent(i)] > self.arr[i]:
        self.swap(self.parent(i), i)
        i = self.parent(i)

  def siftDown(self, i):
    min = i
    left = self.leftChild(i)
    right = self.rightChild(i)
    if type(self.arr[i]) == JWord:
      if left < self.itemCount and self.arr[min].getDueDay() > self.arr[left].getDueDay():
        min = left
      if right < self.itemCount and self.arr[min].getDueDay() > self.arr[right].getDueDay():
        min = right
    else:
      if left < self.itemCount and self.arr[min] > self.arr[left]:
        min = left
      if right < self.itemCount and self.arr[min] > self.arr[right]:
        min = right
    if i != min:
      self.swap(i, min)
      self.siftDown(min)

  def insert(self, value):
    if self.itemCount >= self.maxSize:
      tempArr = [None]*self.maxSize*2
      for i in range(self.maxSize):
        tempArr[i] = self.arr[i]
      self.arr = tempArr
      self.maxSize *= 2
    self.arr[self.itemCount] = value
    self.siftUp(self.itemCount)
    self.itemCount += 1


  def extractMax(self):
    self.itemCount -= 1
    self.arr[0], self.arr[self.itemCount] = self.arr[self.itemCount], self.arr[0]
    self.siftDown(0)
    return self.arr[self.itemCount]
    
  def changePriority(self, i, value):
    if type(self.arr[i]) == JWord:
      self.arr[i].dueDay, value = value, self.arr[i].dueDay
      if value < self.arr[i].getDueDay():
        self.siftDown(i)
      elif value > self.arr[i].getDueDay():
        self.siftUp(i)
    else:
      self.arr[i], value = value, self.arr[i]
      if value < self.arr[i]:
        self.siftDown(i)
      elif value > self.arr[i]:
        self.siftUp(i)

  def remove(self, i): #missing
    if isinstance(self.arr[i], int):
      self.arr[i] = self.arr[0] + 1 #Only for numeric values
    elif type(self.arr[i]) == JWord:
      self.arr[i].setDueDay(self.arr[0].getDueDay()+1) 
    else:
      self.arr[i] = chr(ord(self.arr[0])+1) #Only for characters
    self.siftUp(i)
    self.extracMax()

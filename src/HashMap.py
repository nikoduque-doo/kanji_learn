from random import randint as r
from LinkList import LinkList
from Nodes import Tag

class HashMap():
  PRIME = 908070605040302010203040506070809 #>max code of word, max digits in tag: 23

  def __init__(self, size = 32):
    self.itemCount = 0
    self.maxSize = size
    self.arr = [None]*size
    for i in range(len(self.arr)):
        self.arr[i] = LinkList()
    self.varA = r(1, HashMap.PRIME)
    self.varB = r(0, HashMap.PRIME)

  def hString(self, word):
    l = len(word)
    code = 0
    if l < 24:
      for i in range(l):
        num = ord(word[l-i-1].lower())
        if num > 96 and num < 123:
          code += (num-96) * (27**i)
        elif num != 32:
          print("Tag has unsupported characters.")
          return None
    else:
      print("Tag is too long.")
      return None
    return ((self.varA * code + self.varB) % HashMap.PRIME) % self.maxSize

  def get(self, key):
    index = self.hString(key)
    linkedL = None
    if index != None:
      linkedL = self.arr[index]
    else:
      return None
    point = linkedL.head
    while point != None:
      if point.getValue().getKey() == key:
        return point.getValue().getWords()
      point = point.getNext()
    return None

  def hasKey(self, key):
    found = self.get(key)
    if found != None:
      return True
    return False

  def set(self, key, item):
    self.setIn(key, item, self.arr)
  
  def setIn(self, key, item, arr):
    index = self.hString(key)
    linkedL = None
    if index != None:
      linkedL = arr[index]
    else:
      return False
    point = linkedL.head
    while point != None:
      if point.getValue().getKey() == key:
        point.getValue().setWords(item)
        self.itemCount += 1
        self.rehash()
        return True
      point = point.getNext()
    linkedL.pushFront(Tag(key, item))
    self.itemCount += 1
    self.rehash()
    return True

  def rehash(self):
    loadFactor = self.itemCount / self.maxSize
    if loadFactor > 0.9:
      newArr = [None]*self.maxSize*2
      for i in range(len(newArr)):
        newArr[i] = LinkList()
      self.varA = r(1, HashMap.PRIME)
      self.varB = r(0, HashMap.PRIME)
      for i in self.arr:
        point = i.head
        while point != None:
          self.setIn(point.getValue().getKey(), point.getValue().getWords(), newArr)
      self.arr = newArr

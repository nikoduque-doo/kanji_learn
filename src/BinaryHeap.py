class BinaryHeap:
  def __init__(self, size = 256):
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
      for i in range(int(math.log(self.itemCount, 2)+1)):
        for j in range(2**i):
          index = 2**i + j - 1
          if self.arr[index] != None:
            try:
              s += str(self.arr[index]) + " | "
            except:
              break
        if i != int(int(math.log(self.itemCount, 2))):
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

  def swap(self, a, b):
    self.arr[a], self.arr[b] = self.arr[b], self.arr[a]

  def siftUp(self, i):
    while i > 0 and self.arr[self.parent(i)] < self.arr[i]:
      self.swap(self.parent(i), i)
      i = self.parent(i)

  def siftDown(self, i):
    max = i
    left = self.leftChild(i)
    right = self.rightChild(i)
    if left < self.itemCount and self.arr[max] < self.arr[left]:
      max = left
    if right < self.itemCount and self.arr[max] < self.arr[right]:
      max = right
    if i != max:
      self.swap(i, max)
      self.siftDown(max)

  def insert(self, value):
    if self.itemCount < self.maxSize:
      self.arr[self.itemCount] = value
      self.siftUp(self.itemCount)
      self.itemCount += 1

  def extractMax(self):
    self.itemCount -= 1
    self.arr[0], self.arr[self.itemCount] = self.arr[self.itemCount], self.arr[0]
    self.siftDown(0)
    return self.arr[self.itemCount]
    
  def changePriority(self, i, value):
    self.arr[i], value = value, self.arr[i]
    if value > self.arr[i]:
      self.siftDown(i)
    elif value < self.arr[i]:
      self.siftUp(i)

  def remove(self, i):
    if isinstance(self.arr[i], int):
      self.arr[i] = self.arr[0] + 1 #Only for numeric values
    else:
      self.arr[i] = chr(ord(self.arr[i])+1) #Only for characters
    self.siftUp(i)
    self.extracMax()
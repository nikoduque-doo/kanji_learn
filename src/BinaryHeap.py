class BinaryHeap:
  def __init__(self, size):
    self.arr = [None]*size
    self.maxSize = size
    self.itemCount = 0

  def parent(self, i):
    return int((i-1)/2)

  def leftChild(self, i):
    return (2 * i) + 1

  def rightChild(self, i):
    return 2 * (i + 1)

  def swap(self, a, b):
    if a < self.itemCount and b < self.itemCount:
      self.arr[a], self.arr[a] = self.arr[b], self.arr[a]

  def siftUp(self, i):
    while i > 0 and self.arr[self.parent(i)] < self.arr[i]:
      self.swap(self.parent(i), i)

  def siftDown(self, i):
    max = i
    left = self.leftChildren(i)
    right = self.rightChildren(i)
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
    self.arr[i] = self.arr[0] + 1 #Only for numeric values
    self.siftUp(i)
    self.extracMax()

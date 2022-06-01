from re import S


class DynamicArray():
    def __init__(self):
        self.itemCount = 0
        self.arr = [None]*32
        self.maxSize = 32
        self.position = 0

    def __str__(self):
        if not self.isEmpty():
            s = str(self.arr[0])
            for i in range(1, self.itemCount):
                s += ", " + str(self.arr[i])
            return s
        return "[]"

  
    def isEmpty(self):
        return self.itemCount == 0 
  
    def insert(self, item):
        if self.itemCount == self.maxSize:
            self.maxSize *= 2 
            tempArr = [None]*self.maxSize
            for i in range(self.itemCount):
                tempArr[i] = self.arr[i]
            self.arr = tempArr
        self.arr[self.itemCount] = item
        self.itemCount += 1

    def delete(self, item):
        if not self.isEmpty():
            if self.find(item):
                self.itemCount -= 1
                self.arr[self.position] = self.arr[self.itemCount]

    def find(self, item):
        for i in range(self.itemCount):
            if self.arr[i] == item:
                self.position = i
                return True
        return False

    def deleteKanji(self, item):
        if not self.isEmpty():
            if self.findKanji(item):
                self.itemCount -= 1
                self.arr[self.position] = self.arr[self.itemCount]

    def findKanji(self, item):
        for i in range(self.itemCount):
            if self.arr[i] != None and self.arr[i].english == item:
                self.position = i
                return True
        return False

    def traverse(self, f):
        for i in range(self.itemCount):
            f(self.arr[i])

    def getSize(self):
        return self.itemCount
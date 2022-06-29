import flashcardgroups_operations as fsg
import Vocabulary
import random
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

    def __len__(self):
        return self.itemCount

    def clear(self):
        self.itemCount = 0
        self.arr = [None]*32
        self.maxSize = 32
        self.position = 0

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

    def deleteUpdating(self, my_dict):
        for i in range(self.itemCount):
            item = self.arr[i]
            self.deleteKanji(item)
            if type(item) is not Vocabulary.JWord:
                word_searched = fsg.get_word_data_graphic(item)
            else:
                word_searched = item
            my_dict["WordsInGroups"] -= 1
            if "noun" in word_searched.part_of_speech or "Noun" in word_searched.part_of_speech:
              my_dict["TotalNouns"] -= 1
            elif "adjective" in word_searched.part_of_speech or "Adjective" in word_searched.part_of_speech:
              my_dict["TotalAdjectives"] -= 1
            elif "verb" in word_searched.part_of_speech or "Verb" in word_searched.part_of_speech:
              my_dict["TotalVerbs"] -= 1
            else:
              my_dict["TotalOthers"] -= 1

    def getRandom(self):
        if not self.isEmpty():
            ind = random.randrange(len(self.arr))
            while self.arr[ind] is None:
                ind = random.randrange(len(self.arr))
            return self.arr[ind]
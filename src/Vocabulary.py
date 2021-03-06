from AVLTree import AVLTree
from datetime import datetime, date

class JWord:
  __slots__ = ("english", "word", "part_of_speech", "meaning", "reading", "easiness", "streak", "interval", "dueDay", "dateCreated")
  jwCount = 0

  def __init__(self, english, word, use, meaning, reading):
    JWord.jwCount += 1
    self.english = english
    self.word = word
    self.part_of_speech = use
    self.meaning = meaning
    self.reading = reading
    self.easiness = 2.5
    self.streak = 0
    self.interval = 0
    self.dueDay = 0 
    self.setDateID()
    self.dateCreated = self.dueDay

  def __str__(self):
    return str(self.word)

  def info(self, fin = "\n"):
    print("The japanese writing for {} is {}, it is read like {}, its part of speech is {} and it means: {}".format(self.english, self.word, self.reading, self.part_of_speech, self.meaning), end = fin)

  def __gt__(self, other):
    return self.compare(self.word, other.word) > 0

  def __ge__(self, other):
    return self.compare(self.word, other.word) > -1

  def __lt__(self, other):
    return self.compare(self.word, other.word) < 0

  def __le__(self, other):
    return self.compare(self.word, other.word) < 1

  def __eq__(self, other):
    if other != None:
      if type(other) == JWord:
        return self.compare(self.word, other.word) == 0
      else:
        return self.compare(self.word, other) == 0
    return False
  
  def rise(self, num = 1):
    self.word[0] = chr(ord(self.word[0]) + num)
  
  def compare(self, this, that):
    for i in range(min(len(this), len(that))):
      if this[i] > that[i]:
        return 1
      elif that[i] > this[i]:
        return -1
    if len(this) != len(that):
      if len(this) > len(that):
        return 1
      else:
        return -1
    else:
      return 0

  def setDateID(self):
    self.dueDay =  datetime.now().timetuple().tm_yday + date.today().year*1000

  def setDueDay(self, num):
    self.dueDay = num

  def getDueDay(self):
    return self.dueDay

  def addToDueDay(self, num):
    self.setDateID()
    year = int(self.dueDay/1000)
    limit = 365
    if year%4 == 0:
      limit += 1
    yearIncrease = int((num + self.dueDay - (year*1000) - 0.1)//limit)
    days = ((num + self.dueDay - (year*1000)) % limit)
    days = limit if days == 0 else days

    self.dueDay = ((year+yearIncrease)*1000) + days

  def updatePriority(self, grade):
    if grade >= 3:
      if self.streak == 0:
        self.interval = 1
      elif self.streak == 1:
        self.interval = 6
      else:
        self.interval = int(self.interval * self.easiness)
      self.streak += 1
    else:
      self.streak = 0
      self.interval = 1
    self.addToDueDay(self.interval)
    self.easiness = self.easiness + (0.1-((5-grade)*(0.08+(0.02*(5-grade)))))
    if self.easiness < 1.3:
      self.easiness = 1.3

  @classmethod
  def getVocabularySize(cls):
    return cls.jwCount

class Kanji:
  __slots__ = ("char", "tree")
  
  def __init__(self, char):
    self.char = char
    self.tree = AVLTree()
  
  def __str__(self):
    return self.char

  def __gt__(self, other):
    if type(other) == Kanji:
      return self.char > other.char
    return self.char > other

  def __ge__(self, other):
    if type(other) == Kanji:
      return self.char >= other.char
    return self.char >= other

  def __lt__(self, other):
    if type(other) == Kanji:
      return self.char < other.char
    return self.char < other

  def __le__(self, other):
    if type(other) == Kanji:
      return self.char <= other.char
    return self.char <= other

  def __eq__(self, other):
    if other != None:
      if type(other) == Kanji:
        return self.char == other.char
      return self.char == other
    return False

  def link(self, word):
    self.tree.insert(word)

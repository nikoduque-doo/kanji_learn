from AVLTree import AVLTree

class JWord:
  __slots__ = ("english", "word", "part_of_speech", "meaning")
  jwCount = 0

  def __init__(self, english, word, use, meaning):
    JWord.jwCount += 1
    self.english = english
    self.word = word
    self.part_of_speech = use
    self.meaning = meaning
  
  def __str__(self):
    return "The japanese writing for {} is {}, its part of speech is {} and it means: {}".format(self.english, self.word, self.part_of_speech, self.meaning)

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
      return self.compare(self.word, other.word) == 0
    return False

  def compare(self, this, that):
    for i in range(max(len(this), len(that))):
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

  def link(self, word):
    self.tree.insert(word)

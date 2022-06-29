from datetime import timedelta, datetime, date
from re import M
from Vocabulary import Kanji, JWord
from AVLTree import AVLTree, BST
from BinaryHeap import BinaryHeap
from OrderedLinkList import OrderedLinkList
from DynamicArray import DynamicArray
from HashMap import HashMap
from random import randint as r
import os.path
import platform
import pickle
import jisho_scrape
import time
import random
import ArrQueue
import RefQueue
import LinkList
import StaticStack

def getPath():
  operatingSystem = platform.system()
  if operatingSystem == "Windows":
    path = os.path.expandvars(R"%HOMEPATH%/Documents/") + "tankaiki"
  elif operatingSystem == "Darwin":
    path = os.path.expanduser(R"~/Documents/") + "tankaiki"
  elif operatingSystem == "Linux":
    path = os.path.expanduser(R"~/Documents/") + "tankaiki"
  if not os.path.exists(path):
    os.mkdir(path)
  return path + "/"

def load_existing_fgroups():
    try:
      pickle_in = open(getPath() + "/my_dict.pickle", "rb")
      current_dict = pickle.load(pickle_in)
      pickle_in.close()
    except:
      pickle_in = open(getPath() + "/my_dict.pickle", "wb")
      pickle_in.close()
      current_dict = {}
    if not "my_kanji" in current_dict:
      current_dict["my_kanji"] = AVLTree()
    if not "my_words" in current_dict:
      current_dict["my_words"] = AVLTree()
    if not "groups" in current_dict:
      current_dict["groups"] = {}
    if not "practice_box" in current_dict:
      current_dict["practice_box"] = BinaryHeap()
    if not "tags" in current_dict:
      current_dict["tags"] = HashMap()
    if not "recent" in current_dict:
      current_dict["recent"] = RefQueue.RefQueue()
    if not "search_results" in current_dict:
      current_dict["search_results"] = DynamicArray()
    if not "TotalWords" in current_dict:
      current_dict["TotalWords"] = 0
    if not "WordsInGroups" in current_dict:
      current_dict["WordsInGroups"] = 0
    if not "TotalNouns" in current_dict:
      current_dict["TotalNouns"] = 0
    if not "TotalVerbs" in current_dict:
      current_dict["TotalVerbs"] = 0
    if not "TotalAdjectives" in current_dict:
      current_dict["TotalAdjectives"] = 0
    if not "TotalOthers" in current_dict:
      current_dict["TotalOthers"] = 0
    #Artifitial creation of structures for test
    if False: #False to deactivate
      def randKanji(id):
        kanji = ""
        for i in range(r(1,4)):
            kanji += chr(r(19968, 40879))
        jw = JWord("english {}".format(id), 
                    kanji, 
                    "use {}".format(id), 
                    "meaning {}".format(id), 
                    "reading {}".format(id))
        return jw

      lis = [None]*100
      for i in range(100):
          lis[i] = randKanji(i)
      for i in lis:
          print(i, end=", ")
      print("")
      """a = DynamicArray()
      s = StaticStack.ArrStack(100)
      q = ArrQueue.ArrQueue(100)
      q2 = RefQueue.RefQueue()
      l = LinkList.LinkList()
      ol = OrderedLinkList()
      bst = BST()
      av = AVLTree()"""
      test1 = DynamicArray()
      test2 = DynamicArray()
      test3 = DynamicArray()
      for j in range(100):
          test1.insert(lis[j])
          test2.insert(lis[j])
          test3.insert(lis[j])
          """i = lis[j]
          a.insert(i)
          s.push(i)
          q.enqueue(i)
          q2.enqueue(i)
          l.pushBack(i)
          ol.insert(i)
          bst.insert(i)
          av.insert(i)"""
      """current_dict["groups"]["a"] = a
      current_dict["groups"]["s"] = s
      current_dict["groups"]["q"] = q
      current_dict["groups"]["q2"] = q2
      current_dict["groups"]["l"] = l
      current_dict["groups"]["ol"] = ol
      current_dict["groups"]["bst"] = bst
      current_dict["groups"]["av"] = av
      current_dict["groups"]["My adjectives"] = av"""
      current_dict["groups"]["1"] = test1
      current_dict["groups"]["2"] = test2
      current_dict["groups"]["3"] = test3

    if False: #Set to True to add to practice box, False to deactivate
      current_dict["practice_box"] = BinaryHeap()
      current_dict["practice_box"].insert(JWord("english", "右", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "壁", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "大きな", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "美しい", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "上手", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "面倒くさい", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "山", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "白", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "海", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "暗い", "Noun", "thing", "asd"))
      current_dict["practice_box"].insert(JWord("english", "走る", "Noun", "thing", "asd"))


    update_recent_words(current_dict)
    return current_dict

def save_changes_to_fgroups(dict_saved:dict):
    pickle_out = open(getPath() + "/my_dict.pickle", "wb")
    pickle.dump(dict_saved,pickle_out)
    pickle_out.close()

def reset():
  os.remove(getPath() + "/my_dict.pickle")
  dict = load_existing_fgroups()
  return dict


def getSizeOfGroup(struc):
  ret = 0
  try:
    ret = struc.getSize()
  except:
    pass
  return ret

def get_word_data(item: None):
    group = False
    if(item == None):
      searchedWord = input("Enter the Word you want to translate: ")
    else:
      searchedWord = item
      group = True
    word_to_be_added = jisho_scrape.add_word(searchedWord.lower(), group)
    return word_to_be_added

def get_word_data_graphic(word):
  searchedWord = word
  word_to_be_added = jisho_scrape.add_word_graphic(searchedWord.lower())
  return word_to_be_added


"""def create_group(gen_dict:dict):
    name = input("Name your flashcard group: ")
    data_structure = input("What Data Structure would you like to create it as? \n\tS = Stack\n\tQ = Queue\n\tQ2 = Reference Queue\n\tL = Linked List\n\tA = Array\n>")
    groups_dict = gen_dict["groups"]

    if(data_structure == "D"):
        groups_dict[name] = {}
    elif(data_structure == "A"):
        size = int(input("How many elements would you like to add? "))
        groups_dict[name] = [None]*(size)
    elif(data_structure == "Q"):
        size = int(input("How many elements would you like to add? "))
        groups_dict[name] = ArrQueue.ArrQueue(size)
    elif(data_structure == "Q2"):
        groups_dict[name] = RefQueue.RefQueue()
    elif(data_structure == "L"):
        groups_dict[name] = LinkList.LinkList()
    elif(data_structure == "S"):
        size = int(input("How many elements would you like to add? "))
        groups_dict[name] = StaticStack.ArrStack(size)
    
    save_changes_to_fgroups(gen_dict)"""

def create_group(gen_dict:dict, name:str, data_structure:str, size = 0):
  groups_dict = gen_dict["groups"]

  if(data_structure == "D"):
      groups_dict[name] = {}
  elif(data_structure == "A"):
      groups_dict[name] = DynamicArray()
  elif(data_structure == "Q"):
      groups_dict[name] = ArrQueue.ArrQueue(size)
  elif(data_structure == "Q2"):
      groups_dict[name] = RefQueue.RefQueue()
  elif(data_structure == "L"):
      groups_dict[name] = LinkList.LinkList()
  elif(data_structure == "S"):
      groups_dict[name] = StaticStack.ArrStack(size)
  elif(data_structure == "AVL"):
      groups_dict[name] = AVLTree()
  elif(data_structure == "BST"):
      groups_dict[name] = BST()
  elif(data_structure == "OL"):
      groups_dict[name] = OrderedLinkList()
    
  save_changes_to_fgroups(gen_dict)

def add_singular_word(struc, item: None, gen_dict):
    word_searched = get_word_data(item)
    if word_searched != None:
        for i in range(len(word_searched.word)):
          if 19968 <= ord(word_searched.word[i]) and ord(word_searched.word[i]) <= 40879:
            kanji = gen_dict["my_kanji"].search(word_searched.word[i])
            if kanji != None:
              kanji.link(word_searched)
            else:
              newK = Kanji(word_searched.word[i])
              newK.link(word_searched)
              gen_dict["my_kanji"].insert(newK)
        

        wordTreeSize = gen_dict["my_words"].getSize()
        gen_dict["my_words"].insert(word_searched)
        if wordTreeSize < gen_dict["my_words"].getSize():
          gen_dict["recent"].enqueue(word_searched)
          gen_dict["practice_box"].insert(word_searched)

        if(type(struc) == dict):
          struc[word_searched.english] = word_searched
        elif(type(struc) == DynamicArray):
          struc.insert(word_searched)
        elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
          struc.enqueue(word_searched)
        elif(type(struc) == LinkList.LinkList):
          struc.pushBack(word_searched)
        elif(type(struc) == StaticStack.ArrStack):
          struc.push(word_searched)
        elif(type(struc) == AVLTree or type(struc) == BST or type(struc) == OrderedLinkList):
          struc.insert(word_searched)

def add_word_with_graphic(struc, word, gen_dict):
  word_searched = get_word_data_graphic(word)
  if word_searched != None:

    wordTreeSize = gen_dict["my_words"].getSize()
    gen_dict["my_words"].insert(word_searched)
    if wordTreeSize < gen_dict["my_words"].getSize():
      gen_dict["recent"].enqueue(word_searched)
      gen_dict["practice_box"].insert(word_searched)

      #Update kanji tree
      for i in range(len(word_searched.word)):
        if 19968 <= ord(word_searched.word[i]) and ord(word_searched.word[i]) <= 40879:
          kanji = gen_dict["my_kanji"].search(word_searched.word[i])
          if kanji != None:
            kanji.link(word_searched)
          else:
            newK = Kanji(word_searched.word[i])
            newK.link(word_searched)
            gen_dict["my_kanji"].insert(newK)

      #Insert in group
      if(type(struc) == dict):
        struc[word_searched.english] = word_searched
      elif(type(struc) == DynamicArray):
        struc.insert(word_searched)
      elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
        struc.enqueue(word_searched)
      elif(type(struc) == LinkList.LinkList):
        struc.pushBack(word_searched)
      elif(type(struc) == StaticStack.ArrStack):
        struc.push(word_searched)
      elif(type(struc) == AVLTree or type(struc) == BST or type(struc) == OrderedLinkList):
        struc.insert(word_searched)
      
      # Update Statistics
      gen_dict["TotalWords"] += 1
      gen_dict["WordsInGroups"] += 1
      if "noun" in word_searched.part_of_speech or "Noun" in word_searched.part_of_speech:
        gen_dict["TotalNouns"] += 1
      elif "adjective" in word_searched.part_of_speech or "Adjective" in word_searched.part_of_speech:
        gen_dict["TotalAdjectives"] += 1
      elif "verb" in word_searched.part_of_speech or "Verb" in word_searched.part_of_speech:
        gen_dict["TotalVerbs"] += 1
      else:
        gen_dict["TotalOthers"] += 1
    
    else:
      print("Word was already saved.")





def search_word(struc, item):
  item = item.lower()
  start_time = time.perf_counter_ns()
  
  found = False
  if(type(struc) == DynamicArray):
    found = struc.findKanji(item)
  elif(type(struc) == dict):
    found = item in struc
  elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
    found = ArrQueue.queue_search(item, struc)
  elif(type(struc) == LinkList.LinkList):
    found = struc.search(item)
  elif(type(struc) == StaticStack.ArrStack):
    found = StaticStack.stack_search(item, struc)

  if(found):
    print("{} is in this flashcardgroup".format(item))
  else:
    print("Word not found in flashcard group")
  end_time = time.perf_counter_ns()
  print(end_time - start_time, "ns")
    
def delete_word(struc, item):
  if(type(struc) == dict):
    struc.pop(item)
  elif(type(struc) == DynamicArray):
    struc.deleteKanji(item)
  elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
    ArrQueue.queue_delete(item, struc)
  elif(type(struc) == LinkList.LinkList):
    struc.remove(item)
  elif(type(struc) == StaticStack.ArrStack):
    StaticStack.stack_delete(item, struc)

def delete_word_graphic(my_dict, struc, item):
  if(type(struc) == dict):
    struc.pop(item)
  elif(type(struc) == DynamicArray):
    struc.deleteKanji(item)
  elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
    ArrQueue.queue_delete(item, struc)
  elif(type(struc) == LinkList.LinkList):
    struc.remove(item)
  elif(type(struc) == StaticStack.ArrStack):
    StaticStack.stack_delete(item, struc)
  save_changes_to_fgroups(my_dict)
  # Update Statistics
  word_searched = get_word_data_graphic(item)
  my_dict["WordsInGroups"] -= 1
  if "noun" in word_searched.part_of_speech or "Noun" in word_searched.part_of_speech:
    my_dict["TotalNouns"] -= 1
  elif "adjective" in word_searched.part_of_speech or "Adjective" in word_searched.part_of_speech:
    my_dict["TotalAdjectives"] -= 1
  elif "verb" in word_searched.part_of_speech or "Verb" in word_searched.part_of_speech:
    my_dict["TotalVerbs"] -= 1
  else:
    my_dict["TotalOthers"] -= 1
  

def get_random_word(struc):
  if(type(struc) == dict):
    key, val = random.choice(list(struc.items()))
    print("The random word is {}: {}".format(key,val))
    return key
  elif(type(struc) == list):
    ind = random.randrange(len(struc))
    while(struc[ind] is None):
      ind = random.randrange(len(struc))
    print("The random word is {}".format(struc[ind]))
  elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
    print(ArrQueue.queue_get_rand(struc))
  elif(type(struc) == LinkList.LinkList):
    print(struc.randomElement())
  elif(type(struc) == StaticStack.ArrStack):
    print(StaticStack.stack_get_rand(struc))


def addAction(struc, word, gen_dict):
  add_word_with_graphic(struc, word, gen_dict)
  save_changes_to_fgroups(gen_dict)

def access_group(gen_dict:dict):
    print("kanji tree test: ", gen_dict["my_kanji"])
    print("Practice heap test:\n", gen_dict["practice_box"])
    print("What flashcard group would you like to access? ")
    groups_dict = gen_dict["groups"]
    for key in groups_dict.keys():
        print(key, end= " | ")
    key_access = input("\nInput your selection: ")
    while(key_access not in groups_dict.keys()):
        key_access = input("No such flashcard group exists. Input your selection: ")
    
    operation = input("Choose an operation to perform on {}: \n\t(A)  Add a word\n\t(P)  Print\n\t(D)  Delete the Flashcard Group\n\t(S)  Search\n\t(R)  Remove a Word\n\t(RW) get a Random Word\n>".format(key_access))
    if(operation == "A"):
        add_singular_word(groups_dict[key_access], None, gen_dict)
        save_changes_to_fgroups(gen_dict)

    elif(operation == "P"):
        print("{}: {}".format(key_access, groups_dict[key_access]))
    
    elif(operation == "D"):
      groups_dict.pop(key_access)
      save_changes_to_fgroups(gen_dict)

    elif(operation == "S"):
      s_word = input("What word would you like to search? ")
      search_word(groups_dict[key_access], s_word)
    
    elif(operation == "R"):
      r_word = input("What word would you like to delete? ")
      start_time = time.perf_counter_ns()
      delete_word(groups_dict[key_access], r_word)
      end_time = time.perf_counter_ns()
      print(end_time - start_time, "ns")

    elif(operation == "RW"):
      start_time = time.perf_counter_ns()
      get_random_word(groups_dict[key_access])
      end_time = time.perf_counter_ns()
      print(end_time - start_time, "ns")

    elif(operation == "dev"):
      filename = input("filename = ")
      fileused = open(os.path.dirname(__file__) + "/../data/" + filename, "r")
      file_list = [line.rstrip('\n') for line in fileused]
      fileused.close()
      counter = 0
      
      start_time = time.monotonic()
      for item in file_list:
        counter += 1
        add_singular_word(groups_dict[key_access], item)
        print("{}/{}".format(counter, len(file_list)))
        save_changes_to_fgroups(gen_dict)
      end_time = time.monotonic()
      print(timedelta(seconds=end_time - start_time))

def get_groups(gen_dict:dict):
  groups_dict = gen_dict["groups"]
  groupsList = []
  for key in groups_dict.keys():
    thisGroup = []
    thisGroup.append(key)
    sizeOfThisGroup = getSizeOfGroup(groups_dict[key])
    thisGroup.append(sizeOfThisGroup)
    groupsList.append(thisGroup)
  return groupsList

def raiseQuestion(jw:JWord):
  ans = input("Type the kana reading for {}, what does it mean?\n>".format(jw.word))
  while ans == "":
    ans = input(">")
  print("The correct writing is: {}, it means: {}".format(jw.reading, jw.meaning))
  grade = input("Rate your answer from 0 to 5.\
                \n\t(0) Utter failure.\
                \n\t(1) Wrong, but recognized the answer.\
                \n\t(2) Wrong. Seems easy to remember, though.\
                \n\t(3) Correct, but required a lot of effort.\
                \n\t(4) Correct. Felt dobious, nonetheless.\
                \n\t(5) Perfect recall.\n>")
  valid = False
  while not valid:
    try:
      grade = int(grade[0])
    except:
      grade = input("Bad input, try again: ")
      continue
    if grade <= 5 and 0 <= grade:
      valid = True
  return grade

def grade_question_with_graphic(gen_dict, jw:JWord, grade:int):
  jw.updatePriority(grade)
  gen_dict["practice_box"].insert(jw)
  save_changes_to_fgroups(gen_dict)

def practice_vocab(gen_dict):
  struc = gen_dict["practice_box"]
  practicing = "Y"
  todayID = datetime.now().timetuple().tm_yday + date.today().year*1000
  while practicing == "Y":
    if struc.peek() == None:
      print("You haven't saved any words yet!")
      practicing = "N"
    elif struc.peek().getDueDay() > todayID:
      print("There aren't any words available for practice at the moment.")
      if struc.peek().getDueDay() == todayID + 1:
        print("The next word will be available tomorrow.")
      else:
        print("The next word will be available in {} days.".format(struc.peek().getDueDay()-todayID))
      practicing = "N"
    else:
      j_word = struc.extractMax()
      grade = raiseQuestion(j_word)
      j_word.updatePriority(grade)
      struc.insert(j_word)

      save_changes_to_fgroups(gen_dict)

      practicing = input("Do you want to continue practicing? (Y/N)\n>")
      while practicing != "Y" and practicing != "N":
        practicing = input(">")

def practice_with_graphic(gen_dict):
  struc = gen_dict["practice_box"]
  todayID = datetime.now().timetuple().tm_yday + date.today().year*1000
  if struc.peek() == None:
    #print("You haven't saved any words yet!")
    return 0
  elif struc.peek().getDueDay() > todayID:
    newID = struc.peek().getDueDay()
    newYear = int(newID/1000)
    thisYear = int(todayID/1000)
    if newYear == thisYear:
      return newID - todayID
    else:
      return thisYear - newYear
  else:
    j_word = struc.extractMax()
    return j_word
    grade = raiseQuestion(j_word)
    j_word.updatePriority(grade)
    struc.insert(j_word)

    #save_changes_to_fgroups(gen_dict)

def update_recent_words(gen_dict):
  q = gen_dict["recent"]
  timeRange = 5
  today = datetime.now().timetuple().tm_yday + date.today().year*1000
  while q.peek() != None and futureDateCode(q.peek().dateCreated, timeRange) < today:
    q.dequeue()
  save_changes_to_fgroups(gen_dict)

def futureDateCode(originalDate, num):
  year = int(originalDate/1000)
  limit = 365
  if year%4 == 0:
    limit += 1
  yearIncrease = int((num + originalDate - (year*1000) - 0.1)//limit)
  days = ((num + originalDate - (year*1000)) % limit)
  days = limit if days == 0 else days

  return ((year+yearIncrease)*1000) + days

def word_range_search(gen_dict, word:str):
  gen_dict["search_results"].clear()
  results = gen_dict["search_results"]
  kanjiTree = gen_dict["my_kanji"]
  foundWord = None
  for i in word:
    kanji = None
    if 19968 <= ord(i) and ord(i) <= 40879:
      kanji = kanjiTree.search(i)
    if kanji != None:
      kanjiRelatives = kanji.tree.toStack()
      while not kanjiRelatives.isEmpty():
        if kanjiRelatives.top() == word:
          foundWord = kanjiRelatives.pop()
        else:
          results.insert(kanjiRelatives.pop())

  print(results, foundWord)
  return foundWord

def tagSearch(gen_dict, tag:str):
  gen_dict["search_results"].clear()
  results = gen_dict["tags"].get(tag)
  if results != None:
    gen_dict["search_results"] = results.toDynamicArray()

def tagWord(jword, tag, gen_dict):
  tags = gen_dict["tags"]
  words = tags.get(tag)
  if words != None:
      words.insert(jword)
  else:
      words = AVLTree()
      words.insert(jword)
      tags.set(tag, words)
  save_changes_to_fgroups(gen_dict)

def update_statistics_deleting_group(struc, my_dict):
  print("I am here")
  print(type(struc))
  if(type(struc) == dict):
    for key in struc:
      struc.pop(key)
      word_searched = get_word_data_graphic(key)
      my_dict["WordsInGroups"] -= 1
      if "noun" in word_searched.part_of_speech or "Noun" in word_searched.part_of_speech:
        my_dict["TotalNouns"] -= 1
      elif "adjective" in word_searched.part_of_speech or "Adjective" in word_searched.part_of_speech:
        my_dict["TotalAdjectives"] -= 1
      elif "verb" in word_searched.part_of_speech or "Verb" in word_searched.part_of_speech:
        my_dict["TotalVerbs"] -= 1
      else:
        my_dict["TotalOthers"] -= 1
  elif(type(struc) == DynamicArray):
    struc.deleteUpdating(my_dict)
  elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
    while struc.isEmpty():
      word_searched = struc.dequeue()
      my_dict["WordsInGroups"] -= 1
      if "noun" in word_searched.part_of_speech or "Noun" in word_searched.part_of_speech:
        my_dict["TotalNouns"] -= 1
      elif "adjective" in word_searched.part_of_speech or "Adjective" in word_searched.part_of_speech:
        my_dict["TotalAdjectives"] -= 1
      elif "verb" in word_searched.part_of_speech or "Verb" in word_searched.part_of_speech:
        my_dict["TotalVerbs"] -= 1
      else:
        my_dict["TotalOthers"] -= 1
  elif(type(struc) == LinkList.LinkList):
    while not struc.isEmpty():
      print("I am here now")
      word_searched = struc.popFront()
      my_dict["WordsInGroups"] -= 1
      if "noun" in word_searched.part_of_speech or "Noun" in word_searched.part_of_speech:
        my_dict["TotalNouns"] -= 1
      elif "adjective" in word_searched.part_of_speech or "Adjective" in word_searched.part_of_speech:
        my_dict["TotalAdjectives"] -= 1
      elif "verb" in word_searched.part_of_speech or "Verb" in word_searched.part_of_speech:
        my_dict["TotalVerbs"] -= 1
      else:
        my_dict["TotalOthers"] -= 1
  elif(type(struc) == StaticStack.ArrStack):
    while struc.isEmpty():
      word_searched = struc.pop()
      my_dict["WordsInGroups"] -= 1
      if "noun" in word_searched.part_of_speech or "Noun" in word_searched.part_of_speech:
        my_dict["TotalNouns"] -= 1
      elif "adjective" in word_searched.part_of_speech or "Adjective" in word_searched.part_of_speech:
        my_dict["TotalAdjectives"] -= 1
      elif "verb" in word_searched.part_of_speech or "Verb" in word_searched.part_of_speech:
        my_dict["TotalVerbs"] -= 1
      else:
        my_dict["TotalOthers"] -= 1
  save_changes_to_fgroups(my_dict)
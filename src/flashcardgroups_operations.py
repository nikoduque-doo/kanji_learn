from datetime import timedelta, datetime, date
from keyword import iskeyword
from this import d
from Vocabulary import Kanji, JWord
from AVLTree import AVLTree
from BinaryHeap import BinaryHeap
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
  operatingSystem = platform.system();
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
      current_dict["tags"] = AVLTree()
    if not "recent" in current_dict:
      current_dict["recent"] = RefQueue.RefQueue()
    update_recent_words(current_dict)
    return current_dict

def save_changes_to_fgroups(dict_saved:dict):
    pickle_out = open(getPath() + "/my_dict.pickle", "wb")
    pickle.dump(dict_saved,pickle_out)
    pickle_out.close()

def getSizeOfGroup(struc):
  if(type(struc) == dict or type(struc) == list):
    ret = len(struc)
  elif (type(struc) == ArrQueue.ArrQueue):
    ret = struc.get_size()
  elif (type(struc) == RefQueue.RefQueue):
    ret = struc.getSize()
  elif(type(struc) == LinkList.LinkList):
    ret = struc.size()
  elif(type(struc) == StaticStack.ArrStack):
    ret = struc.getSize()
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

def create_group(gen_dict:dict, name:str, data_structure:str):
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
    
  save_changes_to_fgroups(gen_dict)

def add_singular_word(struc, item: None, gen_dict):
    word_searched = get_word_data(item)
    if word_searched != None:
        for i in range(len(word_searched.word)):
          if 19968 <= ord(word_searched.word[i]) and ord(word_searched.word[i]) <= 40879:
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
        elif(type(struc) == list):
          struc.append(word_searched)
        elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
          struc.enqueue(word_searched)
        elif(type(struc) == LinkList.LinkList):
          struc.pushBack(word_searched)
        elif(type(struc) == StaticStack.ArrStack):
          struc.push(word_searched)

def add_word_with_graphic(struc, word, gen_dict):
  word_searched = get_word_data_graphic(word)
  if word_searched != None:
        for i in range(len(word_searched.word)):
          if 19968 <= ord(word_searched.word[i]) and ord(word_searched.word[i]) <= 40879:
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
        elif(type(struc) == list):
          struc.append(word_searched)
        elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
          struc.enqueue(word_searched)
        elif(type(struc) == LinkList.LinkList):
          struc.pushBack(word_searched)
        elif(type(struc) == StaticStack.ArrStack):
          struc.push(word_searched)

def search_word(struc, item):
  item = item.lower()
  start_time = time.perf_counter_ns()
  
  found = False
  if(type(struc) == list):
    for element in struc:
      if element is not None and element.english == item:
        found = True
        break
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
  elif(type(struc) == list):
    for element in struc:
      if element is not None and element.english == item:
        struc.remove(element)
  elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
    ArrQueue.queue_delete(item, struc)
  elif(type(struc) == LinkList.LinkList):
    struc.remove(item)
  elif(type(struc) == StaticStack.ArrStack):
    StaticStack.stack_delete(item, struc)

def get_random_word(struc):
  if(type(struc) == dict):
    key, val = random.choice(list(struc.items()))
    print("The random word is {}: {}".format(key,val))
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
        if type(groups_dict[key_access]) == list:
            print(key_access, end= ": ")
            for item in groups_dict[key_access]:
              if item is not None:
                print(item, end= " ")
            print()
        else:
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

def access_group(key, groups_dict):
  groups_dict[key]
  ## Faltaría poder mostrar todas las palabras guardadas en la estructura 


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

def update_recent_words(gen_dict):
  q = gen_dict["recent"]
  timeRange = 5
  today = datetime.now().timetuple().tm_yday + date.today().year*1000
  while q.peek() != None and futureDateCode(q.peek().dateCreated, timeRange) < today:
    q.unqueue()
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
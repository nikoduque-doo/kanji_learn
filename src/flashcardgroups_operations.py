from datetime import timedelta
from Vocabulary import Kanji
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
    return current_dict

def save_changes_to_fgroups(dict_saved:dict):
    pickle_out = open(getPath() + "/my_dict.pickle", "wb")
    pickle.dump(dict_saved,pickle_out)
    pickle_out.close()

def get_word_data(item: None):
    group = False
    if(item == None):
      searchedWord = input("Enter the Word you want to translate: ")
    else:
      searchedWord = item
      group = True
    word_to_be_added = jisho_scrape.add_word(searchedWord.lower(), group)
    return word_to_be_added

def create_group(gen_dict:dict):
    name = input("Name your flashcard group: ")
    data_structure = input("What Data Structure would you like to create it as? \n\tS = Stack\n\tQ = Queue\n\tQ2 = Reference Queue\n\tL = Linked List\n\tA = Array\n>")
    
    if(data_structure == "D"):
        gen_dict[name] = {}
    elif(data_structure == "A"):
        size = int(input("How many elements would you like to add? "))
        gen_dict[name] = [None]*(size)
    elif(data_structure == "Q"):
        size = int(input("How many elements would you like to add? "))
        gen_dict[name] = ArrQueue.ArrQueue(size)
    elif(data_structure == "Q2"):
        gen_dict[name] = RefQueue.RefQueue()
    elif(data_structure == "L"):
        gen_dict[name] = LinkList.LinkList()
    elif(data_structure == "S"):
        size = int(input("How many elements would you like to add? "))
        gen_dict[name] = StaticStack.ArrStack(size)
    
    save_changes_to_fgroups(gen_dict)

def add_singular_word(struc, item: None, gen_dict):
    word_searched = get_word_data(item)
    if word_searched != None:
      
        for i in range(len(word_searched.word)):
          if 19968 <= ord(word_searched.word[i]) and ord(word_searched.word[i]) <= 40879:
            newK = Kanji(word_searched.word[i])
            newK.link(word_searched)
            gen_dict["my_kanji"].insert(newK)
            
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

def access_group(gen_dict:dict):
    print("kanji tree test: ", gen_dict["my_kanji"])
    print("What flashcard group would you like to access? ")
    for key in gen_dict.keys():
        print(key, end= " | ")
    key_access = input("\nInput your selection: ")
    while(key_access not in gen_dict.keys()):
        key_access = input("No such flashcard group exists. Input your selection: ")
    
    operation = input("Choose an operation to perform on {}: \n\t(A)  Add a word\n\t(P)  Print\n\t(D)  Delete the Flashcard Group\n\t(S)  Search\n\t(R)  Remove a Word\n\t(RW) get a Random Word\n>".format(key_access))
    if(operation == "A"):
        add_singular_word(gen_dict[key_access], None, gen_dict)
        save_changes_to_fgroups(gen_dict)

    elif(operation == "P"):
        if type(gen_dict[key_access]) == list:
            print(key_access, end= ": ")
            for item in gen_dict[key_access]:
              if item is not None:
                print(item, end= " ")
            print()
        else:
            print("{}: {}".format(key_access, gen_dict[key_access]))
    
    elif(operation == "D"):
      gen_dict.pop(key_access)
      save_changes_to_fgroups(gen_dict)

    elif(operation == "S"):
      s_word = input("What word would you like to search? ")
      search_word(gen_dict[key_access], s_word)
    
    elif(operation == "R"):
      r_word = input("What word would you like to delete? ")
      start_time = time.perf_counter_ns()
      delete_word(gen_dict[key_access], r_word)
      end_time = time.perf_counter_ns()
      print(end_time - start_time, "ns")

    elif(operation == "RW"):
      start_time = time.perf_counter_ns()
      get_random_word(gen_dict[key_access])
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
        add_singular_word(gen_dict[key_access], item)
        print("{}/{}".format(counter, len(file_list)))
        save_changes_to_fgroups(gen_dict)
      end_time = time.monotonic()
      print(timedelta(seconds=end_time - start_time))

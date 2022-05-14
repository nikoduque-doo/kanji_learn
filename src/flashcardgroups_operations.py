import os.path
import pickle
import jisho_scrape
import ArrQueue
import RefQueue
import LinkList
import Stack
import time
from datetime import timedelta
from random import randint

#Base para buscar en una cola y eliminar de la misma. +get random
def queue_search(item, q):
  first_element = q.peek()
  if first_element == None:
    return False
  elif next(iter(first_element.keys())) == item:
    return True
  else:
    q.enqueue(q.dequeue())
    while first_element != q.peek():
      if next(iter(q.peek().keys())) == item:
        return True
      q.enqueue(q.dequeue())
    return False
  #Falta Guardar Cambios en fgroups

def queue_delete(item, q):
  if queue_search(item, q):
    q.dequeue()
    
def queue_get_rand(q):
  first_element = q.peek()
  counter = 0
  if not q.isEmpty():
    q.enqueue(q.dequeue())
    counter += 1
    while first_element != q.peek():
      q.enqueue(q.dequeue())
      counter += 1
  else:
    return None
  num = randint(0,counter - 1)
  for i in range(0,num):
    q.enqueue(q.dequeue())
  return q.peek()

def load_existing_fgroups():
    pickle_in = open(os.path.dirname(__file__) + "/../other/my_dict.pickle", "rb")
    current_dict = pickle.load(pickle_in)
    pickle_in.close()
    return current_dict

def save_changes_to_fgroups(dict_saved:dict):
    pickle_out = open(os.path.dirname(__file__) + "/../other/my_dict.pickle", "wb")
    pickle.dump(dict_saved,pickle_out)
    pickle_out.close()

def get_word_data(item: None):
    group = False
    if(item == None):
      searchedWord = input("Enter the Word you want to translate: ")
    else:
      searchedWord = item
      group = True
    word_to_be_added = jisho_scrape.add_word(searchedWord, group)
    return word_to_be_added

def create_group(gen_dict:dict):
    name = input("Name your flashcard group: ")
    data_structure = input("What Data Structure would you like to create it as? (P = Pile, Q = Queue, Q2 = Reference Queue, L = Linked List) " )
    
    if(data_structure == "D"):
        gen_dict[name] = {}
    elif(data_structure == "Q"):
        size = int(input("How many elements would you like to add? "))
        gen_dict[name] = ArrQueue.ArrQueue(size)
    elif(data_structure == "Q2"):
        gen_dict[name] = RefQueue.RefQueue()
    elif(data_structure == "L"):
        gen_dict[name] = LinkList.LinkList()
    elif(data_structure == "P"):
        gen_dict[name] = Stack.Stack()
    
    save_changes_to_fgroups(gen_dict)

def add_singular_word(struc, item: None):
    word_searched = get_word_data(item)
    word_inserted = {word_searched.name_dict : word_searched.data_dict}
    if(type(struc) == dict):
      struc[word_searched.name_dict] = word_searched.data_dict
    elif (type(struc) == ArrQueue.ArrQueue or type(struc) == RefQueue.RefQueue):
      struc.enqueue(word_inserted)
    elif(type(struc) == LinkList.LinkList):
      struc.pushBack(word_inserted)
    elif(type(struc) == Stack.Stack):
        #gen_dict[name] = Stack.Stack()
      struc.push(word_inserted)

def access_group(gen_dict:dict):
    print("What flashcard group would you like to access?")
    for key in gen_dict.keys():
        print(key, end= " | ")
    key_access = input("\nInput your selection: ")
    while(key_access not in gen_dict.keys()):
        key_access = input("No such flashcard group exists. Input your selection: ")
    
    operation = input("Choose an operation to perform on {}: Add a word (A), Print(P), Delete(D)".format(key_access))
    if(operation == "A"):
        add_singular_word(gen_dict[key_access], None)
        save_changes_to_fgroups(gen_dict)

    elif(operation == "P"):
        if type(gen_dict[key_access]) == dict:
            print("{}: {}".format(key_access, gen_dict[key_access]))
        else:
            print("{}: {}".format(key_access, gen_dict[key_access]))
    
    elif(operation == "D"):
      gen_dict.pop(key_access)
      save_changes_to_fgroups(gen_dict)
    
    elif(operation == "dev"):
      filename = input("filename = ")
      fileused = open(os.path.dirname(__file__) + "/" + filename, "r")
      file_list = fileused.readlines()
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
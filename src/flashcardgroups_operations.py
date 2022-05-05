import os.path
import pickle
import jisho_scrape
import ArrQueue


def load_existing_fgroups():
    pickle_in = open(os.path.dirname(__file__) + "/../other/my_dict.pickle", "rb")
    current_dict = pickle.load(pickle_in)
    pickle_in.close()
    return current_dict

def save_changes_to_fgroups(dict_saved:dict):
    pickle_out = open(os.path.dirname(__file__) + "/../other/my_dict.pickle", "wb")
    pickle.dump(dict_saved,pickle_out)
    pickle_out.close()

def get_word_data():
    current_dict = {}
    continueOperation = "Y"

    while(continueOperation == "Y"):
        searchedWord = input("Enter the Word you want to translate: ")
        jisho_scrape.add_word(searchedWord, current_dict)
        #continueOperation = input("Continue searching words? (Y/N)")
        #while(continueOperation != "Y" and continueOperation != "N"):
            #continueOperation = input("Continue searching words? (Y/N)")
    return current_dict

def create_group(gen_dict:dict):
    name = input("Name your flashcard group: ")
    data_structure = input("What Data Structure would you like to create it as? (D = Dictionary, Q = Queue) " )
    if(data_structure == "D"):
        gen_dict[name] = {}
    elif(data_structure == "Q"):
        size = int(input("How many elements would you like to add? "))
        gen_dict[name] = ArrQueue.ArrQueue(size)
    #Aqui irán los demás tipos de estructuras de datos
    save_changes_to_fgroups(gen_dict)

def access_group(gen_dict:dict):
    print("What flashcard group would you like to access?")
    for key in gen_dict.keys():
        print(key)


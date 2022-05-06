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
    searchedWord = input("Enter the Word you want to translate: ")
    word_to_be_added = jisho_scrape.add_word(searchedWord)
    return word_to_be_added

def create_group(gen_dict:dict):
    name = input("Name your flashcard group: ")
    data_structure = input("What Data Structure would you like to create it as? (D = Dictionary, Q = Queue) " )
    
    #Acá es donde se implementa la creación de las distintas est datos
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
    key_access = input("Input your selection: ")
    while(key_access not in gen_dict.keys()):
        key_access = input("No such flashcard group exists. Input your selection: ")
    
    operation = input("Choose an operation to perform on {}: Add a word (A), Print(P), Delete(D)".format(key_access))
    if(operation == "A"):
        word_searched = get_word_data()
        word_inserted = {word_searched.name_dict : word_searched.data_dict}
        if(type(gen_dict[key_access]) == dict):
            gen_dict[key_access][word_searched.name_dict] = word_searched.data_dict
        elif (type(gen_dict[key_access]) == ArrQueue.ArrQueue):
            gen_dict[key_access].enqueue(word_inserted)

        save_changes_to_fgroups(gen_dict)

    elif(operation == "P"):
            if type(gen_dict[key_access]) == dict:
                print("{}: {}".format(key_access, gen_dict[key_access]))
            else:
                print("{}: {}".format(key_access, gen_dict[key_access]))
    
    elif(operation == "D"):
        gen_dict.pop(key_access)
        save_changes_to_fgroups(gen_dict)


                




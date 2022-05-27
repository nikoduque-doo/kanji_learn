from jisho_api.word import Word
from Vocabulary import JWord
import os.path
import json
#utilizando el api de el diccionario Jisho, se extraen datos de la página (scraping) y se organizan en un
#diccionario. Este diccionario luego es introducido en otro diccionario que se pasa como argumento

class dict_word:

    def __init__(self, name):
        self.name_dict = name
        self.data_dict = {}

    def add_data(self, label, data):
        self.data_dict[label] = data

    def get_data(self, key):
        return self.data_dict[key]
    
    def __str__(self) -> str:
        return self.name_dict + ": " + json.dumps(self.data_dict, indent= 4, ensure_ascii=False)

def request_word(word_requested):
    req = Word.request(word_requested)
    newJWord = None
    include_keys = { 
        'data' : {0 : {"japanese" : {0 : {"word":True, "reading":True}}, "senses" : {0 : {"english_definitions":True, "parts_of_speech":True}}}},
    }

    try:
        reqDict = req.dict(include= include_keys)
    except:
        print("Word not recognized or not found")
    else:
        
        newJWord = JWord(word_requested,\
                         reqDict["data"][0]["japanese"][0]["word"],\
                         reqDict["data"][0]["senses"][0]["parts_of_speech"][0],\
                         reqDict["data"][0]["senses"][0]["english_definitions"][0],\
                         reqDict["data"][0]["japanese"][0]["reading"])
        
        return newJWord

def add_word(word_requested, group: False):
    try:
        reqJWord = request_word(word_requested)
    except:
        print("Word not recognized or not found")
    else:
        if(group == False):
            reqJWord.info()

            addTo = input("Do you want to add this word to your custom list? (Y/N)")
            while(addTo != "Y" and addTo != "N"):
                addTo = input("Do you want to add this word to your custom list? (Y/N)")
        
            if(addTo == "Y"):
                print("Done! Word added successfully")
                return reqJWord
            else:
                print("Word not added")
                return None
        else:
            return reqJWord

def add_words_from_file(filename):

    fileused = open(filename, "r")
    file_list = fileused.readlines()
    fileused.close()
    wordslist = []

    for item in file_list:
        print(item)
        wordslist.append(request_word(item))

    return wordslist

from jisho_api.word import Word
#utilizando el api de el diccionario Jisho, se extraen datos de la página (scraping) y se organizan en un
#diccionario. Este diccionario luego es introducido en otro diccionario que se pasa como argumento

class dict_word:
    data_dict = {}

    def __init__(self, name):
        self.name_dict = name

    def add_data(self, label, data):
        self.data_dict[label] = data

    def get_data(self, key):
        return self.data_dict[key]


def add_word(wordR):
    req = Word.request(wordR)
    organizedDict = dict_word(wordR)

    include_keys = { 
        'data' : {0 : {"slug":True, "senses" : {0 : {"english_definitions":True, "parts_of_speech":True}}}},
    }

    try:
        reqDict = req.dict(include= include_keys)
    except:
        print("Word not recognized or not found")
    else:
        
        organizedDict.add_data("kanji", reqDict["data"][0]["slug"])
        organizedDict.add_data("part_of_speech", reqDict["data"][0]["senses"][0]["parts_of_speech"][0])
        organizedDict.add_data("meaning", reqDict["data"][0]["senses"][0]["english_definitions"][0])

        print("The kanji for {} is  {}, its part of speech is {} and it means: {}".format(organizedDict.name_dict, organizedDict.get_data("kanji"), organizedDict.get_data("part_of_speech"), organizedDict.get_data("meaning")))

        addTo = input("Do you want to add this word to your custom list? (Y/N)")
        while(addTo != "Y" and addTo != "N"):
            addTo = input("Do you want to add this word to your custom list? (Y/N)")
    
        if(addTo == "Y"):
            print("Done! Word added successfully")
            return organizedDict
        else:
            print("Word not added")
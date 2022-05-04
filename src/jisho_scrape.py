from jisho_api.word import Word
#utilizando el api de el diccionario Jisho, se extraen datos de la página (scraping) y se organizan en un
#diccionario. Este diccionario luego es introducido en otro diccionario que se pasa como argumento

def add_word(wordR, targetDict):
    req = Word.request(wordR)
    organizedDict = {}
    include_keys = { 
        'data' : {0 : {"slug":True, "senses" : {0 : {"english_definitions":True, "parts_of_speech":True}}}},
    }

    try:
        reqDict = req.dict(include= include_keys)
    except:
        print("Word not recognized or not found")
    else:
        organizedDict["kanji"] = reqDict["data"][0]["slug"]
        organizedDict["part_of_speech"] = reqDict["data"][0]["senses"][0]["parts_of_speech"][0]
        organizedDict["meaning"] = reqDict["data"][0]["senses"][0]["english_definitions"][0]

        print("The kanji for {} is  {}, its part of speech is {} and it means: {}".format(wordR, organizedDict["kanji"], organizedDict["part_of_speech"], organizedDict["meaning"]))

        addTo = input("Do you want to add this word to your custom list? (Y/N)")
        while(addTo != "Y" and addTo != "N"):
            addTo = input("Do you want to add this word to your custom list? (Y/N)")
    
        if(addTo == "Y"):
            targetDict[wordR] = organizedDict
            print("Done! Word added successfully")
        else:
            print("Word not added")
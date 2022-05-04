import jisho_scrape

my_dict = {}
if __name__ == "__main__":
    continueOperation = "Y"
    
    while(continueOperation == "Y"):
        searchedWord = input("Enter the Word you want to translate: ")
        jisho_scrape.add_word(searchedWord, my_dict)
        continueOperation = input("Continue searching words? (Y/N)")
        while(continueOperation != "Y" and continueOperation != "N"):
            continueOperation = input("Continue searching words? (Y/N)")
    
    print(my_dict)

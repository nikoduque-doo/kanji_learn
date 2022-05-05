
import flashcardgroups_operations as fsg

my_dict = fsg.load_existing_fgroups()
        
if __name__ == "__main__":
    print("Welcome!")
    groupReadorAcc = input("Do you want to create a new group of flashcards or access an existing one? (C/A) ")
    while(groupReadorAcc != "C" and groupReadorAcc != "A"):
        groupReadorAcc = input("Do you want to create a new group of flashcards or read an existing one? (C/A) ")
        
    if(groupReadorAcc == "A"):
        if(my_dict):
            fsg.access_group(my_dict)
        else:
            print("No flashcard groups available, create a group")
            fsg.create_group(my_dict)
    elif(groupReadorAcc == "C"):
        fsg.create_group(my_dict)

import flashcardgroups_operations as fsg
import os

my_dict = fsg.load_existing_fgroups()
        
if __name__ == "__main__":
    print("Welcome!")
    exit_status = "N"
    while(exit_status=="N"):
        groupReadorAcc = input("Do you want to create a new group of flashcards or access an existing one? (C/A) ")
        while(groupReadorAcc != "C" and groupReadorAcc != "A"):
            groupReadorAcc = input("Do you want to create a new group of flashcards or read an existing one? (C/A) ")

        os.system('cls')
        if(groupReadorAcc == "A"):
            if(my_dict):
                fsg.access_group(my_dict)
            else:
                print("No flashcard groups available, create a group")
                fsg.create_group(my_dict)
        elif(groupReadorAcc == "C"):
            fsg.create_group(my_dict)

        input("Do you want to exit the program?: (Y/N) ")
        os.system('cls')
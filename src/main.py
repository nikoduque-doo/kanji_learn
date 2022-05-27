from AVLTree import AVLTree
import flashcardgroups_operations as fsg
import os
import platform
import sys

sys.setrecursionlimit(1000000000)

my_dict = fsg.load_existing_fgroups()

if not "my_kanji" in my_dict:
    my_dict["my_kanji"] = AVLTree()
if not "groups" in my_dict:
    my_dict["groups"] = {}

if __name__ == "__main__":
    operatingSystem = platform.system();
    if operatingSystem == "Windows":
        os.system('cls')
    else:
        os.system("clear")
    print("Welcome!")
    exit_status = "N"
    while(exit_status=="N"):
        groupReadorAcc = input("Do you want to create a new group of flashcards or access an existing one? (C/A) ")
        while(groupReadorAcc != "C" and groupReadorAcc != "A"):
            groupReadorAcc = input("Do you want to create a new group of flashcards or read an existing one? (C/A) ")

        if operatingSystem == "Windows":
            os.system('cls')
        else:
            os.system("clear")
        if(groupReadorAcc == "A"):
            if(my_dict["groups"]):
                fsg.access_group(my_dict)
            else:
                print("No flashcard groups available, create a group")
                fsg.create_group(my_dict)
        elif(groupReadorAcc == "C"):
            fsg.create_group(my_dict)

        exit_status = input("Do you want to exit the program?: (Y/N) ")
        if operatingSystem == "Windows":
            os.system('cls')
        else:
            os.system("clear")

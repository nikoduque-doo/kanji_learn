from unicodedata import numeric
import flashcardgroups_operations as fsg
import os
import platform
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

sys.setrecursionlimit(1000000000)

my_dict = fsg.load_existing_fgroups()

class FirstScreen(Screen):
    pass
    # Para hacer el cambio de screen desde el código de python hay que hacerlo así
    #def onClickButton(self, widget):
        #widget.current = "Home"

class HomeScreen(Screen):
    pass

class LoadingScreen(Screen):
    pass

class WordScreen(Screen):
    pass

class FlashcardScreen(Screen):
    pass

class ViewFlashcardsScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class AllFlashcards(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        numberOfButtons = 0
        for i in range(3):
            if i == 0:
                l = Label(text="Saved Flashcards groups", color=(0 , 0 , 0 , 1), size_hint=(.8, .2))
                self.add_widget(l)
            else:
                l = Label(size_hint=(.1, .2))
                self.add_widget(l)
        if(my_dict["groups"]):
            groups = fsg.get_groups(my_dict)
            print(groups)
            for group in groups:
                if (numberOfButtons == 11):
                    break
                b = Button(text=str(group[0] + "\n" + str(group[1])), size_hint=(.3, .2))
                self.add_widget(b)
                numberOfButtons += 1
        b = Button(text="View All", size_hint=(.3, .2))
        self.add_widget(b)

kv = Builder.load_file('Tankaiki.kv')

class TankaikiApp(App):
    def build(self):
        return kv



if __name__ == "__main__":
    TankaikiApp().run()
    operatingSystem = platform.system()



    exit_status = "Y"
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

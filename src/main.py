from cProfile import label
from unicodedata import numeric
import flashcardgroups_operations as fsg
import os
import platform
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

sys.setrecursionlimit(1000000000)

my_dict = fsg.load_existing_fgroups()
chosen = None
labelText = str(chosen)

sm = ScreenManager()

class FirstScreen(Screen):
    # pass
    # Para hacer el cambio de screen desde el código de python hay que hacerlo así
    def onClickButton(self):
        sm.add_widget(HomeScreen())
        sm.transition.direction = "left"
        sm.current = "Home"
        sm.remove_widget(sm.children[1])

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

class FlashcardGroupScreen(Screen):
    def on_pre_enter(self):
        print(self.children)
        self.clear_widgets()
        fgsc = FlashcardGroupScreenContents()
        fgsc.on_pre_enter()
        self.add_widget(fgsc)

class WindowManager(ScreenManager):
    pass

class TopBar(BoxLayout):
    def onClickHomeButton(self):
        sm.add_widget(HomeScreen())
        sm.transition.direction = "right"
        sm.current = "Home"
        sm.remove_widget(sm.children[1])

class AllFlashcards(StackLayout):
    # def takeMeHome(self, instance):
    #     App.manager.current = "ViewFlashcards"

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
            # view_all_btn = Button(text = "View All", size_hint=(.3, .2))
            # view_all_btn.bind(on_press = self.takeMeHome)#(AllFlashcards))
            # self.add_widget(view_all_btn)
            groups = fsg.get_groups(my_dict)
            for group in groups:
                if (numberOfButtons == 11):
                    break
                b = Label(text=str(group[0] + "\n" + str(group[1])), size_hint=(.3, .2), color=(0, 0, 0, 1))
                self.add_widget(b)
                numberOfButtons += 1
        else:
            b = Label(text="No flashcards groups saved", size_hint=(.8, .2), color=(0, 0, 0, 1), halign="right", valign="middle")
            self.add_widget(b)
    



from random import randint as r
class AllFlashcards2(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """b1 = Button(text="update", size_hint=(.5,None), size=(0,dp(40)))
        b1.bind(on_release = self.update)
        self.add_widget(b1)"""
        for i in my_dict["groups"].keys():
            struc_size = str(fsg.getSizeOfGroup(my_dict["groups"][i]))
            b = Button(text=i+": "+struc_size, size_hint=(.5,None), size=(0,dp(40)))
            #b.bind(on_release = self.update)
            self.add_widget(b)
        # for i in range(r(7,15)):
        #     b = Button(text=str(i), size_hint=(.5,None), size=(0,dp(40)))
        #     self.add_widget(b)

    def onClickButton(self):
        sm.add_widget(ViewFlashcardsScreen())
        sm.transition.direction = "left"
        sm.current = "ViewFlashcards"
        sm.remove_widget(sm.children[1])

class ViewAllFlashcards(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if(my_dict["groups"]):
            groups = fsg.get_groups(my_dict)
            for group in groups:
                b = Label(text=str(group[0] + "\n" + str(group[1])), size_hint=(.3, .2), color=(0, 0, 0, 1))
                self.add_widget(b)
        else:
            b = Label(text="No flashcards groups saved", size_hint=(.3, .2), color=(0, 0, 0, 1))
            self.add_widget(b)

# class ScrollViewAllFlashcards(ScrollView):
#     pass
        
class FlashcardsContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def onValidate(self, thisWidget):
        chosen = thisWidget.text
        if (chosen not in my_dict["groups"].keys()):
            thisWidget.text = "Not an group. Try again"
            chosen = None
        else:
            global labelText
            labelText = str(thisWidget.text)
            sm.add_widget(FlashcardGroupScreen())
            sm.current = "FlashcardGroup"
            sm.remove_widget(sm.children[1])
        
# Falta poner las palabras !!

class FlashcardGroupScreenContents(BoxLayout):
    def on_pre_enter(self):
        fcgc = FlashCardGroupContents()
        fcgc.on_pre_enter()

class LabelFlashcardGroup(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = Label(text=str(labelText), color=(0, 0, 0, 1))
        self.add_widget(l)

    def on_pre_enter(self):
        self.clear_widgets()
        self.__init__()

class FlashCardGroupContents(BoxLayout):
    def on_pre_enter(self):
        lfcg = LabelFlashcardGroup()
        lfcg.on_pre_enter()

    # if chosen != None:
    #     labelText = StringProperty(chosen)
    # else:
    #     labelText = StringProperty("No flashcardSelected")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def onPressAddButton(self, Widget):
        # Falta arreglar este botón de navegación!!
        Widget.current = "AddWord"
        # groups_dict = my_dict["groups"]
        # fsg.addAction(groups_dict[chosen], my_dict)
        
        
class ViewAllWords(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        #words = fsg.access_group(chosen, my_dict["groups"])

class AddWordContents(BoxLayout):
    if chosen != None:
        labelText = StringProperty(chosen)
    else:
        labelText = StringProperty("No flashcardSelected")


class TankaikiApp(App):
    def build(self):
        sm.add_widget(FirstScreen())
        return sm



if __name__ == "__main__":
    TankaikiApp().run()
    operatingSystem = platform.system()



    exit_status = "Y"
    while(exit_status=="N"):
        groupReadorAcc = input("What do you want to do?\n\t(C) create a new group of flashcards\n\t(A) access an existing group of flashcards\n\t(P) practice your vocabulary\n>")
        while(groupReadorAcc != "C" and groupReadorAcc != "A" and groupReadorAcc != "P"):
            groupReadorAcc = input("What do you want to do?\n\t(C) create a new group of flashcards\n\t(A) access an existing group of flashcards\n\t(P) practice your vocabulary\n>")

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
        elif(groupReadorAcc == "P"):
            fsg.practice_vocab(my_dict)

        exit_status = input("Do you want to exit the program?: (Y/N) ")
        if operatingSystem == "Windows":
            os.system('cls')
        else:
            os.system("clear")

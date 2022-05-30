import flashcardgroups_operations as fsg
from unicodedata import name, numeric
from random import randint as r
from Vocabulary import JWord
from cProfile import label
from cgitb import text
from tkinter import N
import platform
import sys
import os


from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

sys.setrecursionlimit(1000000000)

my_dict = fsg.load_existing_fgroups()
chosen = None
labelText = str(chosen)

sm = ScreenManager()

#Japanese font:
#https://github.com/public-domain/mona
LabelBase.register(name="mona", fn_regular="mona.ttf")


class FirstScreen(Screen):
    # Para hacer el cambio de screen desde el código de python hay que hacerlo así
    def onClickButton(self):
        sm.add_widget(HomeScreen())
        sm.transition.direction = "left"
        sm.current = "Home"
        sm.remove_widget(sm.children[1])

class HomeScreen(Screen):
    pass

class PracticeScreen(Screen):
    stButton = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        PracticeScreen.stButton = Button(text="start", on_press=self.start, size_hint=(.5,None), size=(0,dp(40)), pos_hint={"x": 0})
        self.add_widget(PracticeScreen.stButton)


    def start(self, self2 = None):
        self.remove_widget(PracticeScreen.stButton)
        psi = PracticeScreenInteractive()
        self.add_widget(psi)
        psi.getNextQuestion()

class PracticeScreenInteractive(Screen):
    def getNextQuestion(self, self2=None):
        self.clear_widgets()
        jw = fsg.practice_with_graphic(my_dict)
        if isinstance(jw, int):
            if jw == 0:
                lab1 = Label(text = "You haven't saved any words yet!", size_hint=(1,.3), font_name='mona')
            elif jw > 0:
                txt = "There aren't any words available for practice at the moment."
                if jw == 1:
                    txt += "\nThe next word will be available tomorrow."
                else:
                    txt += "\nThe next word will be available in {} days.".fromat(jw)
                lab1 = Label(text = txt, size_hint=(1,.3), font_name='mona')
            else:
                txt = "The next word will be available in {} years, try adding a new word!".format(jw * -1)
                lab1 = Label(text = txt, size_hint=(1,.3), font_name='mona')
            self.add_widget(lab1)
            contb = Button(text = "Continue", size_hint=(.5,None), size=(0,dp(40)), pos_hint={"x": .5})
            contb.bind(on_press = self.getNextButton)
        else:
            lab = Label(text = jw.word+"?", size_hint=(1,.3), font_name='mona')
            self.add_widget(lab)
            bl = BoxLayout(orientation = "horizontal")
            b0 = Button(text = "0", size_hint=(.5,None), size=(0,dp(40)))
            b0.bind(on_press = lambda x:self.gradeQuestion(jw, 0))
            bl.add_widget(b0)
            b1 = Button(text = "1", size_hint=(.5,None), size=(0,dp(40)))
            b1.bind(on_press = lambda x:self.gradeQuestion(jw, 1))
            bl.add_widget(b1)
            b2 = Button(text = "2", size_hint=(.5,None), size=(0,dp(40)))
            b2.bind(on_press = lambda x:self.gradeQuestion(jw, 2))
            bl.add_widget(b2)
            b3 = Button(text = "3", size_hint=(.5,None), size=(0,dp(40)))
            b3.bind(on_press = lambda x:self.gradeQuestion(jw, 3))
            bl.add_widget(b3)
            b4 = Button(text = "4", size_hint=(.5,None), size=(0,dp(40)))
            b4.bind(on_press = lambda x:self.gradeQuestion(jw, 4))
            bl.add_widget(b4)
            b5 = Button(text = "5", size_hint=(.5,None), size=(0,dp(40)))
            b5.bind(on_press = lambda x:self.gradeQuestion(jw, 5))
            bl.add_widget(b5)
            self.add_widget(bl)
    
    def getNextButton(self):
        self.clear_widgets()
        b = Button(text = "Next Question", size_hint=(.5,None), size=(0,dp(40)), pos_hint={"x": .5})
        b.bind(on_press = self.getNextQuestion)
        self.add_widget(b)
    
    def gradeQuestion(self, jw, grade):
        fsg.grade_question_with_graphic(my_dict ,jw, grade)
        self.getNextButton()

class LoadingScreen(Screen):
    pass

class WordScreen(Screen):
    pass

class FlashcardScreen(Screen):
    pass

class ViewFlashcardsScreen(Screen):
    pass


class WordConfirmation(Screen):
    pass

class WordNotAdded(Screen):
    pass

class NewGroup(Screen):
    pass

class WordInformationScreen(Screen):
    pass

##########| Section pertaining group words start |##########
############################################################

class AllWordsInsideGroup(StackLayout):
    struc_key = None
    update = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setUp()
        AllWordsInsideGroup.update = self.setUp

    def setUp(self):
        self.clear_widgets()
        if AllWordsInsideGroup.struc_key != None:
            my_dict["groups"][AllWordsInsideGroup.struc_key].traverse(self.setWords)

    def setWords(self, jw:JWord):
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(40)), font_name='mona')
        b.bind(on_press = lambda x: self.word_contents(jw))
        self.add_widget(b)
    
    def word_contents(self, jw:JWord):
        global word_data
        word_data = jw
        """self.clear_widgets()
        self.add_widget(WordInformation())"""
        sm.add_widget(WordInformationScreen())
        sm.transition.direction = "left"
        sm.current = "WordInformationScreen"
        sm.remove_widget(sm.children[1])


#This one is found at home screen
class AllFlashcards2(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """b1 = Button(text="update", size_hint=(.5,None), size=(0,dp(40)))
        b1.bind(on_release = self.update)
        self.add_widget(b1)"""
        for i in my_dict["groups"].keys():
            struc_size = str(fsg.getSizeOfGroup(my_dict["groups"][i]))
            b = JButton(text=i+": "+struc_size, size_hint=(.5,None), size=(0,dp(40)), custom_label=i)
            b.bind(on_release = b.update)
            self.add_widget(b)
        # for i in range(r(7,15)):
        #     b = Button(text=str(i), size_hint=(.5,None), size=(0,dp(40)))
        #     self.add_widget(b)

class JButton(Button):
    def __init__(self, custom_label, **kwargs):
        super().__init__(**kwargs)
        self.custom_label = custom_label
    
    def update(self, self2):
        print("Structures Test\nKanji tree:")
        print(my_dict["my_kanji"])
        print("Words tree:")
        print(my_dict["my_words"])
        print("Practice heap:")
        print(my_dict["practice_box"])
        print("Recent words queue:")
        print(my_dict["recent"])
        print("Tags tree")
        print(my_dict["tags"])
        FlashcardGroupScreen.setText(self.custom_label)

class FlashcardGroupScreen(Screen):
    def on_pre_enter(self):
        print(self.children)
        self.clear_widgets()
        fgsc = FlashcardGroupScreenContents()
        fgsc.on_pre_enter()
        self.add_widget(fgsc)

    
    def setWord(self, jw:JWord):
        b = Button(text = jw.word, size_hint=(.5, .5), font_name='mona')
        self.add_widget(b)

    def addRecentWords(self):
        my_dict["recent"].traverse(self.setWord)

    @classmethod
    def setText(self, struc_name):
        global labelText
        labelText = struc_name
        sm.add_widget(FlashcardGroupScreen())
        sm.transition.direction = "left"
        sm.current = "FlashcardGroup"
        sm.remove_widget(sm.children[1])

        AllWordsInsideGroup.struc_key = struc_name
        AllWordsInsideGroup.update()


class FlashcardGroupScreenContents(BoxLayout):
    def on_pre_enter(self):
        fcgc = FlashCardGroupContents()
        fcgc.on_pre_enter()


class AddWord(Screen):
    def on_pre_enter(self):
        awc = AddWordContents()
        awc.on_pre_enter()

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
        sm.add_widget(AddWord())
        sm.transition.direction = "left"
        sm.current = "AddWord"
        sm.remove_widget(sm.children[1])
        ######## Flow Idea:
        ######## Add Word -> GetWordData() -> WordConfirmation -> 1) Yes -> AddWord() -> WordInfo o 2) No -> WordNotAdded







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
            thisWidget.text = "Not a group. Try again"
            chosen = None
        else:
            global labelText
            labelText = str(thisWidget.text)
            sm.add_widget(FlashcardGroupScreen())
            sm.current = "FlashcardGroup"
            sm.remove_widget(sm.children[1])




##########################################################
##########| Section pertaining group words end |##########




##########| Section pertaining recent words start |##########
#############################################################

class AllRecentWords(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        my_dict["recent"].traverse(self.setWords)
    
    def setWords(self, jw:JWord):
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(40)), font_name='mona')
        self.add_widget(b)

#This one is found at home screen
class RecentFlashcards(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        struc_size = str(fsg.getSizeOfGroup(my_dict["recent"]))
        b = Button(text="Recently added"+": "+struc_size, size_hint=(.5,None), size=(0,dp(40)))
        b.bind(on_release = RecentFlashcards.onClickButton)
        self.add_widget(b)

    def onClickButton(obj):
        RecentWordsScreen.setText("Recently added")

class RecentWordsScreen(Screen):
    def on_pre_enter(self):
        print(self.children)
        self.clear_widgets()
        fgsc = RecentWordsScreenContents()
        fgsc.on_pre_enter()
        self.add_widget(fgsc)

    
    def setWord(self, jw:JWord):
        b = Button(text = jw.word, size_hint=(.5, .5), font_name='mona')
        self.add_widget(b)

    def addRecentWords(self):
        my_dict["recent"].traverse(self.setWord)

    @classmethod
    def setText(self, struc_name):
        global labelText
        labelText = struc_name
        sm.add_widget(RecentWordsScreen())
        sm.transition.direction = "left"
        sm.current = "RecentWords"
        sm.remove_widget(sm.children[1])

class RecentWordsScreenContents(BoxLayout):
    def on_pre_enter(self):
        fcgc = RecentWordsContents()
        fcgc.on_pre_enter()

class RecentWordsContents(BoxLayout):
    def on_pre_enter(self):
        lfcg = LabelRecentWords()
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

class LabelRecentWords(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = Label(text=str(labelText), color=(0, 0, 0, 1))
        self.add_widget(l)

    def on_pre_enter(self):
        self.clear_widgets()
        self.__init__()

###########################################################
##########| Section pertaining recent words end |##########


class NewGroup(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class TopBar(BoxLayout):
    def onClickHomeButton(self):
        if sm.current != "Home":
            sm.add_widget(HomeScreen())
            sm.transition.direction = "right"
            sm.current = "Home"
            sm.remove_widget(sm.children[1])

    def onClickStartPractice(self):
        if sm.current != "PracticePage":
            sm.add_widget(PracticeScreen())
            sm.transition.direction = "left"
            sm.current = "PracticePage"
            sm.remove_widget(sm.children[1])
    
        

class BottomRightOptions(BoxLayout):
    def onClickAddGroup(self):
        sm.add_widget(NewGroup())
        sm.transition.direction = "left"
        sm.current = "NewGroup"
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



class AddGroupW(StackLayout):

    def ask_size(self, name, struc):
        self.name = name
        self.struc = struc
        self.clear_widgets()
        layout1 = BoxLayout(orientation='horizontal', size_hint= (1, .2))
        lbl1 = Label(text = "How many elements should it have?", color = (0 , 0 , 0 , 1), size_hint = (1, .2))
        layout1.add_widget(lbl1)
        layout2 = BoxLayout(orientation='horizontal', size_hint= (1, .3))
        space1 = Label(text = " ")
        textI = TextInput(multiline = False, size_hint= (.5, .25))
        textI.bind(on_text_validate = self.createFromSize)
        space2 = Label(text = " ")
        layout2.add_widget(space1)
        layout2.add_widget(textI)
        layout2.add_widget(space2)

        self.add_widget(layout1)
        self.add_widget(layout2)

    def createFromSize(self, instance):
        size = instance.text
        print("Check it out " + size + " " + str(size.isnumeric()))
        if(size.isnumeric()):
            print("This happens")
            self.create_group_and_return(my_dict, self.name, self.struc, int(size))
        else:
            if size == "":
                instance.text = "No name was given"
            else:
                instance.text = "Invalid Size"

    def searchvalidate(self, thisWidget, Widget):
        chosen = thisWidget.text.strip()
        if (chosen not in my_dict["groups"].keys() and chosen != ""):
            self.clear_widgets()

            layout1 = BoxLayout(orientation='vertical')
            lbl1 = Label(text = "What kind of Data Structure should it be?", color = (0 , 0 , 0 , 1), size_hint = (1, .2))
            layout1.add_widget(lbl1)

            layout2 = BoxLayout(orientation='vertical')
            Arrbtn = Button(text = "Array")
            Arrbtn.bind(on_press = lambda x: self.ask_size(chosen, "A"))
            LLbtn = Button(text = "Linked List")
            LLbtn.bind(on_press = lambda x:self.create_group_and_return(my_dict, chosen, "L", 0))
            Qbtn = Button(text = "Queue")
            Qbtn.bind(on_press = lambda x: self.ask_size(chosen, "Q"))
            Q2btn = Button(text = "Reference Queue")
            Q2btn.bind(on_press = lambda x:self.create_group_and_return(my_dict, chosen, "Q2", 0))
            Sbtn = Button(text = "Stack")
            Sbtn.bind(on_press = lambda x: self.ask_size(chosen, "S"))
            AVLbtn = Button(text = "AVL Tree")
            AVLbtn.bind(on_press = lambda x:self.create_group_and_return(my_dict, chosen, "AVL", 0))
            BSTbtn = Button(text = "Binary Search Tree")
            BSTbtn.bind(on_press = lambda x:self.create_group_and_return(my_dict, chosen, "BST", 0))
            OLLbtn = Button(text = "Ordered Linked List")
            OLLbtn.bind(on_press = lambda x:self.create_group_and_return(my_dict, chosen, "OL", 0))
            layout2.add_widget(Arrbtn)
            layout2.add_widget(LLbtn)
            layout2.add_widget(Qbtn)
            layout2.add_widget(Q2btn)
            layout2.add_widget(Sbtn)
            layout2.add_widget(AVLbtn)
            layout2.add_widget(BSTbtn)
            layout2.add_widget(OLLbtn)
            layout1.add_widget(layout2)
            

            self.add_widget(layout1)
        else:
            if chosen == "":
                thisWidget.text = "No name was given"
            else:
                thisWidget.text = "Group with the same name already exists"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def create_group_and_return(self, gen_dict:dict, name:str, data_structure:str, size = 0):
        fsg.create_group(gen_dict, name, data_structure, size)

        sm.add_widget(HomeScreen())
        sm.transition.direction = "right"
        sm.current = "Home"
        sm.remove_widget(sm.children[1])


class AddWordContents(BoxLayout):
        # if chosen != None:
     #     labelText = StringProperty(chosen)
     # else:
     #     labelText = StringProperty("No flashcardSelected")
     def on_pre_enter(self):
         lfcg = LabelFlashcardGroup()
         lfcg.on_pre_enter()

     def onValidate(self, widget):
         global word
         word = widget.text
         global word_data
         word_data = fsg.get_word_data_graphic(word)
         print(word_data)
         if word_data != None:
             sm.add_widget(WordConfirmation())
             sm.transition.direction = "left"
             sm.current = "WordConfirmation"
             sm.remove_widget(sm.children[1])
         else:
             sm.add_widget(WordNotAdded())
             sm.transition.direction = "left"
             sm.current = "WordNotAdded"
             sm.remove_widget(sm.children[1])


class WordConfirmationContents(BoxLayout):
    def on_pre_enter(self):
        lfg = LabelFlashcardGroup()
        lfg.on_pre_enter()


class WordInformation(BoxLayout):
    def on_pre_enter(self):
        self.clear_widgets()
        self.__init__()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l1 = Label(text = "English: " + str(word_data.english), color = (0, 0, 0, 1))
        self.add_widget(l1)
        l2 = Label(text = "Kanji: " + str(word_data.word), font_name='mona', color = (0, 0, 0, 1))
        self.add_widget(l2)
        l3 = Label(text = "Reading: " + str(word_data.reading), font_name='mona', color = (0, 0, 0, 1))
        self.add_widget(l3)
        l4 = Label(text = "Part of speech: " + str(word_data.part_of_speech), color = (0, 0, 0, 1))
        self.add_widget(l4)
        l5 = Label(text = "Meaning: " + str(word_data.meaning), color = (0, 0, 0, 1))
        self.add_widget(l5)


#self.english, self.word, self.reading, self.part_of_speech, self.meaning
class WordConfirmationButtons(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bYes = Button(text = "Save Word")
        bYes.bind(on_release = self.saveWord)
        self.add_widget(bYes)
        bNo = Button(text = "Don't save word")
        bNo.bind(on_release = self.notSaveWord)
        self.add_widget(bNo)

    def saveWord(self, instance):
        groups_dict = my_dict["groups"]
        fsg.addAction(groups_dict[labelText], word, my_dict)
        FlashcardGroupScreen.setText(labelText)

    def notSaveWord(self, instance):
        global word_data
        word_data = None
        FlashcardGroupScreen.setText(labelText)


class TankaikiApp(App):
    def build(self):
        sm.add_widget(FirstScreen())
        return sm



if __name__ == "__main__":
    TankaikiApp().run()
    operatingSystem = platform.system()



    exit_status = "N"
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

import time
import flashcardgroups_operations as fsg
from Vocabulary import JWord
from StaticStack import ArrStack

import platform
import sys
import os
import random

from kivy.app import App
from kivy.metrics import dp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy import resources

# To use with pyinstaller
# if getattr(sys, 'frozen', False):
#     # this is a Pyinstaller bundle
#     resources.resource_add_path(sys._MEIPASS)
#     resources.resource_add_path(os.path.join(sys._MEIPASS, 'resources'))
# resources.resource_add_path(os.getcwd()+'\\src\\resources')

sys.setrecursionlimit(1000000000)

my_dict = fsg.load_existing_fgroups()
chosen = None
labelText = str(chosen)

sm = ScreenManager()
backQueue = ArrStack()

randomw = None

#Algorithm SM-2, (C) Copyright SuperMemo World, 1991. 
#https://www.supermemo.com

#Japanese font:
#https://github.com/public-domain/mona
font = resources.resource_find("mona.ttf")
# To use with pyinstaller
# LabelBase.register(name="mona", fn_regular=font)

# To use with the console
LabelBase.register(name="mona", fn_regular="resources/mona.ttf")

class WindowManager(ScreenManager):
    pass

class FirstScreen(Screen):
    def onClickButton(self):
        sm.add_widget(HomeScreen())
        sm.transition.direction = "left"
        sm.current = "Home"
        sm.remove_widget(sm.children[1])


##############| Section pertaining Home start |#############
############################################################

class HomeScreen(Screen):
    pass


class TopBar(BoxLayout):
    def onClickHomeButton(self):
        print(my_dict["practice_box"])
        if sm.current != "Home":
            sm.add_widget(HomeScreen())
            sm.transition.direction = "right"
            sm.current = "Home"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])

    def onClickStartPractice(self):
        if sm.current != "PracticePage":
            sm.add_widget(PracticeScreen())
            sm.transition.direction = "left"
            sm.current = "PracticePage"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])
    
    def onSearch(self, this):
        searchTerm = this.text.strip()
        if searchTerm != "":
            SearchResultsScreen.setText(searchTerm)
        
    def onPressBackButton(self):
        prev = backQueue.pop()
        sm.add_widget(prev)
        sm.transition.direction = "right"
        sm.current = prev.name
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])

    def onClickOptions(self):
        if sm.current != "Options":
            sm.add_widget(OptionsScreen())
            sm.transition.direction = "left"
            sm.current = "Options"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])


class TopBarHome(BoxLayout):
    def onClickHomeButton(self):
        print(my_dict["practice_box"])
        if sm.current != "Home":
            sm.add_widget(HomeScreen())
            sm.transition.direction = "right"
            sm.current = "Home"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])

    def onClickStartPractice(self):
        if sm.current != "PracticePage":
            sm.add_widget(PracticeScreen())
            sm.transition.direction = "left"
            sm.current = "PracticePage"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])
    
    def onSearch(self, this):
        searchTerm = this.text.strip()
        if searchTerm != "":
            SearchResultsScreen.setText(searchTerm)
    
    def onPressBackButton(self):
        prev = backQueue.pop()
        sm.add_widget(prev)
        sm.transition.direction = "right"
        sm.current = prev.name
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


    def onClickOptions(self):
        if sm.current != "Options":
            sm.add_widget(OptionsScreen())
            sm.transition.direction = "left"
            sm.current = "Options"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])
    

class BottomRightOptions(BoxLayout):
    def onClickAddGroup(self):
        sm.add_widget(NewGroup())
        sm.transition.direction = "left"
        sm.current = "NewGroup"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


spoilerButtonState = [False, False]

class RandomWord(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global randomw
        if randomw is None:
            randomw = self.random_word()
        
        label1 = Label(text = "Random Word", color = ( 0 , 0 , 0 , 1), font_name='mona')
        self.add_widget(label1)
        if randomw is not None:
            label2 = Label(text = randomw.word, color = ( 0 , 0 , 0 , 1), font_name='mona', font_size='50dp')
            self.add_widget(label2)
            if spoilerButtonState[0] is False:
                button1 = Button(text ='Reading Spoiler')
                button1.bind(on_press = lambda x: self.spoilerPress("r"))
                self.add_widget(button1)
            else:
                label3 = Label(text = randomw.reading, color = ( 0 , 0 , 0 , 1), font_name='mona')
                self.add_widget(label3)
            
            if spoilerButtonState[1] is False:
                button2 = Button(text ='Meaning Spoiler')
                button2.bind(on_press = lambda x: self.spoilerPress("m"))
                self.add_widget(button2)
            else:
                label4 = Label(text = randomw.meaning, color = ( 0 , 0 , 0 , 1), font_name='mona')
                self.add_widget(label4)
        else:
            label2 = Label(text = "No words available", color = ( 0 , 0 , 0 , 1), font_name='mona')
            self.add_widget(label2)
        
        label5 = Label(text = "", size_hint=(1, .5))
        self.add_widget(label5)

    def spoilerPress(self, spoil):
        if spoil is "r":
            spoilerButtonState[0] = True
        elif spoil is "m":
            spoilerButtonState[1] = True
        self.clear_widgets()
        self.__init__()

    def on_pre_enter(self):
        self.clear_widgets()
        self.__init__()

    def random_word(self):
        if len(my_dict["groups"]) > 0:
            randomkey = random.choice(list(my_dict["groups"].keys()))
            randomitem = my_dict["groups"][randomkey].getRandom()
            return randomitem
        else:
            return None
    


##########################################################
#############| Section pertaining Home end |##############


##########| Section pertaining options screen start |##########
###############################################################

class OptionsScreen(Screen):
    def on_pre_enter(self):
        opsC = OptionsScreenContents()
        opsC.on_pre_enter()
    
    def reset(self):
        global my_dict 
        my_dict = fsg.reset()
        sm.add_widget(HomeScreen())
        sm.transition.direction = "right"
        sm.current = "Home"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])



class OptionsScreenContents(BoxLayout):
    def on_pre_enter(self):
        self.clear_widgets()
        opC = OptionsContents()
        opC.on_pre_enter()
        self.add_widget(opC)


class OptionsContents(BoxLayout):
    label1 = StringProperty("")
    label2 = StringProperty("")
    label3 = StringProperty("")
    label4 = StringProperty("")
    label5 = StringProperty("")
    label6 = StringProperty("")
    label7 = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label1 = "Total Words saved in the app: " + str(my_dict["TotalWords"])
        self.label2 = "Total words in groups: " + str(my_dict["WordsInGroups"])
        self.label3 = "Total flashcard groups saved: " + str(len(my_dict["groups"]))
        self.label4 = "Total Nouns saved: " + str(my_dict["TotalNouns"])
        self.label5 = "Total Verbs saved: " + str(my_dict["TotalVerbs"])
        self.label6 = "Total Adjectives saved: " + str(my_dict["TotalAdjectives"])
        self.label7 = "Total words of other type saved: " + str(my_dict["TotalOthers"])

    def on_pre_enter(self):
        self.clear_widgets()
        self.__init__()


###########################################################
##########| Section pertaining options screen end |########


############| Section pertaining practice start |###########
############################################################

class PracticeScreen(Screen):
    stButton = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        PracticeScreen.stButton = Button(text="start", on_press=self.start, size_hint=(.5,None), size=(0,dp(40)), pos_hint={'center_x':.5, 'center_y':.5})
        self.add_widget(PracticeScreen.stButton)

    def start(self, self2 = None):
        self.remove_widget(PracticeScreen.stButton)
        psi = PracticeScreenInteractive()
        self.add_widget(psi)
        psi.getNextQuestion()


class PracticeScreenInteractive(Screen):
    questionWord = None
    showButton = None
    questionText = None

    def getNextQuestion(self, self2=None):
        self.clear_widgets()
        jw = fsg.practice_with_graphic(my_dict)
        if isinstance(jw, int):
            if jw == 0:
                lab1 = Label(text = "You haven't saved any words yet!", size_hint=(1,.3))
            elif jw > 0:
                txt = "There aren't any words available for practice at the moment."
                if jw == 1:
                    txt += "\nThe next word will be available tomorrow."
                else:
                    txt += "\nThe next word will be available in {} days.".format(jw)
                lab1 = Label(pos_hint={'center_x':.5, 'center_y':.5}, text = txt, size_hint=(1,.3), font_size ='25sp')
            else:
                txt = "The next word will be available in {} years, try adding a new word!".format(jw * -1)
                lab1 = Label(pos_hint={'center_x':.5, 'center_y':.5}, text = txt, size_hint=(1,.3), font_size ='25sp')
            self.add_widget(lab1)
            contb = Button(text = "Return home", size_hint=(.5,None), size=(0,dp(50)), pos_hint={'center_x':.5}, font_size='30dp')
            contb.bind(on_press = self.returnHome)
            self.add_widget(contb)
        else:
            jwtxt = "What's the pronunciation for \n{}? What does it mean?".format(jw.word)
            lab = Label(pos_hint={'center_x':.5, 'center_y':.5}, text = jwtxt, size_hint=(1,.3), font_size ='50sp', font_name='mona')
            self.add_widget(lab)
            b = Button(text = "Show Answer", size_hint=(.5,None), size=(0,dp(50)), pos_hint={'center_x':.5}, font_size='30dp')
            b.bind(on_press = self.showAnswer)
            self.add_widget(b)
            PracticeScreenInteractive.showButton = b
            PracticeScreenInteractive.questionWord = jw
            PracticeScreenInteractive.questionText = lab
    
    def getNextButton(self):
        self.clear_widgets()
        b = Button(text = "Get Question", size_hint=(.5,None), size=(0,dp(50)), pos_hint={'center_x':.5}, font_size='30dp')
        b.bind(on_press = self.getNextQuestion)
        self.add_widget(b)

    def showAnswer(self, self2 = None):
        self.remove_widget(PracticeScreenInteractive.showButton)
        self.remove_widget(PracticeScreenInteractive.questionText)
        jw = PracticeScreenInteractive.questionWord
        jwtxt = "The correct reading of {} is {}, it means: {}.".format(jw.word,jw.reading,jw.meaning)
        bl = BoxLayout(orientation = "horizontal")
        b0 = Button(text = "0", size_hint=(.5,None), size=(0,dp(50)), font_size='30dp')
        b0.bind(on_press = lambda x:self.gradeQuestion(0))
        bl.add_widget(b0)
        b1 = Button(text = "1", size_hint=(.5,None), size=(0,dp(50)), font_size='30dp')
        b1.bind(on_press = lambda x:self.gradeQuestion(1))
        bl.add_widget(b1)
        b2 = Button(text = "2", size_hint=(.5,None), size=(0,dp(50)), font_size='30dp')
        b2.bind(on_press = lambda x:self.gradeQuestion(2))
        bl.add_widget(b2)
        b3 = Button(text = "3", size_hint=(.5,None), size=(0,dp(50)), font_size='30dp')
        b3.bind(on_press = lambda x:self.gradeQuestion(3))
        bl.add_widget(b3)
        b4 = Button(text = "4", size_hint=(.5,None), size=(0,dp(50)), font_size='30dp')
        b4.bind(on_press = lambda x:self.gradeQuestion(4))
        bl.add_widget(b4)
        b5 = Button(text = "5", size_hint=(.5,None), size=(0,dp(50)), font_size='30dp')
        b5.bind(on_press = lambda x:self.gradeQuestion(5))
        bl.add_widget(b5)
        self.add_widget(bl)
        txt = "Rate your answer from 0 to 5.\
            \n        (0) Utter failure.\
            \n        (1) Wrong, but recognized the answer.\
            \n        (2) Wrong. Seems easy to remember, though.\
            \n        (3) Correct, but required a lot of effort.\
            \n        (4) Correct. Felt dobious, nonetheless.\
            \n        (5) Perfect recall.\
            \n\n\n"+jwtxt
        lab = Label(pos_hint={'center_x':.5, 'center_y':.5}, text = txt, size_hint=(1,.5), font_size ='25sp', font_name='mona')
        self.add_widget(lab)

    def gradeQuestion(self, grade):
        fsg.grade_question_with_graphic(my_dict ,PracticeScreenInteractive.questionWord, grade)
        self.getNextButton()

    def returnHome(self, self2 = None):
        sm.add_widget(HomeScreen())
        sm.transition.direction = "left"
        sm.current = "Home"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])

##########################################################
###########| Section pertaining practice end |############


##########| Section pertaining group words start |##########
############################################################

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
        FlashcardGroupScreen.setText(self.custom_label)

#This one is found at home screen
class AllFlashcards2(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in my_dict["groups"].keys():
            struc_size = str(fsg.getSizeOfGroup(my_dict["groups"][i]))
            b = JButton(text=i+": "+struc_size, size_hint=(.5,None), size=(0,dp(40)), custom_label=i)
            b.bind(on_release = b.update)
            self.add_widget(b)


class LabelFlashcardGroup(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        l = Label(text=str(labelText), color=(0, 0, 0, 1))
        self.add_widget(l)

    def on_pre_enter(self):
        self.clear_widgets()
        self.__init__()


class FlashcardGroupScreen(Screen):
    def on_pre_enter(self):
        print(self.children)
        self.clear_widgets()
        fgsc = FlashcardGroupScreenContents()
        fgsc.on_pre_enter()
        self.add_widget(fgsc)
    
    def setWord(self, jw:JWord):
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(50)), font_name='mona', font_size='30dp', background_normal="resources/bb1.png", background_down="resources/bb2.png")
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
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])
        AllWordsInsideGroup.struc_key = struc_name
        AllWordsInsideGroup.update()


class FlashcardGroupScreenContents(BoxLayout):
    def on_pre_enter(self):
        fcgc = FlashCardGroupContents()
        fcgc.on_pre_enter()
    
    def onPressGroupDeleteButton(self, instance):
        struc = my_dict["groups"][labelText]
        fsg.update_statistics_deleting_group(struc, my_dict)
        print(labelText)
        my_dict["groups"].pop(labelText)
        fsg.save_changes_to_fgroups(my_dict)
        AllWordsInsideGroup.struc_key = None
        sm.add_widget(HomeScreen())
        sm.transition.direction = "right"
        sm.current = "Home"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


class FlashCardGroupContents(BoxLayout):
    def on_pre_enter(self):
        lfcg = LabelFlashcardGroup()
        lfcg.on_pre_enter()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def onPressAddButton(self):
        sm.add_widget(AddWord())
        sm.transition.direction = "left"
        sm.current = "AddWord"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


class AllWordsInsideGroup(StackLayout):
    struc_key = None
    update = None

    def __init__(self, **kwargs):
        start_time = time.perf_counter_ns()
        super().__init__(**kwargs)
        self.setUp()
        AllWordsInsideGroup.update = self.setUp
        end_time = time.perf_counter_ns()
        print(end_time - start_time, "ns")

    def setUp(self):
        self.clear_widgets()
        if AllWordsInsideGroup.struc_key != None:
            if(type(my_dict["groups"][AllWordsInsideGroup.struc_key]) != list):
                my_dict["groups"][AllWordsInsideGroup.struc_key].traverse(self.setWords)
            else:
                for element in my_dict["groups"][AllWordsInsideGroup.struc_key]:
                    if element != None:
                        self.setWords(element)

    def setWords(self, jw:JWord):
        WordInformation.showTags = True
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(50)), font_name='mona', font_size='30dp', background_normal="resources/bb1.png", background_down="resources/bb2.png")
        b.bind(on_press = lambda x: self.word_contents(jw))
        self.add_widget(b)
    
    def word_contents(self, jw:JWord):
        global word_data
        word_data = jw
        sm.add_widget(WordInformationScreen())
        sm.transition.direction = "left"
        sm.current = "WordInformationScreen"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


class WordInformationScreen(Screen):
    def onClickDeleteWord(self):
        groups_dict = my_dict["groups"]
        fsg.delete_word_graphic(my_dict, groups_dict[labelText], word)
        sm.add_widget(HomeScreen())
        sm.transition.direction = "right"
        sm.current = "Home"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


class AddWord(Screen):
    def on_pre_enter(self):
        awc = AddWordContents()
        awc.on_pre_enter()


class AddWordContents(BoxLayout):
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
            WordInformation.showTags = False
            sm.add_widget(WordConfirmation())
            sm.transition.direction = "left"
            sm.current = "WordConfirmation"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])
        else:
            sm.add_widget(HomeScreen())
            sm.transition.direction = "left"
            sm.current = "Home"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])


class WordConfirmationContents(BoxLayout):
    def on_pre_enter(self):
        lfg = LabelFlashcardGroup()
        lfg.on_pre_enter()


class WordInformation(BoxLayout):
    showTags = True
    def on_pre_enter(self):
        self.clear_widgets()
        self.__init__()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global word
        word = word_data.english
        global wordInformationFound
        if word_data.english != None and word_data.word != None and word_data.reading != None and word_data.part_of_speech != None and word_data.meaning != None:
            wordInformationFound = True
            layout0 = BoxLayout(orientation='vertical', size_hint= (.8, .8), pos_hint={'center_x':0.5, 'center_y':0.5})
            l1 = Label(text = "English: " + word_data.english, color = (0, 0, 0, 1), size_hint= (1, .10), font_size='30dp')
            layout0.add_widget(l1)
            l2 = Label(text = "Japanese writing: " + word_data.word, font_name='mona', color = (0, 0, 0, 1), size_hint= (1, .10), font_size='30dp')
            layout0.add_widget(l2)
            l3 = Label(text = "Reading: " + word_data.reading, font_name='mona', color = (0, 0, 0, 1), size_hint= (1, .10), font_size='30dp')
            layout0.add_widget(l3)
            l4 = Label(text = "Part of speech: " + word_data.part_of_speech, color = (0, 0, 0, 1), size_hint= (1, .10), font_size='30dp')
            layout0.add_widget(l4)
            l5 = Label(text = "Meaning: " + word_data.meaning, color = (0, 0, 0, 1), size_hint= (1, .10), font_size='30dp')
            layout0.add_widget(l5)
            if WordInformation.showTags:
                layout1 = BoxLayout(orientation='horizontal', size_hint= (.5, .15), pos_hint={'center_x':0.5, 'center_y':0.5})
                tagIn = TextInput(multiline = False, font_name='mona', size_hint= (1, .3), pos_hint={'center_x':0, 'center_y':0.5})
                tagIn.bind(on_text_validate=lambda x:self.addTag(word_data, tagIn.text, tagIn))
                ll = Label(text = "Add a Tag: ", color = (.3, .3, .3, 3), size_hint= (.5, .3), pos_hint={'center_x':0.5, 'center_y':0.5})
                layout1.add_widget(ll)
                layout1.add_widget(tagIn)
                layout0.add_widget(layout1)
            self.add_widget(layout0)
        else:
            wordInformationFound = False
            l1 = Label(text="We had a problem looking for that word. Try again with another one", color = (0, 0, 0, 1))
            self.add_widget(l1)

    def addTag(self, jword, tag, box):
        box.text = ""
        if len(tag) > 23:
            box.text = "Tag was too long."
        fsg.tagWord(jword, tag, my_dict)



class WordConfirmationButtons(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global wordInformationFound
        if  wordInformationFound:
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
        textI = TextInput(multiline = False, size_hint= (.5, .25), font_name='mona')
        textI.bind(on_text_validate = self.createFromSize)
        space2 = Label(text = " ")
        layout2.add_widget(space1)
        layout2.add_widget(textI)
        layout2.add_widget(space2)
        self.add_widget(layout1)
        self.add_widget(layout2)

    def createFromSize(self, instance):
        size = instance.text
        if(size.isnumeric() and int(size) >= 1 ):
            self.create_group_and_return(my_dict, self.name, self.struc, int(size))
        else:
            if size == "":
                instance.text = "No name was given"
            else:
                instance.text = "Invalid Size"

    def searchvalidate(self, thisWidget, Widget):
        chosen = thisWidget.text.strip()
        if (chosen not in my_dict["groups"].keys() and chosen != ""):
            """self.clear_widgets()
            layout1 = BoxLayout(orientation='vertical')
            lbl1 = Label(text = "What kind of Data Structure should it be?", color = (0 , 0 , 0 , 1), size_hint = (1, .2))
            layout1.add_widget(lbl1)
            layout2 = BoxLayout(orientation='vertical')
            Arrbtn = Button(text = "Array")
            Arrbtn.bind(on_press = lambda x:self.create_group_and_return(my_dict, chosen, "A", 0))
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
            self.add_widget(layout1)"""
            self.create_group_and_return(my_dict, chosen, "A", 0)
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
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


class NewGroup(Screen):
    pass

class WordScreen(Screen):
    pass

class FlashcardScreen(Screen):
    pass

class WordConfirmation(Screen):
    pass

class WordNotAdded(Screen):
    pass


##########################################################
##########| Section pertaining group words end |##########


##########| Section pertaining recent words start |##########
#############################################################

class AllRecentWords(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        my_dict["recent"].traverse(self.setWords)
    
    def setWords(self, jw:JWord):
        WordInformation.showTags = True
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(50)), font_name='mona', font_size='30dp', background_normal="resources/bb1.png", background_down="resources/bb2.png")
        b.bind(on_press = lambda x: self.word_contents(jw))
        self.add_widget(b)
    
    def word_contents(self, jw:JWord):
        global word_data
        word_data = jw
        sm.add_widget(insideSomethingWordInformationScreen())
        sm.transition.direction = "left"
        sm.current = "insideView"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


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
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(50)), font_name='mona', font_size='30dp', background_normal="resources/bb1.png", background_down="resources/bb2.png")
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
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


class RecentWordsScreenContents(BoxLayout):
    def on_pre_enter(self):
        pass

###########################################################
##########| Section pertaining recent words end |##########


##########| Section pertaining search results start |##########
###############################################################

class AllSearchResults(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if SearchResultsScreen.found_word != None:
            jw = SearchResultsScreen.found_word
            b = Button(text = jw.word, background_color = (1,0,0,1), size_hint=(.5,None), size=(0,dp(50)), font_name='mona', font_size='30dp')
            b.bind(on_press = lambda x: self.word_contents(jw))
            self.add_widget(b)
            if my_dict["search_results"].getSize() != 0:
                my_dict["search_results"].traverse(self.setWords)
        elif my_dict["search_results"].getSize() == 0:
            lb = Label(text = "- Nothing -", color = (.4,.4,.4,1), size_hint=(1,None), size=(0,dp(40)), font_name='mona')
            self.add_widget(lb)
        else:
            my_dict["search_results"].traverse(self.setWords)
    
    def setWords(self, jw:JWord):
        WordInformation.showTags = True
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(50)), font_name='mona', font_size='30dp', background_normal="resources/bb1.png", background_down="resources/bb2.png")
        b.bind(on_press = lambda x: self.word_contents(jw))
        self.add_widget(b)
    
    def word_contents(self, jw:JWord):
        global word_data
        word_data = jw
        sm.add_widget(insideSomethingWordInformationScreen())
        sm.transition.direction = "left"
        sm.current = "insideView"
        backQueue.push(sm.children[1])
        sm.remove_widget(sm.children[1])


class insideSomethingWordInformationScreen(Screen):
    pass


class InsideSomethingScreenContents(BoxLayout):
    def on_pre_enter(self):
        fcgc = FlashCardGroupContents()
        fcgc.on_pre_enter()


#This one is found at home screen
class SearchResults(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        struc_size = str(fsg.getSizeOfGroup(my_dict["recent"]))
        b = Button(text="Recently added"+": "+struc_size, size_hint=(.5,None), size=(0,dp(40)), custom_label=i)
        b.bind(on_release = SearchResults.onClickButton)
        self.add_widget(b)

    def onClickButton(obj):
        SearchResultsScreen.setText("Search Results")


class SearchResultsScreen(Screen):
    found_word = None

    def on_pre_enter(self):
        print(self.children)
        self.clear_widgets()
        fgsc = SearchResultsScreenContents()
        self.add_widget(fgsc)

    def setWord(self, jw:JWord):
        b = Button(text = jw.word, size_hint=(.5,None), size=(0,dp(50)), font_name='mona', font_size='30dp', background_normal="resources/bb1.png", background_down="resources/bb2.png")
        self.add_widget(b)

    def addRecentWords(self):
        my_dict["recent"].traverse(self.setWord)

    @classmethod
    def setText(self, search_term):
        global labelText
        labelText = "persistent"
        if len(search_term) > 0 and ord(search_term[0]) < 123:
            SearchResultsScreen.found_word = fsg.tagSearch(my_dict, search_term)
        else:
            SearchResultsScreen.found_word = fsg.word_range_search(my_dict, search_term)
        if sm.current != "SearchResults":
            sm.add_widget(SearchResultsScreen())
            sm.transition.direction = "down"
            sm.transition.duration = .15
            sm.current = "SearchResults"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])
        else:
            sm.add_widget(HomeScreen())
            sm.transition.duration = 0
            sm.current = "Home"
            sm.remove_widget(sm.children[1])
            sm.add_widget(SearchResultsScreen())
            sm.transition.duration = .15
            sm.current = "SearchResults"
            backQueue.push(sm.children[1])
            sm.remove_widget(sm.children[1])


class SearchResultsScreenContents(BoxLayout):
    pass

############################################################
##########| Section pertaining search results end |#########

class TankaikiApp(App):
    path = fsg.getPath()

    def build(self):
        #loadResources()
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

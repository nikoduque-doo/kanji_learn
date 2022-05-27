from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

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

kv = Builder.load_file('Tankaiki.kv')


class TankaikiApp(App):
    def build(self):
        return kv

##def runApp():
TankaikiApp().run()


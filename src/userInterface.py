from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class FirstScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('Tankaiki.kv')


class TankaikiApp(App):
    def build(self):
        return kv

##def runApp():
TankaikiApp().run()


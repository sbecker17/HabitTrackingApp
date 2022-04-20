from kivy.app import App
from SpartanGrid import SpartanGrid
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import kivy 
kivy.require('1.0.6')
from kivy.uix.textinput import TextInput
from kivy.graphics import *
from functools import partial 
from kivy.properties import StringProperty


class LoginPage(GridLayout, Screen):

    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        self.cols=2
        self.padding=[50,50,50,50]

        self.login = TextInput(hint_text="Enter your username")
        self.add_widget(self.login)
        connect_button = Button(
            text="Login")
        connect_button.bind(on_press = self.homeScreen)
        self.add_widget(connect_button)

    def homeScreen(self,*args):
        self.db_name = self.login.text
        self.manager.current = 'homepage'

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class SpartanApp(App):
    def build(self):
        Window.clearcolor = (0.82, 0.9, 0.93, 1)
        self.sm = ScreenManagement(transition=NoTransition())
        self.sm.add_widget(LoginPage(name='login'))
        self.sm.add_widget(SpartanGrid(name='homepage', db=LoginPage().db_name))
        return self.sm
        # return LoginPage()


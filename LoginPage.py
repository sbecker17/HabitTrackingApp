import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from databaseops import *
from homepagebuttonfuncs import *
from kivy.clock import Clock
from SpartanGrid import SpartanGrid
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
kivy.require('1.0.6')

class LoginPage(GridLayout, Screen):
    def __init__(self, **kwargs):
    # def build(self):
        super(LoginPage, self).__init__()
        self.cols=2
        self.padding=[50,50,50,50]

        self.login = TextInput(hint_text="Enter your username")
        self.add_widget(self.login)
        connect_button = Button(
            text="Login")
        connect_button.bind(on_press = self.homeScreen)
        self.add_widget(connect_button)

    def homeScreen(self,*args):
        self.manager.current = 'homepage'

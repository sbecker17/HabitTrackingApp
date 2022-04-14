from kivy.app import App
from numpy import roots
# from LoginPage import LoginPage
import SpartanGrid
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import kivy 
from kivy.core.text import LabelBase
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.core.window import Window

class LoginPage(GridLayout, Screen):

    def __init__(self, **kwargs):
    # def build(self):
        super(LoginPage, self).__init__()
        self.cols=2
        self.padding=[50,50,50,50]

        login = TextInput(hint_text="Enter your username")
        self.add_widget(login)
        connect_button = Button(
            text="Login")
        connect_button.bind(on_press = self.homeScreen)
        self.add_widget(connect_button)

    def homeScreen(self,*args):
        self.manager.current = 'homepage'




class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

class SpartanApp(App):
    def build(self):
        Window.clearcolor = (0.82, 0.9, 0.93)
        sm = ScreenManagement(transition=NoTransition())
        sm.add_widget(LoginPage(name='login'))
        sm.add_widget(SpartanGrid.SpartanGrid(name='homepage'))
        return sm
        # return LoginPage()


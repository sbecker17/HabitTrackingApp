from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from databaseops import *
from homepagebuttonfuncs import *
from kivy.clock import Clock
from SpartanGrid import SpartanGrid

class LoginPage(GridLayout):

    def __init__(self, **kwargs):
    # def build(self):

        super(LoginPage, self).__init__()
        self.cols=2
        self.padding=[50,50,50,50]

        self.login = TextInput(hint_text="Enter your username")
        self.add_widget(self.login)
        connect_button = Button(
            text="Login",
            on_press=SpartanGrid(self.login.text)      #self.build_home_page
        )
        self.add_widget(connect_button)

    def build_home_page(self, instance):
        SpartanGrid.__init__
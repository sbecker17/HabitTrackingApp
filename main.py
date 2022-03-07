import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from SpartanApp import SpartanApp
from SpartanGrid import SpartanGrid

from databaseops import *

if __name__  == "__main__":
    # This line is where we would specify which database the user connects to based on their user information (maybe just a username?)
    # If a matching db already exists, it will connect to that one, if not it creates a new one.
    # create_habit_table(xconnection)
    SpartanApp().run()

    close_connection(SpartanGrid.connection)
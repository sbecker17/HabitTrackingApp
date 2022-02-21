import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty

import os

import sqlite3
from sqlite3 import Error

import os

# i can't figure out how to import all the functions at once -- elena
from databaseops import create_connection, insert_habit, close_connection, create_habit_table, get_all_habits, get_first_habit
from habit import Habit

class StartLayout(BoxLayout):
    t_name = ObjectProperty()
    t_category = ObjectProperty()
    t_count = ObjectProperty

    def open_popup(self):
        print("opening")


# class NewLayoutApp(App):
#     def build(self):
#         return StartLayout() 

class NewLayoutApp(App):
    pass


if __name__ == "__main__":
    # This line is where we would specify which database the user connects to based on their user information (maybe just a username?)
    # If a matching db already exists, it will connect to that one, if not it creates a new one.
    # TODO: figure out how to query the sqlite file.
    xconnection = create_connection("sarah.db")
    #print(xconnection)
    create_habit_table(xconnection)
    NewLayoutApp().run()
    close_connection(xconnection)
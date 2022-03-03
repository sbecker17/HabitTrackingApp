import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import sqlite3
from sqlite3 import Error

import os

#from databaseops import create_connection, insert_habit, close_connection, create_habit_table, get_all_habits, get_first_habit
from habit import Habit

class StartLayout(BoxLayout):
    t_name = ObjectProperty(None)
    t_category = ObjectProperty(None)
    
    def show_popup(self):
        show = P()

        popupWindow = Popup(title="Add Task", content=show, size_hint=(None, None), size=(400,400))

        popupWindow.open()


class P(FloatLayout):
    t_name = ObjectProperty(None)
    t_category = ObjectProperty(None)
    
    def close_popup(self):
        pass


class HabitTrackerApp(App):
    def build(self):
        return StartLayout()


if __name__ == "__main__":
    HabitTrackerApp().run()


# kv = Builder.load_file("habittracker.kv")

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
import kivy.properties as kyprops
from kivy.uix.scrollview import ScrollView
from datetime import date
import weakref
from kivy.clock import Clock
#from kivymd.app import MDApp
#from kivy.properties import ObjectProperty

import os

import sqlite3
from sqlite3 import Error

import os

# i can't figure out how to import all the functions at once -- elena
from databaseops import create_connection, insert_habit, close_connection, create_habit_table, get_all_habits, get_first_habit
from habit import Habit

class StartLayout(BoxLayout):
    # t_name = kyprops.ObjectProperty(None)
    # t_category = kyprops.ObjectProperty(None)
    # t_count = kyprops.ObjectProperty(None)
    def __init__(self,**kwargs):
        super(StartLayout, self).__init__(**kwargs)
        # super(StartLayout, self).__getattr__()
        self.i=0
        self.habList = []
        print(get_all_habits(xconnection, "sarah"))
        for hab in get_all_habits(xconnection, "sarah"):
            self.habList.append(Habit(hab[0], hab[1], hab[2], hab[3], hab[4]))
            # button = Button(text = hab[2])
            # self.ids.grid.add_widget(button)
            self.i = self.i + 1
        self.j = self.i
        for self.j in range(20):
            self.habList.append(Habit("sarah", self.j, "", 0, date.today()))
            self.j = self.j + 1
            # button1 = Button(text = self.habList[self.i].name)
            # self.ids.grid.add_widget(button1)
    #     Clock.schedule_once(self._finish_init)
    #     # print(self.habList)
    # def _finish_init(self, dt):
    #     self.grid = self.ids.grid
    # print(habList[i].start_date)

    def open_popup(self):
        print("opening")
        print(self.ids.name_box.text)
        self.ids.name_box.text = ""

    def open_task(self):
        self.habList[self.i].name = self.ids.name_box.text
        print(self.i)
        print(self.habList)
        # print(self.habList[self.i])
        insert_habit(self.habList[self.i], xconnection)
        self.ids.name_box.text = ""
        self.add_task_group()
        self.i = self.i + 1
        # taskL = Label(text=self.habList[self.i].name)
        # self.ids.add_widget(taskL)
        # self.ids['task'+str(self.i)] = weakref.ref(taskL)

    def add_task_group(self):
        # print(self.ids)
        taskL = Label(text=self.habList[self.i].name)
        self.add_widget(taskL)
        # self.ids.add_widget(Label(text = self.habList[self.i].name))



# class NewLayoutApp(App):
#     def build(self):
#         Builder.load_file("/newlayout.kv")
#         return StartLayout() 

class NewLayoutApp(App):
    def build(self):
        return StartLayout()


if __name__ == "__main__":
    # This line is where we would specify which database the user connects to based on their user information (maybe just a username?)
    # If a matching db already exists, it will connect to that one, if not it creates a new one.
    # TODO: figure out how to query the sqlite file.
    xconnection = create_connection("sarah.db")
    # print(xconnection)
    create_habit_table(xconnection)
    NewLayoutApp().run()
    #close_connection(xconnection)
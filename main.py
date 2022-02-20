import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import os

import sqlite3
from sqlite3 import Error

import os

# i can't figure out how to import all the functions at once -- elena
from databaseops import create_connection, insert_habit, close_connection, create_habit_table, get_all_habits
from habit import Habit

class SpartanGrid(GridLayout):

    def __init__(self,**kwargs):
        super(SpartanGrid, self).__init__()
        self.cols = 2
        self.add_widget(Label(text="Student Name:"))

        self.s_name = TextInput(multiline=False)
        self.add_widget(self.s_name)

        self.add_widget(Label(text="Student Marks:"))
        self.s_marks = TextInput()
        self.add_widget(self.s_marks)

        self.add_widget(Label(text="Student Gender"))
        self.s_gender = TextInput()
        self.add_widget(self.s_gender)

        self.press = Button(text="Click me")
        self.press.bind(on_press=self.click_me)
        self.add_widget(self.press)

        self.press = Button(text="Add Task")
        self.press.bind(on_press=self.show_popup)
        self.add_widget(self.press)
        
    def click_me(self, instance):
        print("Name of student is "+self.s_name.text)
        print("Marks of student are "+self.s_marks.text)
        print("Gender of student is "+self.s_gender.text)
        h1 = Habit(self.s_name.text, self.s_marks.text)
        print(h1.category)
        self.add_widget(Label(text=h1.category))
        self.s_gender = TextInput()
        self.add_widget(self.s_gender)


    def show_popup(self, obj):
        playout = GridLayout(cols = 1)
        plabel = Label(text = "add task")
        ptext = TextInput()
        pbutton = Button(text = "Close", on_press = self.close_popup)
        pbutton_add = Button(text = "Add", on_press = self.add_task)
        playout.add_widget(plabel)
        playout.add_widget(ptext)
        playout.add_widget(pbutton)
        playout.add_widget(pbutton_add)
        self.popup = Popup(title = "Test popup", content = playout)
        self.popup.open()

    def close_popup(self, obj):
        self.popup.dismiss()

    def add_task(self, obj):
        h2 = Habit(self.ids.popup.ptext, "")
        self.add_widget(Label(text=h2.category))
        self.p_task = Label()
        self.add_widget(self.popup.ptext)



class SpartanApp(App):

    def build(self):
        return SpartanGrid()

if __name__ == "__main__":
    # This line is where we would specify which database the user connects to based on their user information (maybe just a username?)
    # If a matching db already exists, it will connect to that one, if not it creates a new one.
    # TODO: figure out how to query the sqlite file.
    xconnection = create_connection("sarah.db")
    # create_habit_table(xconnection)
    SpartanApp().run()
    close_connection(xconnection)
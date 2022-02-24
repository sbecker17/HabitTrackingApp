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
#####from HabitTrackingApp.HabitTrackingApp.databaseops import update_count

# i can't figure out how to import all the functions at once -- elena
from databaseops import create_connection, insert_habit, close_connection, create_habit_table, get_all_habits, get_first_habit, update_count
from habit import Habit

class SpartanGrid(GridLayout):

    def __init__(self,**kwargs):
        super(SpartanGrid, self).__init__()
        self.cols = 2

        self.add_widget(Label(text="Task Name:"))
        self.t_name = TextInput(multiline=False)
        self.add_widget(self.t_name)

        self.add_widget(Label(text="Task Category:"))
        self.t_cat = TextInput(text = "category")
        self.add_widget(self.t_cat)

        self.add_widget(Label(text="Task Count"))
        self.t_count = TextInput(text = "0")
        self.add_widget(self.t_count)

        self.press = Button(text="Click me")
        self.press.bind(on_press=self.click_me)
        self.add_widget(self.press)

        self.press = Button(text="Add Task")
        self.press.bind(on_press=self.show_popup)
        self.add_widget(self.press)

    # def count_up(self, label):
    #     self.habit1cnt.text = str(int(self.habit1cnt.text)+1)
    #     #self.habit1cnt.text = str(habit.count)
    #     print(self.habit1cnt.text)
        
    # def click_me(self, instance):
    #     #print("Name of student is "+self.t_name.text)
    #     #print("Marks of student are "+self.t_cat.text)
    #     #print("Gender of student is "+self.t_count.text)
    #     h1 = Habit(self.t_name.text, self.t_cat.text, 0)
    #     insert_habit(h1, xconnection)
    #     get_first_habit(xconnection)
    #     #print(self.h1.category, self.h1.count)
    #     self.habit1cnt = Label(text = "0")
    #     self.habit1 = Button(text = h1.category, on_press = self.count_up)
    #     print(self.habit1cnt.text)
    #     self.add_widget(self.habit1)
    #     self.add_widget(self.habit1cnt)

    def count_up(self, label):
        self.habit1cnt.text = str(int(self.habit1cnt.text)+1)
        update_count(self.habit1cnt.text, self.habit1.text, xconnection)

    def count_down(self, label):
        self.habit1cnt.text = "0"
        update_count(self.habit1cnt.text, self.habit1.text, xconnection)
        
    def click_me(self, instance):
        #print("Name of student is "+self.t_name.text)
        #print("Marks of student are "+self.t_cat.text)
        #print("Gender of student is "+self.t_count.text)
        h1 = Habit(self.t_name.text, self.t_cat.text, 0)
        insert_habit(h1, xconnection)
        get_first_habit(xconnection)
        #print(self.h1.category, self.h1.count)
        self.habit1cnt = Label(text = "0")
        self.habit1 = Label(text = h1.category, bold = True)
        self.didIt = Button(text = "Did it!", on_press = self.count_up, background_color = [169/255,255/255,221/255,1])
        self.didnt = Button(text = "Not today", on_press = self.count_down, background_color = [253/255, 129/255, 129/255, 1])
        #print(self.habit1cnt.text)
        self.add_widget(self.habit1)
        self.add_widget(self.habit1cnt)
        self.add_widget(self.didIt)
        self.add_widget(self.didnt)



        # self.habit1 = Label(text=h1.category)
        # self.add_widget(self.habit1)
        # #self.s_task = TextInput()
        # self.habit1cnt = Button(text=str(h1.count))
        # self.habit1cnt.bind(on_press=self.count_up(h1))
        # self.add_widget(self.habit1cnt)



    def show_popup(self, obj):
        playout = GridLayout(cols = 1)
        self.popup = Popup(title = "Test popup", content = playout)
        self.popup.plabel = Label(text = "add task")
        self.popup.ptext = TextInput()
        self.popup.pbutton = Button(text = "Cancel", on_press = self.close_popup)
        self.popup.pbutton_add = Button(text = "Add", on_press = self.add_task)
        playout.add_widget(self.popup.plabel)
        playout.add_widget(self.popup.ptext)
        playout.add_widget(self.popup.pbutton)
        playout.add_widget(self.popup.pbutton_add)
        #self.popup = Popup(title = "Test popup", content = playout)
        self.popup.open()

    def close_popup(self, obj):
        self.popup.dismiss()

    def add_task(self, obj):
        h2 = Habit(self.popup.ptext.text, "name", 0)
        print(h2.category)
        insert_habit(h2, xconnection)
        get_first_habit(xconnection)



class SpartanApp(App):

    def build(self):
        return SpartanGrid()

if __name__ == "__main__":
    # This line is where we would specify which database the user connects to based on their user information (maybe just a username?)
    # If a matching db already exists, it will connect to that one, if not it creates a new one.
    # TODO: figure out how to query the sqlite file.
    xconnection = create_connection("sarah.db")
    #print(xconnection)
    create_habit_table(xconnection)
    SpartanApp().run()
    close_connection(xconnection)
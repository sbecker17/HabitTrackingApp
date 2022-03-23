from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import date
from habit import Habit
from databaseops import *
import sys
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout

class SpartanGrid(StackLayout):

    def __init__(self, **kwargs):
        # self.orientation = "vertical"
        db_name = "elena.db"
        self.connection = create_connection(db_name)
        create_habit_table(self.connection)

        super(SpartanGrid, self).__init__()
        # self.cols = 1

        self.add_widget(Label(text="Task Name:"))
        # self.t_name = TextInput(multiline=False)
        # self.add_widget(self.t_name)

        # self.add_widget(Label(text="Task Category:"))
        # self.t_cat = TextInput(text = "category")
        # self.add_widget(self.t_cat)

        # self.press = Button(text="Click me")
        # self.press.bind(on_press=lambda x:self.click_me(xconnection = self.connection, db_name = db_name))
        # self.add_widget(self.press)

        # self.press = Button(text="Add Task")
        # self.press.bind(on_press=self.show_popup)
        # self.add_widget(self.press)

        # allHabits = get_all_habits(self.connection, 'elena')
        
        # for i in allHabits:
            
        #     h1 = Habit(i[0],i[1],i[2],i[3],i[4])
            
        #     self.habit1cnt = Label(text = str(h1.count))
        #     self.habit1 = Label(text = h1.name, bold = True)
        #     self.didIt = Button(text = "Did it!", on_press=lambda y:self.count_up(xconnection = self.connection, hab=h1), background_color = [169/255,255/255,221/255,1])
        #     self.didnt = Button(text = "Not today",  background_color = [253/255, 129/255, 129/255, 1])

        #     self.add_widget(self.habit1)
        #     self.add_widget(self.habit1cnt)
        #     self.add_widget(self.didIt)
        #     self.add_widget(self.didnt)

    def count_up(self, xconnection, hab):
        self.habit1cnt.text = str(int(hab.count)+1)
        update_count(self.habit1cnt.text, hab.name, xconnection)

    def count_down(self, xconnection, label):
        self.habit1cnt.text = str(int(self.habit1cnt.text))
        update_count(self.habit1cnt.text, self.habit1.text, xconnection)
        
    def click_me(self, xconnection, db_name):
        h1 = Habit(db_name[:-3], self.t_cat.text, self.t_name.text, 0, date.today())
        insert_habit(h1, xconnection)
        get_first_habit(xconnection)
        self.habit1cnt = Label(text = "0")
        self.habit1 = Label(text = h1.name, bold = True)
        self.didIt = Button(text = "Did it!", on_press = self.count_up, background_color = [169/255,255/255,221/255,1])
        self.didnt = Button(text = "Not today", on_press = self.count_down, background_color = [253/255, 129/255, 129/255, 1])
        self.add_widget(self.habit1)
        self.add_widget(self.habit1cnt)
        self.add_widget(self.didIt)
        self.add_widget(self.didnt)

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

    def add_task(self, xconnection, obj):
        h2 = Habit(self.popup.ptext.text, "name", 0)
        print(h2.category)
        insert_habit(h2, xconnection)
        get_first_habit(xconnection)


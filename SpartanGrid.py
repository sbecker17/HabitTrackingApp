from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import date
from habit import Habit
from databaseops import *
from functools import partial 
from kivy.clock import Clock
import sys


class SpartanGrid(GridLayout):

    def __init__(self, **kwargs):
        self.db_name = "elena.db"
        self.connection = create_connection(self.db_name)
        create_habit_table(self.connection)

        super(SpartanGrid, self).__init__()
        self.cols=1
        self.padding=[50,50,50,50]

        # header = Label(
        #     text="[u][b][size=100][color=346eeb]Habit Tracker[/color][/size][/b][/u]", 
        #     markup=True)
        
        header = Button(
            text="Habit Tracker", 
            font_size="35sp", 
            disabled=True, 
            background_disabled_normal='background_normal', 
            background_color=[52/255, 110/255, 235/255, 0.5])

        self.add_widget(header)
        
        self.homepage=GridLayout(cols=2)

        # self.homepage.add_widget(Label(text="Task Name:"))
        # self.homepage.t_name = TextInput(hint_text="name")
        # self.homepage.add_widget(self.homepage.t_name)

        # self.homepage.add_widget(Label(text="Task Category:"))
        # self.homepage.t_cat = TextInput(hint_text = "category")
        # self.homepage.add_widget(self.homepage.t_cat)

        # self.homepage.press = Button(text="Click me")
        # self.homepage.press.bind(on_press=lambda x:self.click_me_new(xconnection = self.connection, db_name = self.db_name))
        # self.homepage.add_widget(self.homepage.press)

        self.homepage.press = Button(text="Add Task")
        self.homepage.press.bind(on_press=self.show_popup)
        self.homepage.add_widget(self.homepage.press)

        self.homepage.press = Button(text="View __")
        self.homepage.press.bind(on_press=self.show_popup)
        self.homepage.add_widget(self.homepage.press)

        self.add_widget(self.homepage)


        allHabits = get_all_habits(self.connection, 'elena')

        self.tasklayouts = []
        self.habit_name_labels = []
        self.habit_count_labels = []
        self.check_yes_buttons = []
        self.check_no_buttons = []
        self.i=0
        for i in range(len(allHabits)):
            
            if (i%2==0):
                self.habit_name_labels.append(Button(
                    text=str(allHabits[i][2]),  
                    # disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5], #))
                    on_press = partial(self.delete_task_popup, i)))
                
                self.habit_count_labels.append(Button(
                    text=str(allHabits[i][3]),  
                    disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5]))

            else:
                self.habit_name_labels.append(Button(
                    text=str(allHabits[i][2]),  
                    # disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 1],#))
                    on_press = partial(self.delete_task_popup, i)))
                
                self.habit_count_labels.append(Button(
                    text=str(allHabits[i][3]),  
                    disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 1]))
        
 
            self.check_yes_buttons.append(Button(text = "Did it!", on_press = partial(self.count_up_new, self.connection, i), background_color = [169/255,255/255,221/255,1]))
            self.check_no_buttons.append(Button(text = "Didn't", on_press = partial(self.count_down_new, self.connection, i), background_color = [253/255, 129/255, 129/255, 1]))
            

            self.task=GridLayout(rows=1, cols_minimum={0:200, 1:200})
            self.task.add_widget(self.habit_name_labels[i])
            self.task.add_widget(self.habit_count_labels[i])
            self.task.add_widget(self.check_yes_buttons[i])
            self.task.add_widget(self.check_no_buttons[i])

            self.tasklayouts.append(self.task)
            # print(self.tasklayouts)
            self.add_widget(self.task)

            self.i = self.i+1
        
                        

    # def count_up(self, xconnection, hab):
    #     print(self.habit1.text)
    #     print(str(hab.name))
    #     if (self.habit1.text == str(hab.name)):
    #         self.habit1cnt.text = str(int(hab.count)+1)
    #         hab.count = hab.count+1
    #         update_count(self.habit1cnt.text, hab.name, xconnection)
    #     else:
    #         pass

    def count_up_new(self, xconnection, ind, instance):
        name = self.habit_name_labels[ind].text
        self.habit_count_labels[ind].text = str(int(self.habit_count_labels[ind].text) + 1)
        update_count(self.habit_count_labels[ind].text, name, xconnection)
        pass

    # def count_down(self, xconnection, hab):
    #     if (self.habit1.text == str(hab.name)):
    #         self.habit1cnt.text = "0"
    #         hab.count = 0
    #         #self.habit1cnt.text = str(int(self.habit1cnt.text))
    #         update_count(0, self.habit1.text, xconnection)
    #     else: 
    #         pass

    def count_down_new(self, xconnection, ind, instance):
        name = self.habit_name_labels[ind].text
        self.habit_count_labels[ind].text = str(0)
        update_count(0, name, xconnection)
        pass
        
    # def click_me(self, xconnection, db_name):
    #     h1 = Habit(db_name[:-3], self.t_cat.text, self.t_name.text, 0, date.today())
    #     insert_habit(h1, xconnection)
    #     get_first_habit(xconnection)
    #     self.habit1cnt = Label(text = "0")
    #     self.habit1 = Label(text = h1.name, bold = True)
    #     self.didIt = Button(text = "Did it!", on_press = lambda x:self.count_up(xconnection = self.connection, hab = h1), background_color = [169/255,255/255,221/255,1])
    #     self.didnt = Button(text = "Not today", on_press = lambda y: self.count_down(xconnection=self.connection, hab=h1), background_color = [253/255, 129/255, 129/255, 1])
    #     self.add_widget(self.habit1)
    #     self.add_widget(self.habit1cnt)
    #     self.add_widget(self.didIt)
    #     self.add_widget(self.didnt)

    # def click_me_new(self, xconnection, db_name):
    #     h1 = Habit(db_name[:-3], self.homepage.t_cat.text, self.homepage.t_name.text, 0, date.today())
    #     insert_habit(h1, xconnection)
    #     allHabits = get_all_habits(self.connection, db_name[:-3])
    #     # print(allHabits)
    #     self.habit_count_labels[self.i].text = str(allHabits[self.i][3])
    #     self.habit_name_labels[self.i].text = str(allHabits[self.i][2])
    #     self.habit_count_labels[self.i] = Label(text = str(allHabits[self.i][3]))
    #     self.check_yes_buttons.append(Button(text = "Did it!", on_press = partial(self.count_up_new, self.connection, self.i), background_color = [169/255,255/255,221/255,1]))
    #     self.check_no_buttons.append(Button(text = "Didn't", on_press = partial(self.count_down_new, self.connection, self.i), background_color = [253/255, 129/255, 129/255, 1]))
    #     self.add_widget(self.habit_name_labels[self.i])
    #     self.add_widget(self.habit_count_labels[self.i])
    #     self.add_widget(self.check_yes_buttons[self.i])
    #     self.add_widget(self.check_no_buttons[self.i])
    #     self.i = self.i+1 
    #     pass

    def show_popup(self, obj):
        playout = GridLayout(cols = 2, padding=[200, 200, 200, 200], rows_minimum={0:200})
        self.popup = Popup(title = "Add Task", content = playout)
        self.popup.plabel = Button(
                    text="Add Task",  
                    disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5])
        self.popup.ptext = TextInput()
        self.popup.pbutton = Button(text = "Cancel", on_press = self.close_popup)
        # self.popup.pbutton_add = Button(text = "Add", on_press = lambda y:self.add_task(xconnection=self.connection))
        self.popup.pbutton_add = Button(text = "Add", on_press = partial(self.add_task_new, self.connection))
        playout.add_widget(self.popup.plabel)
        playout.add_widget(self.popup.ptext)
        playout.add_widget(self.popup.pbutton)
        playout.add_widget(self.popup.pbutton_add)
        self.popup.open()

    def close_popup(self, obj):
        self.popup.dismiss()

    # def add_task(self, xconnection):
    #     h2 = Habit("elena","cat", self.popup.ptext.text, 0, date.today())
    #     print(h2.name)
    #     insert_habit(h2, xconnection)
    #     get_first_habit(xconnection)
    #     self.popup.dismiss()

    def add_task_new(self, xconnection, instance):
        h2 = Habit(self.db_name[:-3],"cat", self.popup.ptext.text, 0, date.today())
        insert_habit(h2, xconnection)
        allHabits = get_all_habits(self.connection, self.db_name[:-3])
        self.popup.dismiss()

        self.habit_name_labels.append(Button(
                text=str(allHabits[self.i][2]),  
                # disabled=True, 
                background_disabled_normal='background_normal',
                on_press = partial(self.delete_task_popup, self.i)))

        self.habit_count_labels.append(Button(
                text=str(allHabits[self.i][3]),  
                disabled=True, 
                background_disabled_normal='background_normal'))

        if (self.i%2==0):
            self.habit_name_labels[self.i].background_color = [52/255, 110/255, 235/255, 0.5]
            self.habit_count_labels[self.i].background_color = [52/255, 110/255, 235/255, 0.5]
        else:
            self.habit_name_labels[self.i].background_color = [52/255, 110/255, 235/255, 1]
            self.habit_count_labels[self.i].background_color = [52/255, 110/255, 235/255, 1]


        self.check_yes_buttons.append(Button(text = "Did it!", on_press = partial(self.count_up_new, self.connection, self.i), background_color = [169/255,255/255,221/255,1]))
        self.check_no_buttons.append(Button(text = "Didn't", on_press = partial(self.count_down_new, self.connection, self.i), background_color = [253/255, 129/255, 129/255, 1]))


        self.new_task = GridLayout(rows=1, cols_minimum={0:200, 1:200})
        self.new_task.add_widget(self.habit_name_labels[self.i])
        self.new_task.add_widget(self.habit_count_labels[self.i])
        
        #self.yn_buttons = GridLayout(cols=1)
        #self.yn_buttons.add_widget(self.check_yes_buttons[self.i])
        #self.yn_buttons.add_widget(self.check_no_buttons[self.i])
        #self.new_task.add_widget(self.yn_buttons)


        self.new_task.add_widget(self.check_yes_buttons[self.i])
        self.new_task.add_widget(self.check_no_buttons[self.i])
        self.tasklayouts.append(self.new_task)
        self.add_widget(self.new_task)
        self.i = self.i+1 
        pass

    def delete_task(self, i, connection, instance):
        delete_task_db(self.habit_name_labels[i].text, connection)
        # return SpartanGrid()
        # self.remove_widget(self.new_task[i])
        self.remove_widget(self.habit_name_labels[i])
        self.remove_widget(self.habit_count_labels[i])
        self.remove_widget(self.check_yes_buttons[i])
        self.remove_widget(self.check_no_buttons[i])
        self.remove_widget(self.tasklayouts[i])
        self.i = self.i - 1
        self.close_popup_delete(i)
        pass

    def show_limit_popup(self):
        playout3 = GridLayout(cols = 1)
        self.popup_limit = Popup(title = "You've reached the limit", content = playout3)
        self.popup_limit.plabel = Label(text = "You have reached the limit of tasks you can add.")
        self.popup_limit.pcount = Label(text = "You currently have " + str(self.i) + " tasks.")
        self.popup_limit.pbutton = Button(text = "Cancel", on_press = self.close_popup_limit)
        # self.popup.pbutton_add = Button(text = "Add", on_press = partial(self.add_task_new, self.connection))
        playout3.add_widget(self.popup_limit.plabel)
        playout3.add_widget(self.popup_limit.pcount)
        playout3.add_widget(self.popup_limit.pbutton)
        # playout.add_widget(self.popup.pbutton_add)
        #self.popup = Popup(title = "Test popup", contentdel = playout)
        print(self.i)
        self.popup_limit.open()

    def close_popup_limit(self, obj):
        self.popup_limit.dismiss()

    def delete_task_popup(self, i, obj):
        playout2 = GridLayout(cols=1)
        self.popup_delete = Popup(title="Edit a task", content = playout2)
        # self.popup_delete.plabel = Label(text = "Remove each task you no longer want")
        self.popup_delete.pholder =  Button(text = "Close", on_press = self.close_popup_delete)
        # playout2.add_widget(self.popup_delete.plabel)
        playout2.add_widget(Button(text="Delete Task: " + self.habit_name_labels[i].text, on_press = partial(self.delete_task, i, self.connection))) #, on_release = Clock.schedule_once(self.close_popup_delete, 3)))
        playout2.add_widget(Button(text= "Edit task name", on_press = partial(self.edit_task_popup, i)))
        # for i in range(len(self.habit_name_labels)):
        #     if (self.habit_name_labels[i].text == ""):
        #         pass
        #     else:
        #         self.hab_del_btns[i] = Button(text="Delete " + self.habit_name_labels[i].text, on_press = partial(self.delete_task, i, self.connection), on_release = Clock.schedule_once(self.close_popup_delete, 3))
        #         playout2.add_widget(self.hab_del_btns[i])
        playout2.add_widget(self.popup_delete.pholder)
        self.popup_delete.open()


    def close_popup_delete(self, obj):
        Clock.schedule_once(self.popup_delete.dismiss, 2)
        # self.popup_delete.dismiss()

    def edit_task_popup(self, i, obj):
        playout4 = GridLayout(cols=1)
        self.popup_edit = Popup(title="Edit a task", content = playout4)
        playout4.add_widget(Label(text="Old task name: " + str(self.habit_name_labels[i].text) + "\n New task name:"))
        self.popup_edit.ptext = TextInput(hint_text= "New task name")
        self.popup_edit.pcloser =  Button(text = "Close", on_press = self.close_popup_edit)
        playout4.add_widget(self.popup_edit.ptext)
        playout4.add_widget(Button(text="Submit name", on_press = partial(self.update_task_name, i)))
        playout4.add_widget(self.popup_edit.pcloser)
        self.popup_edit.open()

    def close_popup_edit(self, obj):
        self.popup_delete.dismiss()
        Clock.schedule_once(self.popup_edit.dismiss, 2)


    def update_task_name(self, i, obj):
        update_name(self.popup_edit.ptext.text, self.habit_name_labels[i].text, self.connection)
        self.habit_name_labels[i].text = self.popup_edit.ptext.text
        self.close_popup_edit(obj)

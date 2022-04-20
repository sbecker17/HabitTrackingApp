from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import date
from datetime import datetime
from datetime import timedelta
from habit import Habit
from databaseops import *
from homepagebuttonfuncs import *
from functools import partial 
from kivy.clock import Clock

import kivy
kivy.require('1.0.6')

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty

class SpartanGrid(GridLayout, Screen):

    def __init__(self, db, **kwargs):    #, **kwargs

        super(SpartanGrid, self).__init__(**kwargs)
        print(db)

        self.cols=1
        self.padding=[50,50,50,50]

        # login = TextInput(hint_text="Enter your username")
        # self.add_widget(login)
        # connect_button = Button(
        #     text="Login",
        #     on_press = lambda y:super(SpartanGrid, self).__init__()
        # )
        # self.add_widget(connect_button)

        self.db_name = "elena.db"
        self.connection = create_connection(self.db_name)
        create_habit_table(self.connection)

       
        header = Button(
            text="Habit Tracker", 
            font_size="35sp", 
            disabled=True, 
            background_disabled_normal='background_normal', 
            background_color=[52/255, 110/255, 235/255, 0.5])

        self.add_widget(header)
        
        self.homepage=GridLayout(cols=2)

        self.homepage.press = Button(text="Add Task")
        self.homepage.press.bind(on_press=self.show_popup)
        self.homepage.add_widget(self.homepage.press)

        self.homepage.press = Button(text="View __")
        self.homepage.press.bind(on_press=self.show_quitting_popup)
        self.homepage.add_widget(self.homepage.press)

        self.add_widget(self.homepage)

        allHabits = get_all_habits(self.connection, self.db_name[:-3], 'continue')

        self.tasklayouts = []
        self.habit_name_labels = []
        self.habit_count_labels = []
        self.check_yes_buttons = []
        self.check_no_buttons = []
        self.i=0
        self.quit_i=0
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

    def count_up_new(self, xconnection, ind, instance):
        name = self.habit_name_labels[ind].text
        habit_list = get_habit_by_name(xconnection, name)
        last_mod_date = habit_list[0][5]
        category = habit_list[0][2]
        today = str(date.today())

        if (last_mod_date == today):
            self.habit_name_labels[ind].text = self.habit_name_labels[ind].text + ": Already done!"
        else:
            self.habit_count_labels[ind].text = str(int(self.habit_count_labels[ind].text) + 1)
            update_count(self.habit_count_labels[ind].text, name, category, xconnection)
            update_last_mod_date(name, xconnection)
        pass

    def count_down_new(self, xconnection, ind, instance):
        name = self.habit_name_labels[ind].text
        self.habit_count_labels[ind].text = str(0)
        update_count(0, name, 'continue', xconnection)
        pass

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

    def add_task_new(self, xconnection, instance):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        h2 = Habit(self.db_name[:-3],"continue", self.popup.ptext.text, 0, today, yesterday, 0)
        insert_habit(h2, xconnection)
        allHabits = get_all_habits(self.connection, self.db_name[:-3], 'continue')
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
            h3 = Habit("elena", "quit", str(self.i-1), 0, today, today, 0)
            insert_habit(h3, xconnection)
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
        del self.habit_name_labels[i]
        self.remove_widget(self.habit_count_labels[i])
        del self.habit_count_labels[i]
        self.remove_widget(self.check_yes_buttons[i])
        del self.check_yes_buttons[i]
        self.remove_widget(self.check_no_buttons[i])
        del self.check_no_buttons[i]
        self.remove_widget(self.tasklayouts[i])
        del self.tasklayouts[i]
        print(self.i)
        self.i = self.i - 1
        print(self.i)
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
        playout2.add_widget(Label(text="Edit Task Name: "))
        self.popup_delete.pname = TextInput(text = self.habit_name_labels[i].text)
        playout2.add_widget(self.popup_delete.pname)
        playout2.add_widget(Button(text="Submit name", on_press = partial(self.update_task_name, i)))
        playout2.add_widget(Button(text="Delete Task: " + self.habit_name_labels[i].text, background_color = [253/255, 129/255, 129/255, 1], on_press = partial(self.delete_task, i, self.connection))) #, on_release = Clock.schedule_once(self.close_popup_delete, 3)))
        # playout2.add_widget(Button(text= "Edit task name", on_press = partial(self.edit_task_popup, i)))
        # for i in range(len(self.habit_name_labels)):
        #     if (self.habit_name_labels[i].text == ""):
        #         pass
        #     else:
        #         self.hab_del_btns[i] = Button(text="Delete " + self.habit_name_labels[i].text, on_press = partial(self.delete_task, i, self.connection), on_release = Clock.schedule_once(self.close_popup_delete, 3))
        #         playout2.add_widget(self.hab_del_btns[i])
        playout2.add_widget(self.popup_delete.pholder)
        self.popup_delete.open()


    def close_popup_delete(self, obj):
        self.loading_close_popup(obj)
        # comment out above line to remove loading screen :)
        Clock.schedule_once(self.popup_delete.dismiss, 2)
        # self.popup_delete.dismiss()

    def loading_close_popup(self, obj):
        playout4 = FloatLayout()
        self.popup_lc = Popup(title="Loading", content = playout4)
        self.popup_lc.pcloser =  Button(text = "Loading...", disabled=True, background_disabled_normal='background_normal', background_color=[52/255, 110/255, 235/255, 0.5])
        playout4.add_widget(self.popup_lc.pcloser)
        Clock.schedule_once(self.popup_lc.dismiss, 2)
        self.popup_lc.open()
        # Clock.schedule_once(self.popup_lc.dismiss, 2)

    #     playout4 = GridLayout(cols=1)
    #     self.popup_lc = Popup(title="Edit a task", content = playout4)
    #     playout4.add_widget(Label(text="Old task name: " + str(self.habit_name_labels[i].text) + "\n New task name:"))
    #     self.popup_lc.ptext = TextInput(hint_text= "New task name")
    #     self.popup_lc.pcloser =  Button(text = "Close", on_press = self.close_popup_edit)
    #     playout4.add_widget(self.popup_lc.ptext)
    #     playout4.add_widget(Button(text="Submit name", on_press = partial(self.update_task_name, i)))
    #     playout4.add_widget(self.popup_lc.pcloser)
    #     self.popup_lc.open()

    # def close_popup_edit(self, obj):
    #     self.popup_delete.dismiss()
    #     Clock.schedule_once(self.popup_lc.dismiss, 2)


    def update_task_name(self, i, obj):
        update_name(self.popup_delete.pname.text, self.habit_name_labels[i].text, self.connection)
        self.habit_name_labels[i].text = self.popup_delete.pname.text
        self.close_popup_delete(obj)


# ------------------------------------------------------------------------------------------------
# ---------------------------- Quitting is a lot of ~work~ ---------------------------------------
# ------------------------------------------------------------------------------------------------

    def show_quitting_popup(self, obj):
        # return self
        self.quitlayout = GridLayout(cols=2)
        self.quithomepage = Popup(title="Quit tasks", content = self.quitlayout)
        self.quithomepage.addbtn = Button(text="Quit New Task")
        self.quithomepage.addbtn.bind(on_press=self.add_quit_popup)
        self.quitlayout.add_widget(self.quithomepage.addbtn)

        self.quithomepage.press = Button(text="Go Back")
        self.quithomepage.press.bind(on_press=self.quithomepage.dismiss)
        self.quitlayout.add_widget(self.quithomepage.press)

        # quitlayout.add_widget(self.quithomepage)

        quit_allHabits = get_all_habits(self.connection, 'elena', 'quit')

        self.quit_habit_name_labels = []
        self.quit_habit_count_labels = []
        self.quit_max_streak_labels = []
        self.quit_check_no_buttons = []
        for i in range(len(quit_allHabits)):
            if (i%2==0):
                self.quit_habit_name_labels.append(Button(
                    text=str(quit_allHabits[i][2]),  
                    # disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5], #))
                    on_press = partial(self.delete_quit_task_popup, i)))
                if (quit_allHabits[i][5] != quit_allHabits[i][6]):
                    self.quit_habit_count_labels.append(Button(
                        text=str(quit_allHabits[i][3]+1),  
                        disabled=True, 
                        background_disabled_normal='background_normal', 
                        background_color=[52/255, 110/255, 235/255, 0.5]))
                    # insert code to update db streak count 
                else:
                    self.quit_habit_count_labels.append(Button(
                        text=str(quit_allHabits[i][3]),  
                        disabled=True, 
                        background_disabled_normal='background_normal', 
                        background_color=[52/255, 110/255, 235/255, 0.5]))

            else:
                self.quit_habit_name_labels.append(Button(
                    text=str(quit_allHabits[i][2]),  
                    # disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 1],#))
                    on_press = partial(self.delete_quit_task_popup, i)))
                
                self.quit_habit_count_labels.append(Button(
                    text=str(quit_allHabits[i][3]),  
                    disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 1]))
 
            self.quit_max_streak_labels.append(Button(text = "       Max Streak: " + str(quit_allHabits[i][6]) + "\n Earned on: " + str(quit_allHabits[i][5]), disabled=True, background_disabled_normal='background_normal', background_color = [169/255,255/255,221/255,.5]))
            self.quit_check_no_buttons.append(Button(text = "fuckied it up :(", on_press = partial(self.count_down_quit, self.connection, i), background_color = [253/255, 129/255, 129/255, 1]))

            # self.quit_task=GridLayout(rows=1, cols_minimum={0:200, 1:200})
            self.quitlayout.add_widget(self.quit_habit_name_labels[i])
            self.quitlayout.add_widget(self.quit_habit_count_labels[i])
            self.quitlayout.add_widget(self.quit_max_streak_labels[i])
            self.quitlayout.add_widget(self.quit_check_no_buttons[i])

            # self.quit_tasklayouts.append(self.quit_task)
            # print(self.quit_tasklayouts)
            # self.quithomepage.add_widget(self.quit_task)
            new_counts = partial(self.count_up_by_days, self.connection, i)
            new_counts(i)

            self.quit_i = self.quit_i+1
        self.quithomepage.open()


    def delete_quit_task_popup(self, i, obj):
        self.quithomepage.dismiss()

    def count_down_quit(self, xconnection, i):
        self.quithomepage.dismiss()

    def add_quit_popup(self):
        self.quithomepage.dismiss()

    def count_up_by_days(self, xconnection, ind, instance):
        name = self.quit_habit_name_labels[ind].text
        habit_list = get_habit_by_name(xconnection, name)
        last_mod_date = datetime.strptime((habit_list[0][5]), "%Y-%m-%d").date()
        # category = habit_list[0][2]
        today = date.today()
        print((today-last_mod_date).days)
        if (today-last_mod_date).days != 0:
            self.quit_habit_count_labels[ind].text = str((today-last_mod_date).days)
            update_count(self.quit_habit_count_labels[ind].text, name, 'quit', xconnection)
        else:
            self.quit_habit_count_labels[ind].text = str(habit_list[0][3])
        
        if (today-last_mod_date).days >= habit_list[0][6]:
            self.quit_max_streak_labels[ind].text = "       Max Streak: " + str((today-last_mod_date).days) + "\n Earned on: " + str(date.today())
        pass

# console debugging 
# import datetime
# d1 = datetime.date.today()
#                  datetime.date(2022, 4, 5)
# d2 = datetime.datetime.strptime("2022-04-02", "%Y-%m-%d").date()
# (d1-d2).days

    def count_up_new(self, xconnection, ind, instance):
        name = self.habit_name_labels[ind].text
        habit_list = get_habit_by_name(xconnection, name)
        last_mod_date = habit_list[0][5]
        category = habit_list[0][2]
        today = str(date.today())

        if (last_mod_date == today):
            self.habit_name_labels[ind].text = self.habit_name_labels[ind].text + ": Already done!"
        else:
            self.habit_count_labels[ind].text = str(int(self.habit_count_labels[ind].text) + 1)
            update_count(self.habit_count_labels[ind].text, name, category, xconnection)
            update_last_mod_date(name, xconnection)
        pass
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
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
from functools import partial 
from kivy.clock import Clock
import sys


class SpartanGrid(GridLayout):

    def __init__(self, **kwargs):
        self.db_name = "habits.db"
        self.connection = create_connection(self.db_name)
        create_habit_table(self.connection)

        super(SpartanGrid, self).__init__()
        
        self.dailyHabits = get_all_habits(self.connection, 'habits', 'continue', 'daily')
        self.weeklyHabits = get_all_habits(self.connection, 'habits', 'continue', 'weekly')

        self.dailytasklayouts = []
        self.daily_habit_name_labels = []
        self.daily_habit_count_labels = []
        self.daily_check_yes_buttons = []
        self.daily_check_no_buttons = []
        self.daily_i=0

        self.weeklytasklayouts = []
        self.weekly_habit_name_labels = []
        self.weekly_habit_count_labels = []
        self.weekly_check_yes_buttons = []
        self.weekly_check_no_buttons = []
        self.weekly_i=0
        self.quit_i=0

        self.daily_i = self.initialize_habits(self.dailyHabits, self.daily_habit_name_labels, self.daily_habit_count_labels, self.daily_check_yes_buttons, self.daily_count_up_new, self.daily_check_no_buttons, self.daily_count_down_new, self.dailytasklayouts, self.daily_i)
        self.weekly_i = self.initialize_habits(self.weeklyHabits, self.weekly_habit_name_labels, self.weekly_habit_count_labels, self.weekly_check_yes_buttons, self.weekly_count_up_new, self.weekly_check_no_buttons, self.weekly_count_down_new, self.weeklytasklayouts, self.weekly_i)

        # for i in range(len(self.dailyHabits)):
        #     if (self.dailyHabits[i][5] == str(date.today())):
        #         self.daily_check_yes_buttons[i].text = "Done!"
        #         self.daily_check_yes_buttons[i].disabled = True
        #         self.daily_check_yes_buttons[i].background_disabled_normal='atlas://data/images/defaulttheme/button'
        #         self.daily_check_yes_buttons[i].background_color = [169/255,255/255,221/255, 0.5]
        
        # for i in range(len(self.weeklyHabits)):
        #     if (((datetime.strptime(self.weeklyHabits[i][5], '%Y-%m-%d')).date() + timedelta(weeks=1)) >= date.today()):
        #         self.weekly_check_yes_buttons[i].text = "Done!"
        #         self.weekly_check_yes_buttons[i].disabled = True
        #         self.weekly_check_yes_buttons[i].background_disabled_normal='atlas://data/images/defaulttheme/button'
        #         self.weekly_check_yes_buttons[i].background_color = [169/255,255/255,221/255, 0.5]

        self.initialize_add_daily_task_popup()
        self.initialize_add_weekly_task_popup()
        self.initialize_weekly_task_popup()

        self.initialize_homepage()

    def initialize_habits(self, habit_list, name_labels, count_labels, cy_buttons, count_up, cn_buttons, count_down, tlayouts, habit_i):
        
        for i in range(len(habit_list)):
            name_labels.append(Button(
                text=str(habit_list[i][2]),                   
                on_press = partial(self.edit_task_popup, i, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i), 
                size_hint=(.3, 1)))

            count_labels.append(Button(
                text=str(habit_list[i][3]),  
                disabled=True, 
                background_disabled_normal='atlas://data/images/defaulttheme/button', 
                size_hint=(.3, 1)))
            
            if (i%2==0):
                name_labels[i].background_color=[52/255, 110/255, 235/255, 0.5]
                count_labels[i].background_color=[52/255, 110/255, 235/255, 0.5]
            else:
                name_labels[i].background_color=[52/255, 110/255, 235/255, 1]
                count_labels[i].background_color=[52/255, 110/255, 235/255, 1]
 
            cy_buttons.append(Button(text = "Did it!", on_press = partial(count_up, self.connection, i), background_color = [169/255,255/255,221/255,1], size_hint=(.2, 1)))
            
            cn_buttons.append(Button(text = "Didn't", on_press = partial(count_down, self.connection, i), background_color = [253/255, 129/255, 129/255, 1], size_hint=(.2, 1)))

            habit_i = habit_i+1

        return habit_i

    def initialize_homepage(self):
        self.cols=1
        self.rows_minimum={0:40}
        self.padding=[100,100,100,100]

        # "Habit Tracker" title
        self.add_widget(Button(
            text="Habit Tracker", 
            font_size="35sp", 
            disabled=True, 
            background_disabled_normal='background_normal', 
            background_color=[52/255, 110/255, 235/255, 0.5]))

        # buttons below the title, to view weekly habits and view habits to quit
        other_pages_buttons = GridLayout(cols=2)
        weekly_habits_btn = Button(text="View Weekly Habits")
        weekly_habits_btn.bind(on_press=partial(self.open_popup, self.weeklyhomepage))
        other_pages_buttons.add_widget(weekly_habits_btn)
        quitting_habits_btn = Button(text="View Tasks to Quit")
        quitting_habits_btn.bind(on_press=self.show_quitting_popup)
        other_pages_buttons.add_widget(quitting_habits_btn)
        self.add_widget(other_pages_buttons)

        # daily habits header, title and button to add task
        daily_habits_header = BoxLayout(orientation='horizontal')
        daily_habits_header.add_widget(Button(
            text="Daily Habits", 
            font_size="20sp", 
            disabled=True, 
            background_disabled_normal='background_normal', 
            background_color=[52/255, 110/255, 235/255, 0.5], 
            size_hint=(.75, 1)))
        add_task_btn = Button(text="Add Daily Task", size_hint=(.25, 1))
        add_task_btn.bind(on_press=partial(self.open_popup, self.add_daily_popup))
        daily_habits_header.add_widget(add_task_btn)
        self.add_widget(daily_habits_header)

        for num in range(len(self.dailyHabits)):
            dtask=BoxLayout(orientation='horizontal')
            dtask.add_widget(self.daily_habit_name_labels[num])
            dtask.add_widget(self.daily_habit_count_labels[num])
            dtask.add_widget(self.daily_check_yes_buttons[num])
            dtask.add_widget(self.daily_check_no_buttons[num])

            self.dailytasklayouts.append(dtask)
            self.add_widget(dtask)

    def initialize_weekly_task_popup(self):
        
        self.weeklylayout = GridLayout(cols=1)
        self.weeklyhomepage = Popup(title="Weekly Habits", content = self.weeklylayout)

        self.weeklylayout.cols=1
        self.weeklylayout.padding=[100,100,100,100]

        # buttons below the title, to view daily habits and view habits to quit
        other_pages_buttons = GridLayout(cols=2)
        daily_habits_btn = Button(text="View Daily Habits")
        daily_habits_btn.bind(on_press=partial(self.close_popup, self.weeklyhomepage))
        other_pages_buttons.add_widget(daily_habits_btn)
        quitting_habits_btn = Button(text="View Tasks to Quit")
        quitting_habits_btn.bind(on_press=self.show_quitting_popup)
        other_pages_buttons.add_widget(quitting_habits_btn)
        self.weeklylayout.add_widget(other_pages_buttons)

        # weekly habits header, title and button to add task
        weekly_habits_header = BoxLayout(orientation='horizontal')
        weekly_habits_header.add_widget(Button(
            text="Weekly Habits", 
            font_size="20sp", 
            disabled=True, 
            background_disabled_normal='background_normal', 
            background_color=[52/255, 110/255, 235/255, 0.5], 
            size_hint=(.75, 1)))
        add_task_btn = Button(text="Add Weekly Task", size_hint=(.25, 1))
        add_task_btn.bind(on_press=partial(self.open_popup, self.add_weekly_popup))
        weekly_habits_header.add_widget(add_task_btn)
        self.weeklylayout.add_widget(weekly_habits_header)

        for num in range(len(self.weeklyHabits)):
            wtask=BoxLayout(orientation='horizontal')
            wtask.add_widget(self.weekly_habit_name_labels[num])
            wtask.add_widget(self.weekly_habit_count_labels[num])
            wtask.add_widget(self.weekly_check_yes_buttons[num])
            wtask.add_widget(self.weekly_check_no_buttons[num])

            self.weeklytasklayouts.append(wtask)
            self.weeklylayout.add_widget(wtask)

    def initialize_add_daily_task_popup(self):
        add_daily_playout = GridLayout(cols = 2, padding=[200, 200, 200, 200], rows_minimum={0:150})
        self.add_daily_popup = Popup(title = "Add Task", content = add_daily_playout)
        self.add_daily_popup.plabel = Button(
                    text="Add Task",  
                    disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5])
        self.add_daily_popup.ptext = TextInput(multiline=False, write_tab=False, on_text_validate=partial(self.add_task, 'daily', self.add_daily_popup, self.connection))
    
        # self.popup.olabel = Button(
        #             text="Occurrence",  
        #             disabled=True, 
        #             background_disabled_normal='background_normal', 
        #             background_color=[52/255, 110/255, 235/255, 0.25])
        # self.popup.otext="daily"
        # self.popup.occur_buttons = GridLayout(cols=2)
        # self.popup.daily_button = Button(text="Daily", disabled=True, on_press = self.set_daily, background_color=[52/255, 110/255, 235/255, 1])
        # self.popup.weekly_button = Button(text="Weekly", on_press = self.set_weekly, background_color=[52/255, 110/255, 235/255, 1])
        # self.popup.occur_buttons.add_widget(self.popup.daily_button)
        # self.popup.occur_buttons.add_widget(self.popup.weekly_button)

        self.add_daily_popup.pbutton = Button(text = "Cancel", on_press = partial(self.close_popup, self.add_daily_popup))
        self.add_daily_popup.pbutton_add = Button(text = "Add", on_press = partial(self.add_task, 'daily', self.add_daily_popup, self.connection))
        add_daily_playout.add_widget(self.add_daily_popup.plabel)
        add_daily_playout.add_widget(self.add_daily_popup.ptext)
        # playout.add_widget(self.popup.olabel)
        # playout.add_widget(self.popup.occur_buttons)
        add_daily_playout.add_widget(self.add_daily_popup.pbutton)
        add_daily_playout.add_widget(self.add_daily_popup.pbutton_add)

    def initialize_add_weekly_task_popup(self):
        add_weekly_playout = GridLayout(cols = 2, padding=[200, 200, 200, 200], rows_minimum={0:150})

        self.add_weekly_popup = Popup(title = "Add Task", content = add_weekly_playout)
        self.add_weekly_popup.plabel = Button(
                    text="Add Task",  
                    disabled=True, 
                    background_disabled_normal='background_normal', 
                    background_color=[52/255, 110/255, 235/255, 0.5])
        self.add_weekly_popup.ptext = TextInput(multiline=False, write_tab=False, on_text_validate=partial(self.add_task, 'weekly', self.add_weekly_popup, self.connection))

        self.add_weekly_popup.pbutton = Button(text = "Cancel", on_press = partial(self.close_popup, self.add_weekly_popup))
        self.add_weekly_popup.pbutton_add = Button(text = "Add", on_press = partial(self.add_task, 'weekly', self.add_weekly_popup, self.connection))
        add_weekly_playout.add_widget(self.add_weekly_popup.plabel)
        add_weekly_playout.add_widget(self.add_weekly_popup.ptext)

        add_weekly_playout.add_widget(self.add_weekly_popup.pbutton)
        add_weekly_playout.add_widget(self.add_weekly_popup.pbutton_add)


# count up and down functions
    def daily_count_up_new(self, xconnection, ind, instance):
        button_name = self.daily_check_yes_buttons[ind].text
        name = self.daily_habit_name_labels[ind].text
        if (button_name.find("Done!") != -1):
            return
        else:
            habit_list = get_habit_by_name(xconnection, name)
            last_mod_date = habit_list[0][5]
            category = habit_list[0][1]
            today = str(date.today())
            if (last_mod_date == today):
                pass
            else:
                self.daily_habit_count_labels[ind].text = str(int(self.daily_habit_count_labels[ind].text) + 1)
                update_count(self.daily_habit_count_labels[ind].text, name, category, xconnection)
                update_last_mod_date(name, xconnection)

                self.daily_check_yes_buttons[ind].text = "Done!"
                self.daily_check_yes_buttons[ind].disabled=True
                self.daily_check_yes_buttons[ind].background_disabled_normal='atlas://data/images/defaulttheme/button'
                self.daily_check_yes_buttons[ind].background_color = [169/255,255/255,221/255, 0.5]
        
    def weekly_count_up_new(self, xconnection, ind, instance):
        button_name = self.weekly_check_yes_buttons[ind].text
        name = self.weekly_habit_name_labels[ind].text
        if (button_name.find("Done!") != -1):
            return
        else:
            habit_list = get_habit_by_name(xconnection, name)
            last_mod_date = (datetime.strptime(habit_list[0][5], '%Y-%m-%d')).date()
            category = habit_list[0][1]
            today = date.today()
            if (last_mod_date + timedelta(weeks=1) >= today):
                pass
            else:
                self.weekly_habit_count_labels[ind].text = str(int(self.weekly_habit_count_labels[ind].text) + 1)
                update_count(self.weekly_habit_count_labels[ind].text, name, category, xconnection)
                update_last_mod_date(name, xconnection)

                self.weekly_check_yes_buttons[ind].text = "Done!"
                self.weekly_check_yes_buttons[ind].disabled=True
                self.weekly_check_yes_buttons[ind].background_disabled_normal='atlas://data/images/defaulttheme/button'
                self.weekly_check_yes_buttons[ind].background_color = [169/255,255/255,221/255, 0.5]

    def daily_count_down_new(self, xconnection, ind, instance):
        name = self.daily_habit_name_labels[ind].text
        self.daily_habit_count_labels[ind].text = str(0)
        update_count(0, name, 'continue', xconnection)
        pass

    def weekly_count_down_new(self, xconnection, ind, instance):
        name = self.weekly_habit_name_labels[ind].text
        self.weekly_habit_count_labels[ind].text = str(0)
        update_count(0, name, 'continue', xconnection)
        pass


# add task function
    def add_task(self, occurrence, popup, xconnection, instance):
        print("Breakpoint SWAG CHICKEN")
        today = date.today()
        yesterday = today - timedelta(days = 1)
        h2 = Habit(self.db_name[:-3],"continue", popup.ptext.text, 0, today, yesterday, 0, occurrence)
        insert_habit(h2, xconnection)
        self.dailyHabits = get_all_habits(self.connection, self.db_name[:-3], 'continue', 'daily')
        self.weeklyHabits = get_all_habits(self.connection, self.db_name[:-3], 'continue', 'weekly')

        popup.dismiss()

        if (occurrence == 'daily'):
            self.daily_i = self.new_task_to_page(self, self.dailyHabits, self.daily_habit_name_labels, self.daily_habit_count_labels, self.daily_check_yes_buttons, self.daily_count_up_new, self.daily_check_no_buttons, self.daily_count_down_new, self.dailytasklayouts, self.daily_i)
        else:
            self.weekly_i = self.new_task_to_page(self.weeklylayout, self.weeklyHabits, self.weekly_habit_name_labels, self.weekly_habit_count_labels, self.weekly_check_yes_buttons, self.weekly_count_up_new, self.weekly_check_no_buttons, self.weekly_count_down_new, self.weeklytasklayouts, self.weekly_i)
        
        pass
    
    def new_task_to_page(self, page, habit_list, name_labels, count_labels, cy_buttons, count_up, cn_buttons, count_down, tlayouts, habit_i):

        name_labels.append(Button(
            text=str(habit_list[habit_i][2]),  
            on_press = partial(self.edit_task_popup, habit_i, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i), 
            size_hint=(.3, 1)))

        count_labels.append(Button(
            text=str(habit_list[habit_i][3]),  
            disabled=True, 
            background_disabled_normal='atlas://data/images/defaulttheme/button', 
            size_hint=(.3, 1)))

        if (habit_i%2==0):
            name_labels[habit_i].background_color = [52/255, 110/255, 235/255, 0.5]
            count_labels[habit_i].background_color = [52/255, 110/255, 235/255, 0.5]
        else:
            name_labels[habit_i].background_color = [52/255, 110/255, 235/255, 1]
            count_labels[habit_i].background_color = [52/255, 110/255, 235/255, 1]

        cy_buttons.append(Button(text = "Did it!", on_press = partial(count_up, self.connection, habit_i), background_color = [169/255,255/255,221/255,1], size_hint=(.2, 1)))
        cn_buttons.append(Button(text = "Didn't", on_press = partial(count_down, self.connection, habit_i), background_color = [253/255, 129/255, 129/255, 1], size_hint=(.2, 1)))

        new_task = BoxLayout(orientation='horizontal')
        new_task.add_widget(name_labels[habit_i])
        new_task.add_widget(count_labels[habit_i])
        new_task.add_widget(cy_buttons[habit_i])
        new_task.add_widget(cn_buttons[habit_i])
        tlayouts.append(new_task)
        page.add_widget(new_task)

        # if (habit_list[habit_i][7] == 'daily'):
        #     self.add_widget(new_task)
        #     self.add_widget(Label())
        # else:
        #     self.add_widget(Label())
        #     self.add_widget(new_task)

        return habit_i+1 

# edit task popup
    def edit_task_popup(self, j, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i, obj):
        edit_playout = GridLayout(cols=1, padding=[200,100,200,200])
        self.edit_popup = Popup(title="Edit a task", content = edit_playout)
        
        close_button = GridLayout(cols=6)
        for i in range(4):
            close_button.add_widget(Label())
        close_button.add_widget(Button(text="x", size_hint_y=None, height=80, on_press = self.close_popup_delete))

        edit_row = GridLayout(cols=2)
        edit_row.add_widget(Button(text="Edit Task Name: ", disabled=True, background_disabled_normal='background_normal', background_color=[52/255, 110/255, 235/255, 0.5]))
        self.edit_popup.pname = TextInput(text = name_labels[j].text, multiline=False, write_tab=False, on_text_validate=partial(self.update_task_name, j, name_labels))
        edit_row.add_widget(self.edit_popup.pname)

        edit_playout.add_widget(close_button)
        edit_playout.add_widget(edit_row)
        edit_playout.add_widget(Button(text="Save Changes", on_press = partial(self.update_task_name, j, name_labels), background_color=[52/255, 110/255, 235/255, 0.5]))
        edit_playout.add_widget(Button(text="Delete Task: " + name_labels[j].text, background_color = [253/255, 129/255, 129/255, 1], on_press = partial(self.delete_task, j, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i, self.connection)))
        self.edit_popup.open()

    def delete_task(self, l, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i, connection, instance):
        delete_task_db(name_labels[l].text, connection)

        # for m in range(l, len(habit_list)):
        #     name_labels[m].on_press = Button(
        #         text=str(habit_list[m][2]),                   
        #         on_press = partial(self.edit_task_popup, m-1, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i), 
        #         background_color=[52/255, 110/255, 235/255, 0.5])

        del habit_list[l]
        del name_labels[l]
        del count_labels[l]
        del cy_buttons[l]
        del cn_buttons[l]

        for m in reversed(range(l, (len(habit_list)))):
            
            name_labels[m].parent.remove_widget(name_labels[m])       
            # name_labels[m].on_press = partial(self.edit_task_popup, m, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i)
            count_labels[m].parent.remove_widget(count_labels[m])
            cy_buttons[m].parent.remove_widget(cy_buttons[m])
            cn_buttons[m].parent.remove_widget(cn_buttons[m])

            name_labels[m] = Button(
                text=str(habit_list[m][2]),                   
                on_press = partial(self.edit_task_popup, m, habit_list, name_labels, count_labels, cy_buttons, cn_buttons, tlayouts, habit_i),  
                size_hint=(.3, 1))     
            if (m%2==0):
                name_labels[m].background_color = [52/255, 110/255, 235/255, 0.5]
                count_labels[m].background_color = [52/255, 110/255, 235/255, 0.5]
            else:
                name_labels[m].background_color = [52/255, 110/255, 235/255, 1]
                count_labels[m].background_color = [52/255, 110/255, 235/255, 1]

            self.remove_widget(tlayouts[m])
            del tlayouts[m]

        
        for n in range(l, len(habit_list)):
            #print(habit_list[n][2])
            recreate_task=BoxLayout(orientation='horizontal')
            recreate_task.add_widget(name_labels[n])
            recreate_task.add_widget(count_labels[n])
            recreate_task.add_widget(cy_buttons[n])
            recreate_task.add_widget(cn_buttons[n])

            tlayouts.append(recreate_task)
            self.add_widget(recreate_task)

        self.decrement_num(habit_i, habit_list)

        self.close_popup_delete(l)
        pass

    def decrement_num(self, habit_num, habit_list):
        if (habit_list == self.dailyHabits):
            print("true")
            self.daily_i = self.daily_i-1
        else:
            print('false')
            self.weekly_i = self.weekly_i-1

    def close_popup_delete(self, obj):
        self.loading_close_popup(obj)
        Clock.schedule_once(self.edit_popup.dismiss, 2)
    
    def loading_close_popup(self, obj):
        playout4 = GridLayout(cols=1, padding=[300,450,300,450])
        self.popup_lc = Popup(title="Loading", content = playout4)
        self.popup_lc.pcloser =  Button(text = "Loading...", disabled=True, background_disabled_normal='background_normal', background_color=[52/255, 110/255, 235/255, 0.5])
        playout4.add_widget(self.popup_lc.pcloser)
        Clock.schedule_once(self.popup_lc.dismiss, 2)
        self.popup_lc.open()



    def show_limit_popup(self):
        playout3 = GridLayout(cols = 1)
        self.popup_limit = Popup(title = "You've reached the limit", content = playout3)
        self.popup_limit.plabel = Label(text = "You have reached the limit of tasks you can add.")
        self.popup_limit.pcount = Label(text = "You currently have " + str(self.i) + " tasks.")
        self.popup_limit.pbutton = Button(text = "Cancel", on_press = self.close_popup_limit)
        playout3.add_widget(self.popup_limit.plabel)
        playout3.add_widget(self.popup_limit.pcount)
        playout3.add_widget(self.popup_limit.pbutton)
        print(self.i)
        self.popup_limit.open()

    def close_popup_limit(self, obj):
        self.popup_limit.dismiss()



    def update_task_name(self, i, name_labels, obj):
        update_name(self.edit_popup.pname.text, name_labels[i].text, self.connection)
        name_labels[i].text = self.edit_popup.pname.text
        self.close_popup_delete(obj)

    def set_daily(self, obj):
        self.popup.otext = "daily"
        self.popup.daily_button.disabled=True
        self.popup.weekly_button.disabled=False
        pass

    def set_weekly(self, obj):
        self.popup.otext = "weekly"
        self.popup.daily_button.disabled=False
        self.popup.weekly_button.disabled=True
        pass        

    def open_popup(self, pop, obj):
        pop.open()

    def close_popup(self, pop, obj):
        pop.dismiss()


# ------------------------------------------------------------------------------------------------
# ---------------------------- Quitting is a lot of ~work~ -----------------------------
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

        quit_Habits = get_all_habits(self.connection, 'habits', 'quit', 'daily')

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

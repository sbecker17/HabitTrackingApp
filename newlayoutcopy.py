from multiprocessing import connection
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
from functools import partial 
from kivy.clock import Clock


class SpartanGrid(GridLayout):

    def __init__(self, **kwargs):
        self.db_name = "elena.db"
        self.connection = create_connection(self.db_name)
        create_habit_table(self.connection)

        super(SpartanGrid, self).__init__()
        self.cols = 2

        self.add_widget(Label(text="Task Name:"))
        self.t_name = TextInput(multiline=False)
        self.add_widget(self.t_name)

        self.add_widget(Button(text= "Delete task", on_press = self.delete_task_popup, background_color = [253/255, 129/255, 129/255, 1])) #(Label(text="Task Category:"))
        self.t_cat = TextInput(text = "category")
        # self.delete_task_btn = Button(text= "Delete task", on_press = self.delete_task_popup, background_color = [253/255, 129/255, 129/255, 1])
        self.add_widget(self.t_cat)

        self.press = Button(text="Click me")
        self.press.bind(on_press=lambda x:self.click_me_new(xconnection = self.connection, db_name = self.db_name))
        self.add_widget(self.press)

        self.press = Button(text="Add Task")
        self.press.bind(on_press=self.show_popup)
        self.add_widget(self.press)

        # self.press = Button(Text="Delete Task", on_press=self.delete_task_popup)
        # self.add_widget(self.press)

        # allHabits = []
        allHabits = get_all_habits(self.connection, 'elena')
        print(allHabits)
        # self.allHabitsdict = {}

        # for i in allHabits:
        #     # user, cat, name, cnt, date
        #     # name : [user, cat, cnt, date]
        #     self.allHabitsdict.update({i[2] : [i[0], i[1], i[3], i[4]]})
            # print(self.allHabitsdict)
            # allHabitsdict.update({i[0], i[1],i[2],i[3],i[4]})
            # print(self.allHabitsdict[0])

        # for key,value in self.allHabitsdict.items():
        #     self.key = Label(text = str(key), bold = True)
        #     self.keycount = Label(text = str(value[2]))
           
            
        #     # self.habit1cnt = Label(text = str(h1.count))
        #     # self.habit1 = Label(text = h1.name, bold = True)
        #     self.didIt = Button(text = "Did it!", on_press=lambda y:self.count_up(xconnection = self.connection, hab=h1), background_color = [169/255,255/255,221/255,1])
        #     self.didnt = Button(text = "Not today", on_press=lambda z:self.count_down(xconnection=self.connection, hab=h1), background_color = [253/255, 129/255, 129/255, 1])
        #     # self.didnt = Button(text = "Not today",  background_color = [253/255, 129/255, 129/255, 1])

        # for key, value in self.allHabitsdict.items():


        #     self.add_widget(self.key)
        #     self.add_widget(self.keycount)
        #     self.add_widget(self.didIt)
        #     self.add_widget(self.didnt)

        self.h0 = Label()
        self.h1 = Label()
        self.h2 = Label()
        self.h3 = Label()
        self.h4 = Label()
        self.h5 = Label()
        self.h6 = Label()
        self.h7 = Label()
        self.h8 = Label()
        self.h9 = Label()
        self.h10 = Label()
        self.counth0 = Label()
        self.counth1 = Label()
        self.counth2 = Label()
        self.counth3 = Label()
        self.counth4 = Label()
        self.counth5 = Label()
        self.counth6 = Label()
        self.counth7 = Label()
        self.counth8 = Label()
        self.counth9 = Label()
        self.counth10 = Label()
        self.didIt0 = Button()
        self.didIt1 = Button()
        self.didIt2 = Button()
        self.didIt3 = Button()
        self.didIt4 = Button()
        self.didIt5 = Button()
        self.didIt6 = Button()
        self.didIt7 = Button()
        self.didIt8 = Button()
        self.didIt9 = Button()
        self.didIt10 = Button()
        self.didnt0 = Button()
        self.didnt1 = Button()
        self.didnt2 = Button()
        self.didnt3 = Button()
        self.didnt4 = Button()
        self.didnt5 = Button()
        self.didnt6 = Button()
        self.didnt7 = Button()
        self.didnt8 = Button()
        self.didnt9 = Button()
        self.didnt10 = Button()
        self.habit_name_labels = [self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7, self.h8, self.h9, self.h10]
        self.habit_count_labels = [self.counth0, self.counth1, self.counth2, self.counth3, self.counth4, self.counth5, self.counth6, self.counth7, self.counth8, self.counth9, self.counth10]
        self.check_yes_buttons = [self.didIt0, self.didIt1, self.didIt2, self.didIt3, self.didIt4, self.didIt5, self.didIt6, self.didIt7, self.didIt8, self.didIt9, self.didIt10]
        #                     self.didIt11, self.didIt12, self.didIt13, self.didIt14, self.didIt15, self.didIt16, self.didIt17, self.didIt18, self.didIt19]
        self.check_no_buttons = [self.didnt0, self.didnt1, self.didnt2, self.didnt3, self.didnt4, self.didnt5, self.didnt6, self.didnt7, self.didnt8, self.didnt9, self.didnt10]
        #                     self.didnt11, self.didnt12, self.didnt13, self.didnt14, self.didnt15, self.didnt16, self.didnt17, self.didnt18, self.didnt19]
        self.i=0
        for i in range(len(allHabits)):
        # for i in range(2):
            print(i)
            # print("Habit cnt: ", self.habit_count_labels[i])
            self.habit_count_labels[i].text = str(allHabits[i][3])
            # self.habit_count_labels[i].ids = {str(allHabits[i][2])+"_count": self.habit_count_labels[i]}
            self.habit_name_labels[i].text = str(allHabits[i][2])
            # self.habit_name_labels[i].ids = {str(allHabits[i][2]): self.habit_name_labels[i]}
            # print(self.habit_name_labels[i].ids)
            # self.ids.update(self.habit_name_labels[i].ids) 
            # print(self.ids)
            # self.ids.update(self.habit_count_labels[i].ids) 
            # print(self.ids)
            # cntLabel = self.ids[str(allHabits[i][2])+"_count"]
            # print("hbt cnt label: ", cntLabel)
            # print(self.ids[str(allHabits[i][2])])
            self.habit_count_labels[i] = Label(text = str(allHabits[i][3]))
            # print(self.check_yes_buttons[i])
            self.check_yes_buttons[i] = Button(text = "Did it!", on_press = partial(self.count_up_new, self.connection, i), background_color = [169/255,255/255,221/255,1])
            # self.check_yes_buttons[i] = Button(text = "Did it!", on_press = lambda x:self.count_up_new(xconnection = self.connection, loc = i), background_color = [169/255,255/255,221/255,1])
            # self.check_yes_buttons[i].ids= {str(allHabits[i][2])+"_yes"+str(i): self.check_yes_buttons[i]}
            # self.ids.update(self.check_yes_buttons[i].ids) 
            # print(self.ids)
            self.check_no_buttons[i] = Button(text = "Didn't", on_press = partial(self.count_down_new, self.connection, i), background_color = [253/255, 129/255, 129/255, 1])
            self.add_widget(self.habit_name_labels[i])
            self.add_widget(self.habit_count_labels[i])
            self.add_widget(self.check_yes_buttons[i])
            # print("yes btn: ", self.check_yes_buttons[i])
            self.add_widget(self.check_no_buttons[i])
            self.i = self.i+1
        # delete_task_db("h2o", self.connection)


        # for i in allHabits:
        #     # allHabitsdict.update({i[0], i[1],i[2],i[3],i[4]})
        #     # print(allHabitsdict[0])
        #     print(i)
        #     h1 = Habit(i[0],i[1],i[2],i[3],i[4])
            
        #     self.habit1cnt = Label(text = str(h1.count))
        #     self.habit1 = Label(text = h1.name, bold = True)
        #     self.didIt = Button(text = "Did it!", on_press=lambda y:self.count_up_dict(xconnection = self.connection, hab_key=i[2]), background_color = [169/255,255/255,221/255,1])
        #     self.didnt = Button(text = "Not today", on_press=lambda z:self.count_down(xconnection=self.connection, hab=h1), background_color = [253/255, 129/255, 129/255, 1])
        #     # self.didnt = Button(text = "Not today",  background_color = [253/255, 129/255, 129/255, 1])

        #     self.add_widget(self.habit1)
        #     self.add_widget(self.habit1cnt)
        #     self.add_widget(self.didIt)
        #     self.add_widget(self.didnt)
                        

    def count_up(self, xconnection, hab):
        # delete_task_db("h2o", xconnection)
        print(self.habit1.text)
        print(str(hab.name))
        if (self.habit1.text == str(hab.name)):
            self.habit1cnt.text = str(int(hab.count)+1)
            hab.count = hab.count+1
            update_count(self.habit1cnt.text, hab.name, xconnection)
        else:
            pass

    def count_up_new(self, xconnection, ind, instance):
        name = self.habit_name_labels[ind].text
        # cntUpdate = self.ids[loc+"_count"]
        self.habit_count_labels[ind].text = str(int(self.habit_count_labels[ind].text) + 1)
        # self.ids[loc+"_count"].text = str(int(cntUpdate.text) + 1)
        update_count(self.habit_count_labels[ind].text, name, xconnection)
        pass



    def count_down(self, xconnection, hab):
        if (self.habit1.text == str(hab.name)):
            self.habit1cnt.text = "0"
            hab.count = 0
            #self.habit1cnt.text = str(int(self.habit1cnt.text))
            update_count(0, self.habit1.text, xconnection)
        else: 
            pass

    def count_down_new(self, xconnection, ind, instance):
        name = self.habit_name_labels[ind].text
        self.habit_count_labels[ind].text = str(0)
        update_count(0, name, xconnection)
        pass
        
    def click_me(self, xconnection, db_name):
        h1 = Habit(db_name[:-3], self.t_cat.text, self.t_name.text, 0, date.today())
        insert_habit(h1, xconnection)
        get_first_habit(xconnection)
        self.habit1cnt = Label(text = "0")
        self.habit1 = Label(text = h1.name, bold = True)
        self.didIt = Button(text = "Did it!", on_press = lambda x:self.count_up(xconnection = self.connection, hab = h1), background_color = [169/255,255/255,221/255,1])
        self.didnt = Button(text = "Not today", on_press = lambda y: self.count_down(xconnection=self.connection, hab=h1), background_color = [253/255, 129/255, 129/255, 1])
        self.add_widget(self.habit1)
        self.add_widget(self.habit1cnt)
        self.add_widget(self.didIt)
        self.add_widget(self.didnt)

    def click_me_new(self, xconnection, db_name):
        if (self.i == len(self.habit_name_labels)):
            self.show_limit_popup()
            pass
        else: 
            h1 = Habit(db_name[:-3], self.t_cat.text, self.t_name.text, 0, date.today())
            insert_habit(h1, xconnection)
            allHabits = get_all_habits(self.connection, db_name[:-3])
            self.t_cat.hint_text = "Task category"
            self.t_name.hint_text = "Task name"
            self.t_name.text = ""
            # print(allHabits)
            self.habit_count_labels[self.i].text = str(allHabits[self.i][3])
            self.habit_name_labels[self.i].text = str(allHabits[self.i][2])
            self.habit_count_labels[self.i] = Label(text = str(allHabits[self.i][3]))
            self.check_yes_buttons[self.i] = Button(text = "Did it!", on_press = partial(self.count_up_new, self.connection, self.i), background_color = [169/255,255/255,221/255,1])
            self.check_no_buttons[self.i] = Button(text = "Didn't", on_press = partial(self.count_down_new, self.connection, self.i), background_color = [253/255, 129/255, 129/255, 1])
            self.add_widget(self.habit_name_labels[self.i])
            self.add_widget(self.habit_count_labels[self.i])
            self.add_widget(self.check_yes_buttons[self.i])
            self.add_widget(self.check_no_buttons[self.i])
            self.i = self.i+1 
            pass

    def show_popup(self, obj):
        playout = GridLayout(cols = 1)
        self.popup = Popup(title = "Add Task", content = playout)
        self.popup.plabel = Label(text = "Task Name")
        self.popup.ptext = TextInput()
        self.popup.pbutton = Button(text = "Cancel", on_press = self.close_popup)
        self.popup.pbutton_add = Button(text = "Add", on_press = partial(self.add_task_new, self.connection))
        playout.add_widget(self.popup.plabel)
        playout.add_widget(self.popup.ptext)
        playout.add_widget(self.popup.pbutton)
        playout.add_widget(self.popup.pbutton_add)
        #self.popup = Popup(title = "Test popup", content = playout)
        self.popup.open()

    def close_popup(self, obj):
        self.popup.dismiss()

    def add_task(self, xconnection):
        h2 = Habit(self.db_name[:-3],"cat", self.popup.ptext.text, 0, date.today())
        print(h2.name)
        insert_habit(h2, xconnection)
        get_first_habit(xconnection)
        self.popup.dismiss()

    def add_task_new(self, xconnection, instance):
        h2 = Habit(self.db_name[:-3],"cat", self.popup.ptext.text, 0, date.today())
        print(h2.name)
        insert_habit(h2, xconnection)
        allHabits = get_all_habits(self.connection, self.db_name[:-3])
        print(allHabits)
        self.popup.dismiss()
        self.habit_count_labels[self.i].text = str(allHabits[self.i][3])
        self.habit_name_labels[self.i].text = str(allHabits[self.i][2])
        self.habit_count_labels[self.i] = Label(text = str(allHabits[self.i][3]))
        self.check_yes_buttons[self.i] = Button(text = "Did it!", on_press = partial(self.count_up_new, self.connection, self.i), background_color = [169/255,255/255,221/255,1])
        self.check_no_buttons[self.i] = Button(text = "Didn't", on_press = partial(self.count_down_new, self.connection, self.i), background_color = [253/255, 129/255, 129/255, 1])
        self.add_widget(self.habit_name_labels[self.i])
        self.add_widget(self.habit_count_labels[self.i])
        self.add_widget(self.check_yes_buttons[self.i])
        self.add_widget(self.check_no_buttons[self.i])
        self.i = self.i+1 
        pass

    def delete_task(self, i, connection, instance):
        delete_task_db(self.habit_name_labels[i].text, connection)
        self.remove_widget(self.habit_name_labels[i])
        self.remove_widget(self.habit_count_labels[i])
        self.remove_widget(self.check_yes_buttons[i])
        self.remove_widget(self.check_no_buttons[i])
        # i am forseeing potential problems with if a user deletes a task and keeps using the app, as the index of things will b different
        self.i = self.i - 1
        pass

    def show_limit_popup(self):
        playout = GridLayout(cols = 1)
        self.popup_limit = Popup(title = "You've reached the limit", content = playout)
        self.popup_limit.plabel = Label(text = "You have reached the limit of tasks you can add.")
        self.popup_limit.pcount = Label(text = "You currently have " + str(self.i) + " tasks.")
        self.popup_limit.pbutton = Button(text = "Cancel", on_press = self.close_popup_limit)
        # self.popup.pbutton_add = Button(text = "Add", on_press = partial(self.add_task_new, self.connection))
        playout.add_widget(self.popup_limit.plabel)
        playout.add_widget(self.popup_limit.pcount)
        playout.add_widget(self.popup_limit.pbutton)
        # playout.add_widget(self.popup.pbutton_add)
        #self.popup = Popup(title = "Test popup", contentdel = playout)
        print(self.i)
        self.popup_limit.open()

    def close_popup_limit(self, obj):
        self.popup_limit.dismiss()

    def delete_task_popup(self, obj):
        self.h0_del = Button()
        self.h1_del = Button()
        self.h2_del = Button()
        self.h3_del = Button()
        self.h4_del = Button()
        self.h5_del = Button()
        self.h6_del = Button()
        self.h7_del = Button()
        self.h8_del = Button()
        self.h9_del = Button()
        self.h10_del = Button()
        self.hab_del_btns = [self.h0_del, self.h1_del, self.h2_del, self.h3_del, self.h4_del, self.h5_del, self.h6_del, self.h7_del, self.h8_del, self.h9_del, self.h10_del]
        playout2 = GridLayout(cols=1)
        self.popup_delete = Popup(title="Delete a task", content = playout2)
        self.popup_delete.plabel = Label(text = "Remove each task you no longer want")
        self.popup_delete.pholder =  Button(text = "Close", on_press = self.close_popup_delete)
        playout2.add_widget(self.popup_delete.plabel)
        for i in range(len(self.habit_name_labels)):
            if (self.habit_name_labels[i].text == ""):
                pass
            else:
                self.hab_del_btns[i] = Button(text="Delete " + self.habit_name_labels[i].text, on_press = partial(self.delete_task, i, self.connection), on_release = Clock.schedule_once(self.close_popup_delete, 3))
                playout2.add_widget(self.hab_del_btns[i])
        playout2.add_widget(self.popup_delete.pholder)
        self.popup_delete.open()


    def close_popup_delete(self, obj):

        self.popup_delete.dismiss()













class SpartanApp(App):

    def build(self):
        return SpartanGrid()

if __name__  == "__main__":
    # This line is where we would specify which database the user connects to based on their user information (maybe just a username?)
    # If a matching db already exists, it will connect to that one, if not it creates a new one.
    # create_habit_table(xconnection)
    SpartanApp().run()

    close_connection(SpartanGrid.connection)
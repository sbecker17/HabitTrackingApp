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


class SpartanGrid(GridLayout):

    def __init__(self, **kwargs):
        db_name = "elena.db"
        self.connection = create_connection(db_name)
        create_habit_table(self.connection)

        super(SpartanGrid, self).__init__()
        self.cols = 2

        self.add_widget(Label(text="Task Name:"))
        self.t_name = TextInput(multiline=False)
        self.add_widget(self.t_name)

        self.add_widget(Label(text="Task Category:"))
        self.t_cat = TextInput(text = "category")
        self.add_widget(self.t_cat)

        self.press = Button(text="Click me")
        self.press.bind(on_press=lambda x:self.click_me(xconnection = self.connection, db_name = db_name))
        self.add_widget(self.press)

        self.press = Button(text="Add Task")
        self.press.bind(on_press=self.show_popup)
        self.add_widget(self.press)

        # allHabits = []
        allHabits = get_all_habits(self.connection, 'elena')
        print(allHabits)
        self.allHabitsdict = {}

        for i in allHabits:
            # user, cat, name, cnt, date
            # name : [user, cat, cnt, date]
            self.allHabitsdict.update({i[2] : [i[0], i[1], i[3], i[4]]})
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
            self.check_yes_buttons[i] = Button(text = "Did it!", on_press = partial(self.count_up_new, self.connection, str(allHabits[i][2]), i), background_color = [169/255,255/255,221/255,1])
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
        print(self.habit1.text)
        print(str(hab.name))
        if (self.habit1.text == str(hab.name)):
            self.habit1cnt.text = str(int(hab.count)+1)
            hab.count = hab.count+1
            update_count(self.habit1cnt.text, hab.name, xconnection)
        else:
            pass

    def count_up_new(self, xconnection, loc, ind, instance):
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

    def show_popup(self, obj):
        playout = GridLayout(cols = 1)
        self.popup = Popup(title = "Test popup", content = playout)
        self.popup.plabel = Label(text = "add task")
        self.popup.ptext = TextInput()
        self.popup.pbutton = Button(text = "Cancel", on_press = self.close_popup)
        self.popup.pbutton_add = Button(text = "Add", on_press = lambda y:self.add_task(xconnection=self.connection))
        playout.add_widget(self.popup.plabel)
        playout.add_widget(self.popup.ptext)
        playout.add_widget(self.popup.pbutton)
        playout.add_widget(self.popup.pbutton_add)
        #self.popup = Popup(title = "Test popup", content = playout)
        self.popup.open()

    def close_popup(self, obj):
        self.popup.dismiss()

    def add_task(self, xconnection):
        h2 = Habit("elena","cat", self.popup.ptext.text, 0, date.today())
        print(h2.name)
        insert_habit(h2, xconnection)
        get_first_habit(xconnection)
        self.popup.dismiss()

class SpartanApp(App):

    def build(self):
        return SpartanGrid()

if __name__  == "__main__":
    # This line is where we would specify which database the user connects to based on their user information (maybe just a username?)
    # If a matching db already exists, it will connect to that one, if not it creates a new one.
    # create_habit_table(xconnection)
    SpartanApp().run()

    close_connection(SpartanGrid.connection)
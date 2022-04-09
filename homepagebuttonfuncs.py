from databaseops import *
import sqlite3
from sqlite3 import Error
from datetime import date

# ----------------This file contains all of our old count up and count down function that are not currently in use

# def count_up_new_quit(self, xconnection, ind, instance):
#     name = self.habit_name_labels[ind].text
#     habit_list = get_habit_by_name(xconnection, name)
#     last_mod_date = habit_list[0][5]
#     today = str(date.today())

#     if last_mod_date == today:
#         self.habit_name_labels[ind].text = self.habit_name_labels[ind].text + ": Already done!"
#     else:
#         self.habit_count_labels[ind].text = str(int(self.habit_count_labels[ind].text) + 1)
#         update_count(self.habit_count_labels[ind].text, name, xconnection)
#         update_last_mod_date(name, xconnection)
#     pass

# def count_down(self, xconnection, hab):
#     if (self.habit1.text == str(hab.name)):
#         self.habit1cnt.text = "0"
#         hab.count = 0
#         #self.habit1cnt.text = str(int(self.habit1cnt.text))
#         update_count(0, self.habit1.text, xconnection)
#     else: 
#         pass

# def count_down_new(self, xconnection, ind, instance):
#     name = self.habit_name_labels[ind].text
#     self.habit_count_labels[ind].text = str(0)
#     update_count(0, name, xconnection)
#     pass

# def count_up(self, xconnection, hab):
#     print(self.habit1.text)
#     print(str(hab.name))
#     if (self.habit1.text == str(hab.name)):
#         self.habit1cnt.text = str(int(hab.count)+1)
#         hab.count = hab.count+1
#         update_count(self.habit1cnt.text, hab.name, xconnection)
#     else:
#         pass

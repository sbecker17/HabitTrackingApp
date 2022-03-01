
import sqlite3
from habit import Habit
from datetime import date


# to use a fresh database every time its run, connect to :memory:.
# this is good for testing purposes.
conn = sqlite3.connect('elena_work.db')

c = conn.cursor()

# c.execute("""CREATE TABLE if not exists habitlist
#                             (
#                             category text,
#                             name text,
#                             count integer,
#                             start_date date
#                             )"""
#                          )

def insert_hab(hab):
    with conn:
        c.execute("INSERT INTO habitlist VALUES (:category, :name, :count, :start_date)",
        {'category': hab.category, 'name': hab.name, 'count': hab.count, 'start_date': hab.start_date})

def get_habs_by_name(category):
    c.execute("SELECT * FROM habitlist WHERE name=:category", {'category': category})
    return c.fetchall()

def get_all_habs():
    c.execute("SELECT * FROM habitlist")
    typ = type(c.fetchall())
    return c.fetchall()

hab_1 = Habit('personal','do stuff',0,date.today())
print(hab_1.name)
print(type(hab_1))
print(hab_1.start_date)

# insert_hab(hab_1)

print(get_habs_by_name('category'))


import sqlite3
from sqlite3 import Error

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)


def close_connection(conn):
    conn.close()
# c = conn.cursor()
def create_habit_table(conn):
    conn.cursor().execute("""CREATE TABLE if not exists habitlist
                            (
                            username text,
                            category text,
                            name text,
                            count integer,
                            start_date date
                            )"""
                         )
    conn.commit()

def insert_habit(hab, conn):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO habitlist(username, category, name, count, start_date) VALUES (:username, :category, :name, :count, :start_date)",
        {'username': hab.username, 'category': hab.category, 'name': hab.name, 'count':hab.count, 'start_date':hab.start_date})
    conn.commit()

# def insert_habit(conn, hab):
#     conn.cursor.execute("""INSERT INTO habitlist(category, name, count) VALUES (:category, :name, :count)""", 
#         {'category': hab.category, 'name': hab.name, 'count':hab.count})
#     conn.commit()
#     #print("1")
#     #print(hab.category)
#     #print(hab.name)
#     #print("2")
#     #print(hab.count)
#     #print("3s")

def get_all_habits(conn, username):
    c = conn.cursor()
    c.execute("SELECT * FROM habitlist WHERE username =:username", {'username': username})
    # typ = type(conn.cursor().fetchall())
    # print(typ)
    return c.fetchall()


def get_first_habit(conn):
    conn.cursor().execute("SELECT * FROM habitlist LIMIT 1")
    # print(conn.cursor().fetchall())
    # return conn.cursor().fetchall()
    return conn.cursor().fetchall()
    

def update_count(count, name, conn):
    conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name", {'count': count, 'name': name})
    conn.commit()

# def check_yes(habit, conn):
#     conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name", {'count': habit.count + 1, 'name': habit.name})
#     conn.commit()
    # here, I want to add one to the count of a habit


# def create_connection(db_file):
#     """ create a database connection to a SQLite database"""
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#         return conn
#     except Error as e:
#         print(e)

# def close_connection(conn):
#     conn.close()

# # c = conn.cursor()
# def create_habit_table(conn):
#     conn.cursor().execute("""CREATE TABLE if not exists habitlist
#                             (
#                             username text,
#                             category text,
#                             name text,
#                             count integer,
#                             start_date date
#                             )"""
#                          )
#     conn.commit()
# # CREATE TABLE if not exists habitlist

# def insert_habit(hab, conn):
#     c = conn.cursor()
#     with conn:
#         c.execute("INSERT INTO habitlist(username, category, name, count, start_date) VALUES (:username, :category, :name, :count, :start_date)",
#         {'username': hab.username, 'category': hab.category, 'name': hab.name, 'count':hab.count, 'start_date':hab.start_date})
#     conn.commit()
#     #print("1")
#     #print(hab.category)
#     #print(hab.name)
#     #print("2")
#     #print(hab.count)
#     #print("3")

# # def insert_habit(conn, hab):
# #     conn.cursor.execute("""INSERT INTO habitlist(category, name, count) VALUES (:category, :name, :count)""", 
# #         {'category': hab.category, 'name': hab.name, 'count':hab.count})
# #     conn.commit()
# #     #print("1")
# #     #print(hab.category)
# #     #print(hab.name)
# #     #print("2")
# #     #print(hab.count)
# #     #print("3")

# # def get_all_habits(conn, username):
# #     conn.cursor().execute("""SELECT * FROM habitlist where count = 0""")
# #     return conn.cursor().fetchall()

# def get_all_habits(conn, username):
#     conn.cursor().execute("SELECT * FROM habitlist WHERE username= :username", {'username': username})
#     return conn.cursor().fetchall()

# def get_first_habit(conn):
#     conn.cursor().execute("SELECT category FROM habitlist LIMIT 1")
#     # print(conn.cursor().fetchall())
#     # return conn.cursor().fetchall()
#     data = conn.cursor().fetchall()
#     print(data)
#     for row in data:
#         print(row)
#         print(type(conn.cursor().fetchall()))

# def update_count(count, name, conn):
#     conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name", {'count': count, 'name': name})
#     conn.commit()

# def check_yes(habit, conn):
#     count = habit.count+1
#     conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name", {'count': count, 'name': habit.name})
#     conn.commit()
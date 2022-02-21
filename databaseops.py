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
                            category text,
                            name text,
                            count integer
                            )"""
                         )
    conn.commit()

def insert_habit(hab, conn):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO habitlist(category, name, count) VALUES (:category, :name, :count)",
        {'category': hab.category, 'name': hab.name, 'count':hab.count})
    conn.commit()
    #print("1")
    #print(hab.category)
    #print(hab.name)
    #print("2")
    #print(hab.count)
    #print("3")

# def insert_habit(conn, hab):
#     conn.cursor.execute("""INSERT INTO habitlist(category, name, count) VALUES (:category, :name, :count)""", 
#         {'category': hab.category, 'name': hab.name, 'count':hab.count})
#     conn.commit()
#     #print("1")
#     #print(hab.category)
#     #print(hab.name)
#     #print("2")
#     #print(hab.count)
#     #print("3")

def get_all_habits(cat, conn):
    conn.cursor().execute("SELECT * FROM habitlist WHERE category=:category", {'category': cat})
    return conn.cursor().fetchall()

def get_first_habit(conn):
    conn.cursor().execute("SELECT category FROM habitlist LIMIT 3")
    # print(conn.cursor().fetchall())
    # return conn.cursor().fetchall()
    data = conn.cursor().fetchall()
    for row in data:
        print(row)

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect('db_file')
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

def close_connection(conn):
    conn.close()

# c = conn.cursor()
def create_habit_table(conn):
    conn.cursor().execute("""CREATE TABLE habitlist
                            (
                            category text,
                            name text
                            )"""
                         )

def insert_habit(hab, conn):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO habitlist VALUES (:category, :name)",
        {'category': hab.category, 'name': hab.name})
    print("1")
    print(hab.category)
    print(hab.name)
    print("2")

def get_all_habits(cat, conn):
    conn.cursor().execute("SELECT * FROM habitlist WHERE category=:category", {'category': cat})
    return conn.cursor().fetchall()

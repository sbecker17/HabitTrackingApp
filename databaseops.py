import sqlite3
from sqlite3 import Error
from datetime import date

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
                            start_date date,
                            last_modified_date date,
                            max_quit_count integer,
                            habit_occurrence text
                            )"""
                         )
    conn.commit()

def insert_habit(hab, conn):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO habitlist(username, category, name, count, start_date, last_modified_date, max_quit_count, habit_occurrence) VALUES (:username, :category, :name, :count, :start_date, :last_modified_date, :max_quit_count, :habit_occurrence)",
        {'username': hab.username, 'category': hab.category, 'name': hab.name, 'count':hab.count, 'start_date':hab.start_date, 'last_modified_date':hab.last_modified_date, 'max_quit_count':hab.max_quit_count, 'habit_occurrence':hab.habit_occurrence})
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

# def get_all_habits(conn, username):
#     c = conn.cursor()
#     c.execute("SELECT * FROM habitlist WHERE username =:username", {'username': username})
#     # typ = type(conn.cursor().fetchall())
#     # print(typ)
#     return c.fetchall()

def get_all_habits(conn, username, category, habit_occurrence):
    c = conn.cursor()
    c.execute("SELECT * FROM habitlist WHERE username =:username AND category =:category AND habit_occurrence =:habit_occurrence", {'username': username, 'category':category, 'habit_occurrence':habit_occurrence})
    # typ = type(conn.cursor().fetchall())
    # print(typ)
    return c.fetchall()

def get_habit_by_name(conn, name):
    c = conn.cursor()
    c.execute("SELECT * FROM habitlist WHERE name =:name", {'name': name})
    return c.fetchall()

def get_first_habit(conn):
    conn.cursor().execute("SELECT * FROM habitlist LIMIT 1")
    # print(conn.cursor().fetchall())
    # return conn.cursor().fetchall()
    return conn.cursor().fetchall()
    
# def update_count(count, name, conn):
#     conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name", {'count': count, 'name': name})
#     conn.commit()

def update_count(count, name, category, conn):
    conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name AND category=:category", {'count': count, 'name': name, 'category':category})
    conn.commit()

def update_name(newname, name, conn):
    conn.cursor().execute("UPDATE habitlist SET name = :newname WHERE name = :name", {'newname': newname, 'name': name})
    conn.commit()

def update_last_mod_date(name, conn):
    conn.cursor().execute("UPDATE habitlist SET last_modified_date = :newdate WHERE name = :name", {'newdate': date.today(), 'name': name})
    conn.commit()

# def check_yes(habit, conn):
#     conn.cursor().execute("UPDATE habitlist SET count = :count WHERE name = :name", {'count': habit.count + 1, 'name': habit.name})
#     conn.commit()
    # here, I want to add one to the count of a habit

def delete_task_db(name, conn):
    conn.cursor().execute("DELETE FROM habitlist WHERE name = :name", {'name': name})
    conn.commit()
import sqlite3

with sqlite3.connect("mytaskr.db") as connection:

    # a cursor object used to execute SQL commands
    c = connection.cursor()

    # create the table
    c.execute("""CREATE TABLE tasks(
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, 
        due_date TEXT NOT NULL, 
        status INTEGER NOT NULL)""")

    # insert some dummy data into the table - task description, date, status
    # status : 1 as open task and 0 as closed task
    c.execute(
        'INSERT INTO tasks (name, due_date, status)'
        'VALUES("Finish this design", "11/07/2017", 1)')

    c.execute(
        'INSERT INTO tasks (name, due_date, status)'
        'VALUES("Finish that app", "18/07/2017", 1)')

    c.execute(
        'INSERT INTO tasks (name, due_date, status)'
        'VALUES("Finish that business plan", "04/07/2017", 0)')

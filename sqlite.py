import sqlite3


def createDatabase():
    sqliteConnection = sqlite3.connect('voltmeter.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    cursor.execute('''CREATE TABLE Log
             (id integer primary key AUTOINCREMENT,
              data text NOT NULL,
              volt real NOT NULL,
              temp real NOT NULL)''')


def insertValues(volt, temp, data):
    try:
        sqliteConnection = sqlite3.connect('voltmeter.db')
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO 'Log'
                          ('volt', 'temp', 'data') 
                          VALUES (?, ?, ?);"""

        data_tuple = (volt, temp, data)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        # print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            # print("The SQLite connection is closed")

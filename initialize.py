# initialize and load data into marathon runs table from MarathonData.csv

import csv, sqlite3, sys, os

with open("MarathonData.csv") as csvfile:
    # connect to the database
    database = sqlite3.connect("marathoner.db", check_same_thread=False)
    cursordb = database.cursor()
    
    # create table to load data for athletes 
    cursordb.execute("""
        CREATE TABLE IF NOT EXISTS marathoners (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            marathon TEXT NOT NULL,
            athlete TEXT NOT NULL DEFAULT "anonymous runner",
            agecategory TEXT,
            km4week REAL NOT NULL,
            speed4week REAL NOT NULL,
            crosstraining TEXT,
            marathontime REAL NOT NULL,
            performancecategory CHARACTER(1))
        """)
    
    # create runs table if not exists
    cursordb.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            rundate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            distance REAL NOT NULL,
            runtime TEXT NOT NULL,
            speed REAL NOT NULL,
            city TEXT,
            weather TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY (user_id) REFERENCES users (id))
    """)
    database.commit()

    result = cursordb.execute("SELECT name FROM sqlite_master")
    tables = result.fetchall()
    newtuple = ("marathoners",)
    if not newtuple in tables:
        # table hasn't created
        sys.exit(1)

    result = cursordb.execute("SELECT marathon FROM marathoners")
    entries = result.fetchone()

    if not entries is None:
        # if table is not empty - delete all entries before loading csv
        cursordb.execute("DELETE FROM TABLE marathoners")
        database.commit()

    # load from file to database
    with open('MarathonData.csv', newline='') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for row in csvreader:
            # insert row in marathoners
            cursordb.execute("""
                INSERT INTO marathoners 
                    (marathon, 
                    athlete,
                    agecategory,
                    km4week,
                    speed4week,
                    crosstraining,
                    marathontime,
                    performancecategory) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,(row[1],row[2],row[3],row[4],row[5],row[6],row[8],row[9],))           
    database.commit()
    database.close()
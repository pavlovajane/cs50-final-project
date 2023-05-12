# initialize and load data into marathon runs table from MarathonData.csv

import csv, sqlite3, sys

with open("MarathonData.csv") as csvfile:
    # connect to the database
    database = sqlite3.connect("marathoner.db", check_same_thread=False)
    cursordb = database.cursor()
    
    # create table to load data for athletes 
    cursordb.execute("""
        CREATE TABLE IF NOT EXISTS marathoners (
            id INTEGER NOT NULL,
            marathon TEXT NOT NULL,
            athlete TEXT NOT NULL DEFAULT "anonymous runner",
            agecategory TEXT,
            km4week REAL NOT NULL,
            speed4week REAL NOT NULL
            crosstraining TEXT,
            marathontime REAL NOT NULL,
            performancecategory CHARACTER(1)
        """)
    
    result = cursordb.execute("SELECT name FROM sqlite_master")
    result.fetchone()

    if not "marathoners" in result.fetchone():
        # table hasn't created
        sys.exit(1)

    result = cursordb.execute("SELECT marathon FROM marathoners")
    if not result.fetchone() is None:
        # if table is not empty - delete all entries before loading csv
        cursordb.execute("DELETE FROM TABLE marathoners")
        database.commit()

    # load from file to database
    with open('MarathonData.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
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
                """,(row["Marathon"],row["Name"],row["Category"],row["km4week"],row["sp4week"],row["CrossTraining"],row["MarathonTime"],row["CATEGORY"],))           
    database.commit()
    database.close()
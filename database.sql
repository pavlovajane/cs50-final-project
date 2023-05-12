CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, hash TEXT NOT NULL);

CREATE TABLE runs (
    id INTEGER NOT NULL,
    rundate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    distance REAL NOT NULL,
    runtime TEXT NOT NULL,
    speed REAL NOT NULL,
    weather TEXT,
    notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id) 
);

CREATE TABLE marathoners (
    id INTEGER NOT NULL,
    marathon TEXT NOT NULL,
    athlete TEXT NOT NULL DEFAULT "anonymous runner",
    agecategory TEXT,
    km4week REAL NOT NULL,
    speed4week REAL NOT NULL
    crosstraining TEXT,
    marathontime REAL NOT NULL,
    performancecategory CHARACTER(1)
)

CREATE INDEX user_id ON runs(user_id);

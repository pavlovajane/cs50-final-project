CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    username TEXT NOT NULL, hash TEXT NOT NULL);

CREATE TABLE runs (
   id INTEGER NOT NULL,
   user_id INTEGER,
    symbol TEXT NOT NULL,
    operation TEXT NOT NULL,
    share INTEGER NOT NULL,
    price REAL NOT NULL,
    amount REAL NOT NULL,
    rundate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    runtime TEXT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id) 
);

CREATE INDEX user_id ON runs(user_id);
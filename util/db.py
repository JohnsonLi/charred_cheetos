import sqlite3
DB_FILE="data/wordsearch.db"

# ===================== Initiate =====================
def createTable():
    """Create all data tables."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE leaderboard (username TEXT, puzzleID INTEGER, time INTEGER)"
    c.execute(command)

    command = "CREATE TABLE puzzle (puzzleID INTEGER, words TEXT)"
    c.execute(command)

    db.commit()
    db.close()

# ===================== User Accounts =====================
def add_user(username, password):
    """Insert credentials for newly registered user into database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    """Authenticate a user attempting to log in."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # user_info = c.execute("SELECT users.username, users.password FROM users WHERE username={} AND password={}".format(username, password))
    for entry in c.execute("SELECT users.username, users.password FROM users"):
        if(entry[0] == username and entry[1] == password):
            db.close()
            return True
    db.close()
    return False

def check_user(username):
    """Check if a username has already been taken when registering."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for entry in c.execute("SELECT users.username FROM users"):
        if(entry[0] == username):
            db.close()
            return True
    db.close()
    return False

# createTable()

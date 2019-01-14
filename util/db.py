import sqlite3
DB_FILE="./data/wordsearch.db"

# ===================== Initiate =====================
def createTable():
    """Create all data tables."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE leaderboard (username TEXT, category INTEGER, level INTEGER, time INTEGER)"
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

# ===================== Leaderboard =====================
def update_lb(user, category, level, time):
    """Update leaderboard with new time."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "SELECT time FROM leaderboard WHERE username = '{}' and category = {} and level = {}".format(user, category, level)
    c.execute(command)
    current_best = c.fetchall()

    # if user has never played the level
    if (current_best == []):
        # print("inserting new value")
        command = "INSERT INTO leaderboard VALUES(?,?,?,?)"
        c.execute(command, (user, category, level, time))
    # the user had played the level
    else:
        # print(current_best[0][0])
        # if new time is faster than current time
        if (time < current_best[0][0]):
            # print("new best for user " + user)
            command = "UPDATE leaderboard SET time={} WHERE username = '{}' and category = {} and level = {}".format(time, user, category, level)
            c.execute(command)

    db.commit()
    db.close()

def load_lb(category, level):
    """Load leaderboard for a level in a category."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "SELECT username, time FROM leaderboard WHERE category = {} and level = {}".format(category, level)
    c.execute(command)
    result = c.fetchall()
    db.close()

    # No score records
    if (result == []):
        return result
    else:
        # a list of [score, username]
        return sort_time(result)

def sort_time(data):
    """Sort time from fastest to slowest for leaderboard display and return up to 10 best times."""
    print(data)

    lb = list()
    for score in data:
        # print(score)
        temp = list()
        temp.append(score[1])
        temp.append(score[0])
        lb.append(temp)

    lb.sort()
    return lb[:10]

# createTable()
def test():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # c.execute("SELECT time FROM leaderboard WHERE level = 3")
    # result = c.fetchall()
    # print(result)

    # update_lb("a", 1, 1, 30)
    # update_lb("b", 1, 2, 30)
    # update_lb("a", 1, 2, 45)
    # update_lb("a", 1, 1, 25)
    # update_lb("c", 1, 1, 100)
    # update_lb("d", 1, 1, 20)
    # update_lb("3", 1, 1, 43)
    #
    # print(load_lb(1,1))
    # print(load_lb(1,2))

    db.close()

# test()

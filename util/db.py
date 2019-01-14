import sqlite3
DB_FILE="./data/wordsearch.db"

# ===================== Initiate =====================
def createTable():
    """Create all data tables."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE personalBest (username TEXT, category TEXT, time INTEGER)"
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

# ===================== Personal Best =====================
def update_pb(user, category, time):
    """Update personal best with new time."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    try:
        command = "SELECT time FROM personalBest WHERE username = '{}' and category = '{}'".format(user, category)
        c.execute(command)
        current_best = c.fetchall()
        # print(current_best[0][0])
        # if new time is faster than current time
        if (time < current_best[0][0]):
            # print("new best for user " + user)
            command = "UPDATE personalBest SET time={} WHERE username = '{}' and category = '{}'".format(time, user, category)
            c.execute(command)

    except:
        # if user has never played the level
        # print("inserting new value " + user + str(time))
        command = "INSERT INTO personalBest VALUES(?,?,?)"
        c.execute(command, (user, category, time))

    db.commit()
    db.close()

def load_pb(username, category):
    """Load personal best for a category."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    try:
        command = "SELECT time FROM personalBest WHERE category = '{}' and username = '{}'".format(category, username)
        c.execute(command)
        result = c.fetchall()
        db.close()
        return result[0][0]
    except:
        return False


# def sort_time(data):
#     """Sort time from fastest to slowest for leaderboard display and return up to 10 best times."""
#     print(data)
#
#     lb = list()
#     for score in data:
#         # print(score)
#         temp = list()
#         temp.append(score[1])
#         temp.append(score[0])
#         lb.append(temp)
#
#     lb.sort()
#     return lb[:10]

# createTable()
def test():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    update_pb("a", "nature", 30)
    update_pb("b", "nature", 30)
    update_pb("a", "food", 45)
    update_pb("a", "nature", 25)
    # update_lb("c", 1, 1, 100)
    # update_lb("d", 1, 1, 20)
    # update_lb("3", 1, 1, 43)
    #
    print(load_pb("a", "nature"))
    print(load_pb("b", "nature"))

    db.close()

# test()

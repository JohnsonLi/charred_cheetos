import os, json

from flask import Flask, request, render_template, \
     flash, session, url_for, redirect

from util import db, puzzle, wordApi

app = Flask(__name__)

app.secret_key = os.urandom(32)

#---------- Main Page ----------
@app.route("/")
def home():
    if 'logged_in' in session:
        return render_template("home.html", logged_in=True, user=session['logged_in'])
    return render_template("home.html", logged_in=False)

#---------- Login/Register----------
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth")
def authenticate():
    if db.auth_user(request.args["user"], request.args["password"]):
        session["logged_in"] = request.args["user"]
        return redirect(url_for("home"))
    else:
        flash("username or password is incorrect")
        return redirect(url_for("login"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/adduser")
def add_user():
    if(not request.args["user"].strip() or not request.args["password"] or not request.args["confirm_password"]):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(db.check_user(request.args["user"])):
        flash("User already exists")
        return redirect(url_for("register"))

    if(request.args["password"] != request.args["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    db.add_user(request.args["user"], request.args["password"])
    session["logged_in"] = request.args["user"]
    return redirect(url_for("home"))

#---------- Logout ----------
@app.route("/logout")
def logout():
    try:
        session.pop("logged_in")
    finally:
        return redirect(url_for("home"))

#---------- Random ----------
@app.route("/random")
def random():
    return redirect(url_for("game", mode="random"))

#---------- Custom ----------
@app.route("/custom")
def custom():
    if 'logged_in' in session:
        return render_template("custom.html", logged_in=True, user=session['logged_in'])
    return render_template("custom.html", logged_in=False)

#---------- Category ----------
@app.route("/categories")
def categories():
    categories = [word.capitalize() for word in wordApi.get_categories()]
    if 'logged_in' in session:
        return render_template("categories.html", categories=categories, logged_in=True, user=session['logged_in'])
    return render_template("categories.html", categories=categories, logged_in=False)

#---------- Game ----------
@app.route("/time")
def recordTime():
    print("attempting to record")
    new = request.args["time"]
    user = session["logged_in"]
    cat = request.args["cat"]
    db.update_pb(user, cat, new)
    print("time added")
    return redirect(url_for("home"))

@app.route("/game")
def game():
    size = 12
    custom_category = ''
    try:
        size = int(request.args['size'])
        custom_category = request.args['category']
    except:
        pass
    try:
    # print("getting category")
        t = db.load_pb(session["logged_in"], custom_category)
    except:
        print("not found")
        t = False
    ws = [['_' for i in range(size)] for i in range(size)]

    # the following if statement does not allow a new mode after the first
    # since there will be a mode ins session
    # not using this might break something
    if 'mode' not in session:
        session['mode'] = request.args["mode"]

    # same with this if
    if 'category' not in session:
        session['custom_category'] = custom_category

    mode = request.args["mode"]
    game = puzzle.create_puzzle(mode, ws, size, custom_category)
    # print(game["words"])
    # print(str(len(game['words'])) + " words added")
    if 'logged_in' in session:
        return render_template("game.html", time=t, board = game["puzzle"], wb = game["words"], logged_in=True, user=session['logged_in'], cat=custom_category)
    return render_template("game.html", time=t, board = game["puzzle"], wb = game["words"], logged_in=False, cat=custom_category)

if __name__ == "__main__":
    app.debug = True
    app.run()

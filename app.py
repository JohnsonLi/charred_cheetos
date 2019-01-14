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
        return render_template("home.html", logged_in=True)
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

#---------- Category ----------
@app.route("/categories")
def categories():
    categories = [word.capitalize() for word in wordApi.get_categories()]
    return render_template("categories.html", categories=categories)

#---------- Levels ----------
@app.route("/game")
def game():
    size = 12
    ws = [['_' for i in range(size)] for i in range(size)]
    mode = request.args["mode"]
    game = puzzle.create_puzzle(mode, ws, size)
    # print(game["words"])
    # print(str(len(game['words'])) + " words added")

    return render_template("game.html", board = game["puzzle"], wb = game["words"])

if __name__ == "__main__":
    app.debug = True
    app.run()

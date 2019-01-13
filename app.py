import os

from flask import Flask, request, render_template, \
     flash, session, url_for, redirect

from util import db, puzzle


app = Flask(__name__)

app.secret_key = os.urandom(32)

#---------- Main Page ----------
@app.route("/")
def home():
    return render_template("home.html")

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
        return redirect(url_for("login"))

#---------- Random ----------
@app.route("/random")
def random():
    return redirect(url_for("game", mode="random"))

#---------- Custom ----------

#---------- Category ----------

#---------- Levels ----------
@app.route("/game")
def game():
    mode = request.args["mode"]
    game = puzzle.create_puzzle(mode)
    # print(game["words"])
    return render_template("game.html", board = game["puzzle"], wb = game["words"])

if __name__ == "__main__":
    app.debug = True
    app.run()

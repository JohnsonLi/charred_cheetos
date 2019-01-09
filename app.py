import os

from flask import Flask, request, render_template, \
     flash, session, url_for, redirect

from util import db, puzzle, word


app = Flask(__name__)

app.secret_key = os.urandom(32)

#---------- Main Page ----------

#---------- Login/Register----------

#---------- Logout ----------

#---------- Random ----------

#---------- Custom ----------

#---------- Category ----------

#---------- Levels ----------



if __name__ == "__main__":
    app.debug = True
    app.run()

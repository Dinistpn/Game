import os
import secrets
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_login import LoginManager
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "POST":
        quant = int(request.form.get("score"))
        level = int(request.form.get("level"))
        if (level == 0) and (quant > 24):
            return apology("Your score is invalid", 400)
        if (level == 1) and (quant > 47):
            return apology("Your score is invalid", 400)
        if (level == 2) and (quant > 114):
            return apology("Your score is invalid", 400)
        if (level == 3) and (quant > 114):
            return apology("Your score is invalid", 400)
        user_id = session["user_id"]
        timeDate = datetime.now()
        userN = db.execute("select username from users WHERE id=:user_id", user_id=user_id)
        userC = userN[0]["username"]
        db.execute("INSERT INTO submissions (username, score, level, time) VALUES (:username, :score, :level, :time)",
        username = userC, score = quant, level = level, time = timeDate)
    return render_template("index.html")

@app.route("/history")
@login_required
def history():
    """maximum score by level"""
    sumT = db.execute("SELECT username, SUM(score) as 'suT' FROM submissions GROUP by username Order by SUM(score) desc limit 5")
    res0 = db.execute("SELECT username, level, score, time FROM submissions Where level = 1 Order by score desc, time asc limit 5")
    res1 = db.execute("SELECT username, level, score, time FROM submissions Where level = 2 Order by score desc, time asc limit 5")
    res2 = db.execute("SELECT username, level, score, time FROM submissions Where level = 3 Order by score desc, time asc limit 5")
    res3 = db.execute("SELECT username, level, score, time FROM submissions Where level = 4 Order by score desc, time asc limit 5")
    """return template"""
    return render_template("history.html", sumT = sumT, res0 = res0, res1 = res1, res2 = res2, res3 = res3)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/music", methods=["GET", "POST"])
@login_required
def music():
    return render_template("music.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        phash = generate_password_hash(password)
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if not len(rows) == 0:
            return apology("This username already exists", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide a password confirmation", 400)
        elif not password == confirmation:
            return apology("the password must match", 400)
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=phash)
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/score", methods=["GET", "POST"])
@login_required
def score():
    """Sell shares of stock"""
    if request.method == "POST":
        quant = 121
        print(quant)
        level = 2
        print(level)
        user_id = session["user_id"]
        userN = db.execute("select username from users WHERE id=:user_id", user_id=user_id)
        userC = userN[0]["username"]
        db.execute("INSERT INTO submissions (username, score, level) VALUES (:username, :score, :level)",
        username = userC, score = quant, level = level)
    return render_template("index.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
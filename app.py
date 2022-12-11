import secrets
import requests
from flask_frozen import Freezer
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from datetime import datetime
from helpers import apology, login_required

# Configure application
app = Flask(__name__)
freezer = Freezer(app)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
 
    return render_template("index.html", username= user_id )
    

        
    


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        user = request.form.get("username")
    
        # Remember which user has logged in
        session["user_id"] = user
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
    s = requests.session()
    # Redirect user to login form
    return redirect("/")


@app.route("/music", methods=["GET", "POST"])
def music():
    return render_template("music.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
    
if __name__ == "__main__":
    freezer.freeze()

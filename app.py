import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import json
import re

# internal imports
from supportfunc import apology, login_required, check_passowrd_validity

# Configure application
app = Flask(__name__)
# Enable debug mode to allow on the fly updates (DISCLAIMER: this is an edu project - not for production)
app.debug = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Connect to the database
database = sqlite3.connect("marathoner.db", check_same_thread=False)
cursordb = database.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show runs done for logged in user"""
    # TODO: implement query for the runs and fix flash_message accrodingly
    return render_template("layout.html", flash_message=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
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
        rows = cursordb.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        user = rows.fetchone()

        # Ensure username exists and password is correct
        if user == None or not check_password_hash(user[2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user[0]
        session["username"] = user[1]

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("passwordRegister"):
            return apology("must provide password", 400)

        # Ensure password was confirmed
        elif not request.form.get("confirmationRegister"):
            return apology("must confirm password", 400)

        # Ensure confirmation matched password
        elif not (request.form.get("passwordRegister") == request.form.get("confirmationRegister")):
            return apology("Password and confirmation don't match", 400)
        
        elif not check_passowrd_validity(request.form.get("passwordRegister")):
            return apology("Password should be at least 8 letters, one digit, one capital letter and one special character", 400)

        username = request.form.get("username")
        password = request.form.get("passwordRegister")

        # Check if such username exists

        if ((cursordb.execute("SELECT * FROM users WHERE username = ?", (username,))).rowcount != -1):
            return apology("Username is taken", 400)

        # Add user to the database
        cursordb.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, generate_password_hash(password),))
        database.commit()
        # TODO: fix execution of queries

        # Query database for username
        rows = cursordb.execute("SELECT id, username FROM users WHERE username = ?", (username,))
        user = rows.fetchone(); 
        # Remember which user has logged in
        session["user_id"] = user[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

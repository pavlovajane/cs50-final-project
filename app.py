import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from datetime import date

# Internal imports
from supportfunctions import apology, login_required, check_passowrd_validity, get_user_runs, \
    convert_to_mph, convert_to_kmh, convert_to_fahrenheit, parse_weather, get_seconds, convert_to_date

# Configure application
app = Flask(__name__)

# Enable debug mode to allow on the fly updates (DISCLAIMER: this is an edu project - not for production)
app.debug = True

# Custom filter
app.jinja_env.filters["convertdate"] = convert_to_date

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    runs = get_user_runs(session["user_id"], cursordb)
    today = date.today()

    flash_message = False
    if len(runs) != 0:
        # Runs are found/tracked
        flash_message = True
    
    return render_template("layout.html", flash_message = flash_message, runs = runs, futuredate = today)


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

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # TODO: implement profile - let user choose btw imperical and metric

    if request.method == "POST":
        
        # Redirect to index
        return redirect("/")
    
    else:
        return render_template("profile.html")

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

@app.route("/addrun", methods=["GET", "POST"])
@login_required
def addrun():
    
    if request.method == "POST":
        
        # Ensure all mandatory fields are subbmitted
        if not request.form.get("date"):
            return apology("must provide date", 400)
        else:
            date = request.form.get("date")
        
        if not request.form.get("distance"):
            return apology("must provide distance", 400)
        else:
            distance = int(request.form.get("distance"))
            if request.form.get("flexSwitchCheckDefault")=="mi":
                # convert to km if mi is chosen
                distance = round(distance*1.60934,2)

        if not request.form.get("city"):
            city = ""
        else:
            city = request.form.get("city")

        if not request.form.get("time"):
            return apology("must provide time", 400)
        else:
            time = request.form.get("time")

        # read weather for latitude and langitude if city provided
        if (request.form.get("lat") and request.form.get("lang")):
            # Request summary weather for the api
            try:
                lat = request.form.get("lat")
                lang = request.form.get("lang")
                
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lang}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&forecast_days=1&start_date={date}&end_date={date}&timezone=auto"
                
                response = requests.get(url)
                response.raise_for_status()
                load = response.json()
                
                weather = parse_weather(load)
            except requests.RequestException:
                # can't load weather
                weather = ""
                pass
        else:
            weather = ""
        # Calculate speed for the run - convert into km per hour
        speed = round((distance*60*60)/get_seconds(time),2)

        # Create a database entry for the run
        # Distance is always stored in metric, converted into imperial on the front-end only
        # Same for the temperatures - stored in Celsius, on user's settings converted into Farenheit
        
        cursordb.execute("""
                        INSERT INTO runs (user_id, rundate, distance, runtime, speed, city, weather) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,(session["user_id"], date, round(distance,2), time, speed, city, weather))
        database.commit()

        # Redirect user to home page
        return redirect("/")
    else:
        # Request is sent via GET - open the quote form
        return render_template("addrun.html")

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify, g
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from datetime import date

# Internal imports
from supportfunctions import handle_exception, login_required, check_passowrd_validity, get_user_runs, \
    parse_weather, get_seconds, convert_to_date, get_user_settings, create_coordinates, calculate_start_date, \
    convert_to_strdate, convert_to_datestr

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

@app.before_request
def before_request():
    # Connect to the database
    if "db" not in g:
        g.db = sqlite3.connect("marathoner.db", check_same_thread=False)
    
    if "crs" not in g:
        g.crs = g.db.cursor()

@app.after_request
def after_request(response):
    # close db connection
    if g.db is not None:
        g.db.close()

    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/<int:runid>', methods=['DELETE'])
@login_required
def delete_run(runid):
    # Delete a run by its id
    if request.method == "DELETE" and runid != None:
        # triggered row deletion
        g.crs.execute("DELETE FROM runs WHERE id = ?", (runid,))
        g.db.commit()
        return jsonify(message="Run deleted")

@app.route("/api/compare", methods=["POST"])
@login_required
def compare_runs():

    if request.method == "POST":
        
        data = request.get_json()
        
        queryruns = """
        SELECT 
        user_id as athlete,
        AVG(distance) as distance
        FROM runs 
        WHERE user_id = ? AND (rundate >= ? AND rundate <= ?) 
        GROUP BY user_id
        """
        
        if data["chartType"]=="Speed":
            # if speed requested - replace distance with speed in the query
            queryruns = queryruns.replace("AVG(distance)", "AVG(speed)")

        if session["imperial"]==1 and data["chartType"]=="Speed":
            # replace speed kmh (default) by mph
            queryruns = queryruns.replace("AVG(speed)","AVG(ROUND(speed/1.609,2))")
        elif session["imperial"]==1 and data["chartType"]=="Distance":
            # replace km (default) by miles
            queryruns = queryruns.replace("AVG(distance)","AVG(ROUND(distance/1.609,2))")
        
        # convert to ISO date for calculations
        datereport = convert_to_datestr(data["datereport"])
        # calculate week from date
        weekbefore = calculate_start_date(datereport)
        # convert date into string to use in the query
        datereport = convert_to_strdate(datereport)

        querymarath = """
        SELECT 
        id as athlete,
        km4week as distance,
        marathontime as time
        FROM marathoners
        ORDER BY distance
        """
        if data["chartType"]=="Speed":
            querymarath = querymarath.replace("km4week as distance", "speed4week as speed")
            querymarath = querymarath.replace("ORDER BY distance","ORDER BY speed")

        if session["imperial"]==1 and data["chartType"]=="Speed":
            # replace speed kmh (default) by mph
            querymarath = querymarath.replace("speed4week as speed","ROUND(speed4week/1.609,2) as speed")
        elif session["imperial"]==1 and data["chartType"]=="Distance":
            # replace km (default) by miles
            querymarath = querymarath.replace("km4week as distance","ROUND(km4week/1.609,2) as distance")

        runs = g.crs.execute(queryruns, (session["user_id"], weekbefore, datereport,))
        userruns = runs.fetchone()
        comps = g.crs.execute(querymarath).fetchall()
        array_runs = create_coordinates(userruns, comps)

        return jsonify(array_runs)

@app.route("/compare", methods=["GET"])
@login_required
def compare():
    
    # check if any runs tracked - if not - don't show the compare chart
    runs = get_user_runs(session["user_id"], g.crs)

    show_chart = False
    if len(runs) != 0:
        # Runs are found/tracked
        show_chart = True

    return render_template("compare.html", show_chart = show_chart, imperial = session["imperial"])

@app.route("/", methods=["GET"])
@login_required
def index():
    # Show runs done for logged in user
    runs = get_user_runs(session["user_id"], g.crs)
    today = date.today()

    flash_message = False
    if len(runs) != 0:
        # Runs are found/tracked
        flash_message = True
    
    return render_template("layout.html", flash_message = flash_message, runs = runs, futuredate = today)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return handle_exception("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return handle_exception("must provide password", 403)

        # Query database for user information
        rows = g.crs.execute("SELECT id, username, imperial, hash FROM users WHERE username = ?", (request.form.get("username"),))
        user = rows.fetchone()

        # Ensure username exists and password is correct
        if user == None or not check_password_hash(user[3], request.form.get("password")):
            return handle_exception("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["imperial"] = user[2]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/settings", methods=["GET", "POST"])
def settings():
  
    if request.method == "POST":
        
        checkbox = request.form.get("flexRadio")
        
        # Update settings
        imperialnew = 1 if checkbox=="imperial" else 0
        g.crs.execute("""
                    UPDATE users 
                    SET imperial = ?
                    WHERE id = ?
                    """, (imperialnew, session["user_id"],))
        g.db.commit()
        session["imperial"] = imperialnew
        # Redirect to index
        return redirect("/")
    
    else:
        # By default site uses metric system
        imperial = get_user_settings(session["user_id"], g.db)

        return render_template("settings.html", imperial = imperial)

@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return handle_exception("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("passwordRegister"):
            return handle_exception("must provide password", 400)

        # Ensure password was confirmed
        elif not request.form.get("confirmationRegister"):
            return handle_exception("must confirm password", 400)

        # Ensure confirmation matched password
        elif not (request.form.get("passwordRegister") == request.form.get("confirmationRegister")):
            return handle_exception("Password and confirmation don't match", 400)
        
        elif not check_passowrd_validity(request.form.get("passwordRegister")):
            return handle_exception("Password should be at least 8 letters, one digit, one capital letter and one special character", 400)

        username = request.form.get("username")
        password = request.form.get("passwordRegister")

        # Check if such username exists
        if ((g.crs.execute("SELECT * FROM users WHERE username = ?", (username,))).rowcount != -1):
            return handle_exception("Username is taken", 400)

        # Add user to the database
        g.crs.execute("""
        INSERT INTO users 
        (username, hash) 
        VALUES (?, ?)
        """, (username, generate_password_hash(password),))
        g.db.commit()

        # Query database for username
        rows = g.crs.execute("SELECT id, username, imperial FROM users WHERE username = ?", (username,))
        user = rows.fetchone(); 
        # Remember which user has logged in
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["imperial"] = user[2]

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
            return handle_exception("must provide date", 400)
        else:
            date = request.form.get("date")
        
        if not request.form.get("distance"):
            return handle_exception("must provide distance", 400)
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
            return handle_exception("must provide time", 400)
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
        
        g.crs.execute("""
                        INSERT INTO runs (user_id, rundate, distance, runtime, speed, city, weather) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,(session["user_id"], date, round(distance,2), time, speed, city, weather))
        g.db.commit()

        # Redirect user to home page
        return redirect("/")
    else:
        # Request is sent via GET - open the quote form
        return render_template("addrun.html", imperial = session["imperial"])

if __name__ == "__main__":
    app.run(ssl_context='adhoc')

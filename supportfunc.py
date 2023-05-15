import os
import requests
import re
import json

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def weather(latitude, longitude):
    """Look up weather summary for given coordinates"""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://forecast9.p.rapidapi.com/rapidapi/forecast/{latitude}/{longitude}/summary/"

        headers = {
	            "X-RapidAPI-Key": api_key,
	            "X-RapidAPI-Host": "forecast9.p.rapidapi.com"
                }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            # TODO change to weather response
            # "name": quote["companyName"],
            # "price": float(quote["latestPrice"]),
            # "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None
    
def check_passowrd_validity(password):
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    match = re.match(password_pattern, password)
    if match==None:
        return False
    else:
        return True

def get_user_runs(userid, db):

    """Show portfolio of stocks if share>0"""
    runs = db.execute("""
                SELECT 
                r.rundate as date,
                r.distance as distance,
                r.runtimte as time,
                r.speed as speed,
                r.weather as weather,
                FROM runs AS r
                INNER JOIN users AS u ON u.id = r.user_id
                WHERE r.user_id = ?
                ORDER BY r.rundate
                """, userid)

    jsonstring = json.dumps(runs)
    runs = json.loads(jsonstring)
import os
import requests
import re
from datetime import datetime

from flask import redirect, render_template, request, session
from functools import wraps


def handle_exception(message, code=400):
    # Return a message if something went wrong
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
                r.id as id,
                r.rundate as date,
                r.distance as distance,
                r.runtime as time,
                r.speed as speed,
                CASE r.city
                    WHEN ""
                        THEN "N/A"
                    ELSE r.city
                END city,
                CASE r.weather
                    WHEN ""
                        THEN "N/A"
                    ELSE r.weather
                END weather,
                u.imperial as imperial
                FROM runs AS r
                INNER JOIN users AS u ON u.id = r.user_id
                WHERE r.user_id = ?
                ORDER BY r.rundate
                """, (userid,))

    runsdict = []
    for row in runs:
        
        if row[7] ==1:
            # Users' settings set to imperial - convert into F, mph and miles
            distance =  round(row[2]/1.60934,2)
            speed = round(convert_to_mph(row[4]),2)
            weather = row[6] 
            if weather != "N/A":
                pos = weather.find(":")
                if pos != -1:
                    ppt = weather.find("Ppt(mm)")
                # weather template is 'Temp max: 00.0, Ppt(mm): 0.0'
                temp = weather[pos+2:ppt-2] 
                # add F sign for farenheit
                ftemp = str(round(convert_to_fahrenheit(float(temp)),2)) + " F" + chr(176)
                weather = weather.replace(temp, ftemp)
        else:
            # if imperial = 0 - then system is metric, default to store in database in metric
            distance =  row[2]
            speed = row[4]
            weather = row[6]  

            if weather != "N/A":
                # add C sign for celsius
                pos = weather.find(":")
                if pos != -1:
                    ppt = weather.find("Ppt(mm)")
                # weather template is 'Temp max: 00.0, Ppt(mm): 0.0'
                temp = weather[pos+2:ppt-2]
                weather = weather.replace(temp, temp + " C" + chr(176))

        dict = {
            "id": row[0],
            "date": row[1],
            "distance": distance,
            "time": row[3],
            "speed": speed,
            "city": row[5],
            "weather": weather
        }
        runsdict.append(dict)

    return runsdict

def get_user_settings(userid, db):
    # get current units setup for the user
    units = db.execute("""
                SELECT
                imperial
                FROM
                users
                WHERE id = ?
                """, (userid,))

    # Return false is no data or imperial (1 == True, 0 == False)
    imperial = units.fetchone()
    return False if imperial is None else (True if imperial[0]==1 else False)


def convert_to_mph(kmh):
    return kmh/1.609

def convert_to_fahrenheit(c):
    return ((c*9/5) + 32)

def parse_weather(json):
    # support function to parse weather reponse json
    temp = json["daily"]["temperature_2m_max"][0]
    ppt = json["daily"]["precipitation_sum"][0]
    str = f"Temp max: {temp}, Ppt(mm): {ppt}"

    return str

def get_seconds(time_str):
    # split in hh, mm, ss
    hh, mm, ss = time_str.split(':')
    return int(hh) * 3600 + int(mm) * 60 + int(ss)

def convert_to_date(datestr):
    return datetime.strptime(datestr, "%Y-%m-%d").date()

def convert_to_dateiso(datelong):
    return datetime.strptime(datelong, "%Y-%m-%dT%H:%M:%S.%fZ").date()

def create_coordinates(runs, compruns):
    # create from sqlite query results sorted dictionary
    array_runs = []
    # compruns = [(id,distance,time),(id,distnace,time),()]
    calculated = False
    for i in compruns:
        # if current distance/speed is more than users distance/speed
        # we need to calculate projected time - AVG(t-1 + t+1)
        # projected time - average of marathoners times with smaller and
        # greater values
        if i[1]>=runs[1] and not calculated:
            if compruns.index(i)>1:
                prev = compruns[compruns.index(i)-1][2]
            else:
                prev = 0
            if len(compruns) >= (compruns.index(i)+1):
                next = compruns[compruns.index(i)+1][2]
            else:
                next = i[2]
            if not prev==0:               
                projected_time = round((prev + next)/2,2)
            else:
                # if prev result is 0 - projected time is not average but remaining time
                projected_time = next
            calculated = True

            add_list_entry(array_runs, projected_time, runs[1], 1)

        add_list_entry(array_runs, i[2], i[1])

    return array_runs

def add_list_entry(arr, time, dist_speed, user = 0):
    dictentry = {
                "x": dist_speed,
                "y": time
            }
    
    if user == 1:
        dictentry["user"] = 1
    
    arr.append(dictentry)
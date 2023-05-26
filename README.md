# You are a marathoner
#### Video Demo:  <URL HERE>

#### Description  
##### About the CS50x course
  A graduation project from [Harvard Online CS50x course](https://cs50.harvard.edu/x/2023/). The course starts with a traditional but omnipresent language **C** that underlies today’s newer languages. The course then transitions to **Python**, a higher-level language that the learner will understand all the more because of **C**. Toward term’s end, the course introduces **SQL**, via which the learner can store data in databases, along with **HTML**, **CSS**, and **JavaScript**, via which the learner can create web and mobile apps alike. The course culminates in a **final project**.
  
##### About the project
  The project is called "You are a marathoner!". This is a crisp web app built with **Python**, **Flask**, **Jinja**, **HTML**, **CSS**, and with a grain of **Javascript**. This is a simple but effective application that helps you to track your runs. Especially if you are having a marathon in mind. It helps you to compare your 4-week results with a database of actual marathoners (based on a dataset kindly provided by [Andrea Girardi at Kaggle](https://www.kaggle.com/datasets/girardi69/marathon-time-predictions)).

##### Value proposition
 Running a marathon ain't no joke! It is a challenge where this web application can give you some support. Just track your runs and you can always compare any of your running weeks with the other athletes. 

 The source dataset from Kaggle has real marathon times for athletes running the Prague marathon and the training results before (distance and speed of runs before the X-day). 

 Check if you are falling behind most of the runners and adjust your training routine accordingly. Celebrate success if you have a good projected time and keep going!

##### Features
  * Users can register using their name and specifying their password
    1. Password is evaluated towards certain rules (e.g. number of symbols, special characters etc.)
    2. User is notified in real-time if their password is aligned with the rules
  * Logged in user's name is shown on the right of the menu
    1. If a user isn't logged in, they can't access any functionality except for login and registration
    2. If wrong user name or password are given - the app will show a confused penguin with clarification what went wrong
  * User can choose their default metrics settings - imperial (mi, mph, Fahrenheit) or metric (km, kmh, Celsius)
    1. Settings will be saved for future use
    2. Settings are shown near logged user's name
    3. Settings are applied to recalculate all values on the fly (temperature, distance, and speed)
    4. Settings are shown in the table headers for runs and axis labels for the runs compare chart
  * Add run functionality enriched with the google places API - user can start typing the place of run and it will
  auto-complete from the google places database
    1. If the user added a place of a run (see above) - weather API will be triggered to receive the maximum temperature for the date of the run and precipitation for the day of the run
    2. User can enter a run for a future date. The system will make a record and load forecast for the record (if a place is entered). The future date runs will be highlighted in pink in a runs table to indicate possible faulty data to the user
    3. User can choose between adding the run distance in miles or in kilometers. By default the switcher is aligned with user's settings
  * User can delete any previously recorded run on the main page. The system will ask to confirm the deletion
  * Compare shows user's results for 7 weeks before given date on a scatter chart with athletes from Prague's marathon
    1. By default the date is set to current date
    2. The report will check for results from previous 7 days
    3. The date of the report can be changed to any date by date picker
    4. User's results are represented as a slighlty bigger dot
    5. If user has no results for the given date or 7 days before - no bigger dot will be visible
    6. The chart will show the exact data on hover - (distance/speed, time, dot size - misc.)  

##### Design choices and details
  * Flask is chosen as a back-end framework. File structure follows Flask's standard structure:
    1. All HTML templates (with Jinja expressions) located in templates/
    2. CSS, Javascript, and favicon picture are located in static/
    3. Database.sql file has queries (some) used in code to extract data
  * Pyhton files are app.py, supportfunctions.py and initialize.py
    1. app.py has the main logic, routing to diffrernt template HTMLs
    2. supportfunctions.py has supplemental logic like converting strings to date, dates to different formats, building chart array data, and similar
    3. initialize.py has logic for creating a database (disclaimer) - it was already created and data from CSV loaded. But steps could be reproduced from scratch using initialize.py. Marathon data was downloaded from Kaggle and saved in MarathonData.csv 
  * requirements.txt has package details for dependencies
  * I had an idea to create it pure command-line (with [ASCII art](https://en.wikipedia.org/wiki/ASCII_art) and stuff) as I tend to focus on back-end development. But I decided I give front-end a go too, I always was supportive of T-shape idea. So here we are - Python - 48.9%, HTML - 29.0%, JavaScript - 16.1%, CSS - 6.0% 
  
##### Future developments/ next releases
  * Improved authorization - e.g. via social platforms 
  * Register by e-mail instead of name with e-mail validation
  * More security of user's account - e.g. password restoration and change
  * Filtering and/or sorting in runs
  * More user-friendly adding of runs
  * Add user's personal info - age (to compare with age group), gender (to compare with age-gender group)
  * Implement a training plan creation - should take into account average km per week, days to run, plan start date
  * Implement plan adaptation to recorded run - check the number of done/planned runs and ask about adjustment
  * Change the algorithm of the time prediction to a more sophisticated one
  * Add unit and integration test with BDD
  * Containarize application with Docker
  * Host application on Amazon using free 1-year tier
  
[![memecomplete](https://api.memegen.link/images/bihw/it_ain't_much/but_it_is_the_honest_final_work.jpg?token=g2pd8jp936gb8xraaswq)](https://memecomplete.com/share/images/bihw/it_ain't_much/but_it_is_the_honest_final_work.jpg?token=g2pd8jp936gb8xraaswq)

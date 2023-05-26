# You are a marathoner
#### Video Demo:  <URL HERE>

#### Description  
##### About the CS50x course
  A graduation project from [Harvard Online CS50x course](https://cs50.harvard.edu/x/2023/). The course starts with a traditional but omnipresent language **C** that underlies today’s newer languages. The course then transitions to **Python**, a higher-level language that the learner will understand all the more because of **C**. Toward term’s end, the course introduces **SQL**, via which the learner can store data in databases, along with **HTML**, **CSS**, and **JavaScript**, via which the learner can create web and mobile apps alike. Course culminates in a **final project**.
  
##### About the project
  The project is called "You are a marathoner!". This is a crisp web app built with **Python**, **Flask**, **Jinja**, **HTML**, **CSS** and with a grain of **Javascript**. This is a simple but effective application which helps you to track your runs. Especially if you are having a marathon in mind. It helps you to compare your 4 week results with a database of actual marathoners (based on a dataset kindly provided by [Andrea Girardi at Kaggle](https://www.kaggle.com/datasets/girardi69/marathon-time-predictions)).

###### Features
  * User can register using their name and specifying their password
    1. Password is evaluated towards certain rules (e.g. number of symbols, special characters etc.)
    2. User is notified in real time if their password is aligned with the rules
  * Logged in user's name is shown on the right of the menu
  * User can choose their default metrics settings - imperial (mi, mph, Farenheit) or metric (km, kmh, Celsius)
    1. Settings will be saved for future use
    2. Settings are shown near logged user's name
    3. Settings are applied to recalculate all values on the fly (temperature, distance and speed)
    4. Settings are shows in the table headers for runs and in axis lebels for runs compare chart
  * Add run functionality enriched with google places API - user can start typing the place of run and it will
  auto-complete from google places database
  * If user added a place of run (see above) - weather API will be triggered to receive maximum temperature for the date of run and precipitation for the day of run
  * TBC

###### Design choices and details
  * Flask is chosen as a back-end framework. File structure follows Flask's standard structure:
    1. All html templates (with Jinja expressions) located in templates
    2. CSS, Javascript and favicon picture are located in static/
    3. Database.sql file has queries (some) used in code to extract data
  * Pyhton files are app.py, supportfunctions.py and initialize.py
  
###### Future developments
  * Improved authorizathion - e.g. via social platforms 
  * Register by e-mail instead of name with e-mail validation
  * More security of user's account - e.g. password restore and change
  * Filtering and/or sorting in runs
  * More user friendly adding of runs
  * Add user's personal info - age (to compare with age group), gender (to compare with age-gender group)
  * Implement a training plan creation - should take into account average km per week, days to run, plan start date
  * Implement plan adaptaion to recorded run - check the number of done/planned runs and ask about adjustment
  * Change algorithm of the time prediction to more sophisticated one
  * Add unit and integration test with BDD
  * Containarize application with Docker
  * Host application on Amazon using free 1-year tier
  
[![memecomplete](https://api.memegen.link/images/bihw/it_ain't_much/but_it_is_the_honest_final_work.jpg?token=g2pd8jp936gb8xraaswq)](https://memecomplete.com/share/images/bihw/it_ain't_much/but_it_is_the_honest_final_work.jpg?token=g2pd8jp936gb8xraaswq)

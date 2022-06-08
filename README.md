
# MeTrack

An expense tracker for personal use. 

## What is MeTrack?
MeTrack is built with the flask framework. It uses Flask-Login for user management, allowing useres to sign
up and have a personal profile where they can track their expenses. It is a full CRUD app, and usere
can add, edit end delete their expenses. The profile also display users charts of their 
expenses by months and by categories, to help them understand where their money goes.

## Technologies
* Front-end: Bootstrap, Charts.js and DataTables.
* Back-end: Flask
* DB: SQLite
* Hosting: Heroku
* Tests: Pytest

## How can you use it?
 Simply go to https://me-track.herokuapp.com. Sign up and start
 adding expenses in your profile.

 ## How can you run it locally?
 1. Clone the repo  
`git clone https://github.com/ShayNoa/MeTrack.git`

2. Create your virtual enviornment 
 `python -m venv env`

 3. Activate your environment:
 `source evn/bin/activate`

 4. Install the dependencies:
 `pip install -r ruqirements.txt`

 5. Create the db:
 `python <br />
 from Tracker import db  <br />
 db.create_all()  <br />
 exit()`

6. Run flask app using `flask run`

The app should now be available on localhost, port 5000.




 

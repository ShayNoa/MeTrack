
# MeTrack
An expense tracker for personal use. 

## What is MeTrack?
MeTrack is built with the flask framework. It uses Flask-Login for user management, allowing useres to sign
up and have a personal profile where they can track their expenses. It is a full CRUD app, and usere
can add, edit and delete their expenses. The profile also display users charts of their 
expenses by months and by categories to help them understand where their money goes.

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
```
git clone https://github.com/ShayNoa/MeTrack.git
```

2. Create your virtual enviornment 
 ```
 python -m venv env
 ```

 3. Activate your environment:
 ```
 source env/bin/activate
 ```
 4. Install the dependencies:
 ```
 pip install -r requirements.txt
 ```

 ```
6. Run flask app typing
```
flask run
```

The app now will be available on localhost, port 5000.








 

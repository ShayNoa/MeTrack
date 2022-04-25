from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'c1bf717b3bc136aebebc' # secret key procced in hidden_tag in templated, required for login system.
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login' # when accesing a page requiring login, if user not loged in, login_view is the page
                                       # he'll be redirected to - in this case, the login route.
    login_manager.login_message_category = 'info' # enable editing the login required message that appears to the user
    bcrypt.init_app(app) # ?
    
    return app

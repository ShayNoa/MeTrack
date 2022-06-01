from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from Tracker.config import BaseConfig

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "info"
bcrypt = Bcrypt()


def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from Tracker.expenses.routes import expenses
    from Tracker.main.routes import main
    from Tracker.users.routes import users
    app.register_blueprint(expenses)
    app.register_blueprint(main)
    app.register_blueprint(users)
    
    return app

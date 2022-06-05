from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask_login import current_user, login_user, logout_user
# from werkzeug.exceptions import NotFound

from Tracker import bcrypt
from Tracker.users.forms import LoginForm, RegistrationForm
from Tracker.models import User

users = Blueprint('users', __name__)

# @app.errorhandler(NotFound)
# def handle_bad_request(e):
#     return render_template("404.html"), 400


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("expenses.profile"))

    form = RegistrationForm()
    if form.validate_on_submit():
        User.create(form)
        flash(f"Account created for {form.username.data}", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("expenses.profile"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.by_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_route = request.args.get("next")
            if next_route:
                return redirect(next_route)
            else:
                return redirect(url_for("expenses.profile"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))

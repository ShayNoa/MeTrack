from flask_wtf import FlaskForm
from Tracker.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, Length, Optional, Regexp,
                                equal_to)
from wtforms_alchemy import ModelForm, Unique


class RegistrationForm(FlaskForm, ModelForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=25),
            Unique(
                User.username,
                message="Username is taken. Please choose a different one",
            ),
        ],
    )
    first_name = StringField(
        "First name", validators=[Optional(), Length(min=2, max=30)]
    )
    last_name = StringField("Last name", validators=[Optional(), Length(min=2, max=30)])
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Unique(
                User.email, message="This email is taken. Please choose a different one"
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=30),
            Regexp(
                regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$",
                message="Must contain at least one uppercase letter, one lowercase letter and one number",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm password", validators=[DataRequired(), equal_to("password")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=30)]
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

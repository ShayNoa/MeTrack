from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, FloatField, PasswordField,
                     StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, InputRequired, Length,
                                Optional, Regexp, equal_to)
from wtforms_alchemy import ModelForm, Unique
from wtforms_sqlalchemy.fields import QuerySelectField

from Tracker.models import Category, User


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


# for the query factory in QuerySelectField, not sure it shold be here.
def category_query():
    return Category.query.order_by(Category.name.asc()).all()


class ExpenseForm(FlaskForm):
    name = StringField("Description", validators=[DataRequired()])
    cost = FloatField(
        "Cost", validators=[InputRequired(message="Please enter only numbers")]
    )
    category = QuerySelectField(
        query_factory=category_query,
        allow_blank=True,
        blank_text="Select Category",
        get_label="name",
        validators=[DataRequired()],
    )
    date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Save")

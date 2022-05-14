from flask_wtf import FlaskForm
from wtforms import (BooleanField, FloatField, PasswordField,
                     StringField, SubmitField, DateField)
from wtforms.validators import (DataRequired, Email, Length, ValidationError, equal_to, Optional, InputRequired)
from wtforms_sqlalchemy.fields import QuerySelectField

from Tracker.models import Category, User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    first_name = StringField('First name', validators=[Optional(), Length(min=2, max=30)]) # make it optional
    last_name = StringField('Last name', validators=[Optional(), Length(min=2, max=30)]) # make it optional
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), equal_to('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()        
        if user:
            raise ValidationError('This username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('This email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=30)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


def category_query():
    return Category.query.order_by(Category.name.asc()).all()


class ExpenseForm(FlaskForm):
    name = StringField('Description', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[InputRequired(message='Please enter only numbers')])
    category = QuerySelectField(
        query_factory=category_query, 
        allow_blank=True, blank_text='Select Category', 
        get_label='name', validators=[DataRequired()]
        )
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Save')


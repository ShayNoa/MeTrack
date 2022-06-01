from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired
                               
from wtforms_sqlalchemy.fields import QuerySelectField
from Tracker.models import Category


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
from Tracker.models import User, Expense, Category
import datetime
from Tracker import db


def test_new_expense(init_database):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """
    expense = Expense(
        name='test_expense',
        cost=22.2,
        date=datetime.date(2022, 6, 2),
        category_id=1,
        user_id=1
    )
    assert expense.name == 'test_expense'
    assert expense.cost == 22.2 
    assert expense.date == datetime.date(2022, 6, 2)
    assert expense.category_id == 1


def test_new_user(init_database):
    new_user = User(
        username='TestUser',
        first_name='Test',
        last_name='User',
        email='testuser@gmail.com',
        password='Thisispassword'
    )
    assert new_user.password != 'Thisispassword'
    assert new_user.first_name == 'Test'
    assert new_user.email == 'testuser@gmail.com'


def test_new_category(init_database):
    new_category = Category(
        name='Education'
    )
    assert new_category.name == 'Education'
    
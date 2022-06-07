from Tracker.models import User, Expense, Category
import datetime
from Tracker import db


def test_new_expense(init_database):
    expense = Expense(
        name='test expense',
        cost=22.2,
        date=datetime.date(2022, 6, 2),
        category_id=1,
        user_id=1
    )
    db.session.add(expense)
    db.session.commit()
    assert expense.name == 'test expense'
    assert expense.cost == 22.2 
    assert expense.date == datetime.date(2022, 6, 2)
    assert expense.category_id == 1
    assert expense.__repr__() == f"{1}, test expense, {22.2}, 2022-06-02"


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
    assert new_category.__repr__() == 'Education'
    
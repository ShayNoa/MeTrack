from flask_login import current_user
import datetime
from Tracker.models import User, Expense, Category


def test_logged_user_register(logged_in_user):  # added now
    response = logged_in_user.get('/register', follow_redirects=True)
    assert response.status_code == 200
    assert b'Add Expense' in response.data


def test_logged_user_login(logged_in_user):  # added now
    response = logged_in_user.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert b'Add Expense' in response.data


def test_profile(logged_in_user):
    response = logged_in_user.get('/profile')

    assert response.status_code == 200
    assert b'Add Expense' in response.data
    assert b'Profile' in response.data
    assert b'Description' in response.data
    assert current_user.id == 1
    assert current_user.username == 'testuser'


def test_add_expense(logged_in_user):
    response = logged_in_user.post(
        '/profile',
        follow_redirects=True,
        data=dict(
            name='test expense',
            cost=12,
            category=1,
            date=datetime.date(2022, 6, 5),
            submit=True
        )
    )

    assert response.status_code == 200
    assert current_user.username == 'testuser'
    assert b"testuser's Expenses" in response.data
    assert b'Actions' in response.data 
    assert b'test expense added' in response.data
    assert len(Expense.query.all()) == 1
    assert Expense.query.get(1).name == 'test expense'
    assert Expense.query.get(1).category_id == 1
    assert Category.query.get(1).name == 'Education'
    assert Expense.query.get(1).user_id == current_user.id


def test_edit_expense(logged_in_user):
    response = logged_in_user.get('/edit_expense/1')
    assert response.status_code == 200
    assert b'Edit Expense' in response.data
    assert b'test expense' in response.data

    response = logged_in_user.post(
        '/edit_expense/1',
        data=dict(
            name='test expense',
            cost=22,
            category=2,
            date=datetime.date(2022, 6, 5),
            submit=True
        ),
        follow_redirects=True)
    assert response.status_code == 200
    assert b'test expense changes saved' in response.data
    assert b'Add Expense' in response.data
    assert Expense.query.get(1).category_id == 2
    assert Category.query.get(2).name == 'Fitness'
    assert Expense.query.get(1).user_id == current_user.id


def test_invalid_id_delete_expense(logged_in_user):
    response = logged_in_user.get('/edit_expense/2', follow_redirects=True)
    assert response.status_code == 404


def test_delete_id_expense(logged_in_user):
    response = logged_in_user.get('/delete_expense/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'test expense has been deleted' in response.data
    assert b'Add Expense' in response.data


def test_invalid_id_delete_expense(logged_in_user):
    response = logged_in_user.get('/delete_expense/2', follow_redirects=True)
    assert response.status_code == 404



    







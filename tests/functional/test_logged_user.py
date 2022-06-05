import pytest
from flask_login import current_user
import datetime
from Tracker.models import User, Expense, Category
from Tracker import db


def test_profile(logged_in_user):
    response = logged_in_user.get('/profile')

    assert response.status_code == 200
    assert b'Add Expense' in response.data
    assert b'Profile' in response.data
    assert b'Description' in response.data
    assert current_user.id == 1
    assert current_user.username == 'testuser'


# def test_add_expense(logged_in_user):
#     education = Category.query.first()
#     response = logged_in_user.post(
#         '/profile',
#         follow_redirects=True,
#         data=dict(
#             name='test expense',
#             cost=12,
#             category=education,
#             date=datetime.date(2022, 6, 5),
#             submit=True
#         )
#     )
#     assert b"testuser's Expenses" in response.data
#     assert response.status_code == 200
#     assert b'test expense' in response.data
#     assert current_user.username == 'testuser'


    



import pytest
from flask_login import FlaskLoginClient
from Tracker import create_app, db
from Tracker.config import TestConfig
from Tracker.models import Category, User
from pathlib import Path

@pytest.fixture(scope='session')
def test_app():
    flask_app = create_app(config_class=TestConfig)
    yield flask_app


@pytest.fixture(scope='module')
def test_client(test_app):
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def new_user():
    user1 = User(
        username='testuser',
        first_name='test',
        last_name='user',
        email='testuser@gmail.com',
        password='Tuser1234'
    )
    return user1


@pytest.fixture(scope='module')
def new_user2():
    user2 = User(
        username='testuser2',
        first_name='test',
        last_name='user',
        email='testuser2@gmail.com',
        password='Tuser1234'
    )
    return user2


@pytest.fixture(scope='module')
def init_database(test_client, new_user):
    db.create_all()
    db.session.add(new_user)
    db.session.commit()
    yield db
    db.drop_all()


@pytest.fixture(scope='module')
def logged_in_user(new_user, test_app):
    with test_app.app_context():
        db.create_all(app=test_app)
        db.session.add(new_user)
        db.session.commit()

        categories = ["Education", "Fitness", "Groceries"]
        for name in categories:
            category = Category(name=name)
            db.session.add(category)
        db.session.commit()
       
        test_app.test_client_class = FlaskLoginClient
        with test_app.test_client(user=new_user) as testing_client:
            yield testing_client
      
        db.drop_all()


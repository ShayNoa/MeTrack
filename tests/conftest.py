import pytest
from Tracker import create_app, db
from Tracker.models import User, Category, Expense
from Tracker.config import TestConfig
from flask_login import FlaskLoginClient


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class=TestConfig)
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()
    user1 = User(
        username='testuser',
        first_name='test',
        last_name='user',
        email='testuser@gmail.com',
        password='Tuser1234'
    )
    db.session.add(user1)
    db.session.commit()
    yield db

    db.drop_all()


@pytest.fixture(scope='module')
def logged_in_user():
    flask_app = create_app(config_class=TestConfig)

    with flask_app.app_context():
        db.create_all(app=flask_app)
        test_user = User(
            username='testuser',
            first_name='test',
            last_name='user',
            email='testuser@gmail.com',
            password='Tuser1234'
        )
        db.session.add(test_user)
        db.session.commit()

        categories = ["Education", "Fitness", "Groceries"]
        for name in categories:
            category = Category(name=name)
            db.session.add(category)
        db.session.commit()
        
        flask_app.test_client_class = FlaskLoginClient
        with flask_app.test_client(user=test_user) as testing_client:
            yield testing_client
        db.drop_all()


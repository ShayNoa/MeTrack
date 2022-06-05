import pytest
    

def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_homepage(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Register now' in response.data
    assert b'With so many' in response.data


def test_valid_login_and_logout(test_client, init_database):
    response = test_client.post('/login',
                                data=dict(email='testuser@gmail.com', password='Tuser1234'),
                                follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Add Expense' in response.data
    assert b'Logout' in response.data
    assert b'Profile' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Remember me' in response.data
    assert b'Profile' not in response.data
    assert b'Logout' not in response.data


def test_invalid_login(test_client, init_database):
    response = test_client.post(
        '/login',
        data={'email': 'testuser@gmail.com', 'password': 'Wrongpassword'},
        follow_redirects=True
        )
    assert response.status_code == 200
    assert b'Login Unsuccessful' in response.data
    assert b'Profile' not in response.data
    assert b'Logout' not in response.data


def test_valid_registration(test_client, init_database):
    response = test_client.post(
        '/register',
        data={
            'username': 'TestUser2',
            'email': 'testuser2@gmail.com',
            'password': 'TestUser1234',
            'confirm_password': 'TestUser1234',
            'submit': True
        },
        follow_redirects=True
        )
    assert response.status_code == 200
    assert b'Account created for TestUser2' in response.data
    assert b'Log In' in response.data 


test_data = [
    (
        {
            'username': 'TestUser2',
            'email': 'testuser2@gmail.com',
            'password': 'pw123456',
            'confirm_password': 'pw123456',
            'submit': True
        },
        b'Must contain at least one uppercase letter'
    ),
    (
        {
            'username': 'TestUser2',
            'email': 'testuser2@gmail.com',
            'password': 'pw123456',
            'confirm_password': 'pw123455',
            'submit': True
        },
        b'Field must be equal to password'
    ),
    (
        {
            'username': 'TestUser2',
            'email': 'testuser2@gmail',
            'password': 'pw123456',
            'confirm_password': 'pw123455',
            'submit': True
        },
        b'Invalid email address.'
    ),
]


@pytest.mark.parametrize('data_input, error_message', test_data)
def test_invalid_registartion(
    test_client, init_database, data_input, error_message
):
    response = test_client.post(
        '/register',
        data=data_input,
        follow_redirects=True
        )
    assert response.status_code == 200
    assert error_message in response.data
    assert b'Join Today' in response.data


def test_unique_email_and_username(test_client, init_database):
    response = test_client.post('/register',
        data={
            'username': 'TestUser2',
            'email': 'testuser2@gmail.com',
            'password': 'TestUser1234',
            'confirm_password': 'TestUser1234',
            'submit': True
        },
        follow_redirects=True
    )

    response = test_client.post('/register',
        data={
            'username': 'TestUser2',
            'email': 'testuser2@gmail.com',
            'password': 'TestUser1234',
            'confirm_password': 'TestUser1234',
            'submit': True
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Username is taken. Please choose a different one' in response.data
    assert b'email is taken. Please choose a different one' in response.data
    assert b'Join Today' in response.data
    assert b'Profile' not in response.data
    



    
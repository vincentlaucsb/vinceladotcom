import os
import tempfile
import pytest
import vinceladotcom as site

@pytest.fixture(scope='function')
def client(request):
    print("Setting up")
    application = site.application
    application.config['TESTING'] = True
    db_file, application.config['DATABASE'] = tempfile.mkstemp()
    
    from vinceladotcom.database import db_init
    db_init()

    with application.app_context():
        # Set up admin user
        site.auth.new_user(
            name='admin',
            password='password',
            full_name='Admin Adminson',
            email='adminator@wh.gov',
            is_admin=True
        )
        application.config['USERNAME'] = 'admin'
        application.config['PASSWORD'] = 'password'
    
    client = application.test_client()

    def close():
        print("Closing")
        site.database.db.close()
        os.close(db_file)
        os.unlink(application.config['DATABASE'])

    request.addfinalizer(close)

    return client

def login(test_client, username, password):
    return test_client.post('/login', data=dict(
        name=username,
        password=password
    ), follow_redirects=True)
    
@pytest.fixture(scope='function')
def admin_client(client):
    login(client, 'admin', 'password')
    return client

def logout(test_client):
    return test_client.get('/logout', follow_redirects=True)

def test_login_logout(client):
    ''' Test logging in and logging out '''
    
    rv = login(client,
              site.application.config['USERNAME'],
              site.application.config['PASSWORD'])
    assert b'Hi, and welcome to my online home!' in rv.data
    
    rv = logout(client)
    assert b'You have been logged out' in rv.data
import os
import tempfile
import pytest
import vinceladotcom as site

@pytest.fixture
def client():
    db_file, site.application.config['DATABASE'] = tempfile.mkstemp()
    site.application.config['TESTING'] = True
    
    with site.application.app_context():
        # Set up admin user
        site.auth.new_user(
            name='admin',
            password='password',
            full_name='Admin Adminson',
            email='adminator@wh.gov',
            is_admin=True
        )
        site.application.config['USERNAME'] = 'admin'
        site.application.config['PASSWORD'] = 'password'
    
    client = site.application.test_client()
        
    yield client
    
    os.close(db_file)
    os.unlink(site.application.config['DATABASE'])

def login(client, username, password):
    return client.post('/login', data=dict(
        name=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)
    
def test_login_logout(client):
    ''' Test logging in and logging out '''
    
    rv = login(
        client, 
        site.application.config['USERNAME'],
        site.application.config['PASSWORD']
    )
    assert b'Hi, and welcome to my online home!' in rv.data
    
    rv = logout(client)
    assert b'You have been logged out' in rv.data
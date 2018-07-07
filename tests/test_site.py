import os
import tempfile
import pytest
import vinceladotcom as site

@pytest.fixture
def client():
    db_file, site.app.config['DATABASE'] = tempfile.mkstemp()
    site.app.config['TESTING'] = True
    
    with site.app.app_context():
        site.init_db()
        
        # Set up admin user
        site.auth.new_user(
            name='admin',
            password='password',
            email='adminator@wh.gov',
            is_admin=True
        )
        site.app.config['USERNAME'] = 'admin'
        site.app.config['PASSWORD'] = 'password'
    
    client = site.app.test_client()
        
    yield client
    
    os.close(db_file)
    os.unlink(site.app.config['DATABASE'])

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
        site.app.config['USERNAME'],
        site.app.config['PASSWORD']
    )
    assert b'Hi, and welcome to my online home!' in rv.data
    
    rv = logout(client)
    assert b'You have been logged out' in rv.data
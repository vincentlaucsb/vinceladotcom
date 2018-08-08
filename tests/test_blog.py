from .test_site import client, admin_client, login, logout, site

def test_make_post(admin_client):
    ''' Make sure that posting new entries works properly '''
    rv = admin_client.post('/blog/', data=dict(
        page_title='Why We Should Nuke Canada',
        tags='america, canada, freedom',
        content='Because they drink syrup',
        submit=True
    ), follow_redirects=True)

    rv = admin_client.get('/blog/why-we-should-nuke-canada', follow_redirects=True)
    assert b'Because they drink syrup' in rv.data

    ''' Make sure that blog lists work properly '''
    for i in ['america', 'canada', 'freedom']:
        rv = admin_client.get('/blog/tags/{}'.format(i))
        assert b'<a href="/blog/why-we-should-nuke-canada">Why We Should Nuke Canada</a>' in rv.data
        
    # Make sure this doesn't appear in other unrelated tags
    for i in ['prius', 'civic', 'corolla']:
        rv = admin_client.get('/blog/tags/{}'.format(i))
        assert b'<a href="/blog/why-we-should-nuke-canada">Why We Should Nuke Canada</a>' not in rv.data

def test_get_post(admin_client):
    ''' Make sure that getting blog posts as a guest works '''

    rv = admin_client.post('/blog/', data=dict(
        page_title='Why We Should Nuke Canada',
        tags='america, canada, freedom',
        content='Because they drink syrup',
        submit=True
    ), follow_redirects=True)

    assert b'Because they drink syrup' in rv.data

    logout(admin_client)

    rv = admin_client.get('/blog/why-we-should-nuke-canada', follow_redirects=True)
    assert b'Because they drink syrup' in rv.data
    assert b'[edit]' not in rv.data
from ..config import *
from .. import database

def make_router(page):
    ''' page: Database object '''

    class PageRouter(object):
        def __init__(self, url):
            self.url = url
            
        def __call__(self):
            # Pull content from database
            page = database.Page.get(database.Page.url == self.url)
            if not page.template:
                page.template = 'base_page.html'
            
            return render_template(
                page.template,
                page = page,
                **PAGE_GLOBALS
            )
        
    router = PageRouter(page.url)
    router.__name__ = page.url
    return router
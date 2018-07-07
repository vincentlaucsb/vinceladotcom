from peewee import *
from playhouse.pool import PooledSqliteDatabase
import datetime

db = PooledSqliteDatabase(
    database='vince.sqlite'
)

def title_to_url(title):
    ret = title.lower()
    ret = ret.replace(' ', '-')
    return ret

class BaseModel(Model):
    class Meta:
        database = db
        
class BasePage(BaseModel):
    title = CharField(200, unique=True)
    tags = TextField(default='[]')
    deleted = BooleanField(default=False)

class BlogPost(BasePage):
    author = CharField(200)
    created = DateField(default=datetime.datetime.now)
    modified = DateField(default=datetime.datetime.now)
    draft = BooleanField(default=True)
    content = TextField()
    urls = {} # Mapping of titles to blog IDs
    
    def __init__(self, *args, **kwargs):
        super(BlogPost, self).__init__(*args, **kwargs)
        BlogPost.urls[ self.url() ] = self.id
    
    def url(self):
        return title_to_url(self.title)
    
class Page(BasePage):
    url = TextField(unique=True)
    template = TextField(default='')
    custom_css = TextField(default='')
    content = TextField()
    markdown = BooleanField(default=False)
    
class Users(BaseModel):
    name = CharField(200)
    password = TextField() # Should not be plaintext
    email = CharField(200)
    is_admin = BooleanField(default=False)
    
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        
        # This object is only returned on succesful authentication attempts
        self.is_authenticated = True
        
    def is_active(self):
        return True
    
    def is_active(self):
        return True
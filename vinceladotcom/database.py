from peewee import *
from playhouse.pool import PooledSqliteDatabase

import datetime
import json

def has_tag(tag_list, tag):
    ''' Parse the tag field of a page '''
    
    tag_list = tag_list.split(',')
    for i in tag_list:
        if i.startswith(' '):
            i = i[1:]
        
        if i == tag:
            return True
    
    return False

db = PooledSqliteDatabase(database='vince.sqlite')
db.register_function(has_tag, name='has_tag', num_params=2)

##############################
# Post/Page Revision History #
##############################

db.execute_sql('''
    CREATE TRIGGER IF NOT EXISTS blog_revisions_ins
    UPDATE OF content on blogpost
        BEGIN
            INSERT INTO blogrevisions VALUES(
                old.id,
                old.content,
                old.modified
            );
        END;
''')
        
db.execute_sql('''
    CREATE TRIGGER IF NOT EXISTS page_revisions_ins
    UPDATE OF content on page
        BEGIN
            INSERT INTO pagerevisions VALUES(
                old.id,
                old.content,
                old.modified
            );
        END;
''')

def title_to_url(title):
    ret = title.lower()
    ret = ret.replace(' ', '-')
    return ret

class BaseModel(Model):
    class Meta:
        database = db
        
class BaseRevision(Model):
    ''' Base class for revision history models '''
    id = IntegerField()
    content = TextField()
    modified = DateField()
    
    class Meta:
        database = db
        primary_key = False
        
class BasePage(BaseModel):
    title = CharField(200, unique=True)
    tags = TextField(default='')
    created = DateField(default=lambda: datetime.datetime.now())
    modified = DateField(default=lambda: datetime.datetime.now())
    deleted = BooleanField(default=False)
    meta = TextField(default='')
    
    def __init__(self, *args, **kwargs):
        super(BasePage, self).__init__(*args, **kwargs)
        
        if self.meta:
            meta_data = json.loads(self.meta)
            for k, v in meta_data.items():
                setattr(self, k, v)

    def get_tags(self):
        def strip_leading_space(_str):
            if _str.startswith(' '):
                _str = _str[1: ]
            return _str

        return [strip_leading_space(i) for i in self.tags.split(',')]

class BlogPost(BasePage):
    author = CharField(200)
    draft = BooleanField(default=True)
    content = TextField()
    urls = {} # Mapping of titles to blog IDs
    
    def __init__(self, *args, **kwargs):
        super(BlogPost, self).__init__(*args, **kwargs)
        BlogPost.urls[ self.url() ] = self.id
    
    def url(self):
        ''' Return URL of blog post relative to /blog/ '''
        return title_to_url(self.title)
    
class Page(BasePage):
    url = TextField(unique=True)
    template = TextField(default='')
    custom_css = TextField(default='')
    content = TextField()
    markdown = BooleanField(default=False)
    
class BlogRevisions(BaseRevision):
    class Meta:
        constraints = [SQL('''
            FOREIGN KEY(id) REFERENCES blogpost(id) ON DELETE CASCADE''')]

class PageRevisions(BaseRevision):
    class Meta:
        constraints = [SQL('''
            FOREIGN KEY(id) REFERENCES page(id) ON DELETE CASCADE''')]
    
class Users(BaseModel):
    name = CharField(200)
    password = TextField() # Should not be plaintext
    full_name = CharField(200)
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
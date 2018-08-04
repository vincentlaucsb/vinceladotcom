from contextlib import contextmanager
from peewee import *
from playhouse.pool import PooledSqliteDatabase
from vinceladotcom.main import application

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

def title_to_url(title):
    temp = title.lower()
    ret = ''
    for i in temp:
        if i.isalnum():
            ret += i
        elif (i == '+'):
            ret += 'p'
        elif (i == ' '):
            ret += '-'
            
        # Strip other characters
    
    return ret

db = SqliteDatabase(database=application.config['DATABASE'])
db.register_function(has_tag, name='has_tag', num_params=2)
db.register_function(title_to_url, name='title_to_url', num_params=1)

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
    tags = TextField(default='')
    created = DateField(default=lambda: datetime.datetime.now())
    modified = DateField(default=lambda: datetime.datetime.now())
    deleted = BooleanField(default=False)
    meta = TextField(default='')
    
    def __init__(self, *args, **kwargs):
        super(BasePage, self).__init__(*args, **kwargs)
        
        if self.meta:
            meta_data = json.loads(self.meta)
            self.meta_parsed = meta_data
            
            for k, v in meta_data.items():
                setattr(self, k, v)

    def get_tags(self):
        def strip_leading_space(_str):
            if _str.startswith(' '):
                _str = _str[1: ]
            return _str

        return [strip_leading_space(i) for i in self.tags.split(',')]

class BlogPost(BasePage):
    title = CharField(200, unique=True)
    author = CharField(200)
    draft = BooleanField(default=True)
    content = TextField()
    
    def url(self):
        ''' Return URL of blog post relative to /blog/ '''
        return title_to_url(self.title)
    
class Page(BasePage):
    title = CharField(200)
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
        
        # This object is only returned on successful authentication attempts
        self.is_authenticated = True
        
    def is_active(self):
        return True
    
    def is_active(self):
        return True

def db_init() -> None:
    # Create tables
    db.create_tables([
        Users,
        BlogPost,
        Page,
        BlogRevisions,
        PageRevisions
    ])

    # Post/Page Revision History
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
from contextlib import contextmanager
from peewee import *
from playhouse.pool import PooledSqliteDatabase
from vinceladotcom.main import application
from vinceladotcom.config import STATIC_DIR

import os
import datetime
import json

DISPLAY_IMAGE_DIR = os.path.join(STATIC_DIR, 'blog', 'display')

def has_tag(tag_list: str, tag: str) -> bool:
    ''' Parse the tag field of a page '''
    
    tag_list = tag_list.split(',')
    for i in tag_list:
        if i.startswith(' '):
            i = i[1:]
        
        if i == tag:
            return True
    
    return False

def title_to_url(title: str) -> str:
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
        
        self.meta_parsed = {}
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
    ''' Model for blog posts '''

    title = CharField(200, unique=True)
    author = CharField(200)
    draft = BooleanField(default=True)
    content = TextField()
    
    @property
    def url(self):
        ''' Return URL of blog post relative to /blog/ '''
        return title_to_url(self.title)

    @property
    def _image_name(self):
        # TODO: Non-JPG images?
        return '{}.jpg'.format(self.id)

    @property
    def _image_path(self):
        return os.path.join(DISPLAY_IMAGE_DIR, self._image_name)

    @property
    def image(self):
        ''' Return the path to display image (if it exists) '''
        return '/static/blog/display/' + self._image_name if os.path.isfile(self._image_path) else None

    def save_image(self, data):
        ''' Upload image for post '''
        def write():
            data.save(self._image_path)

        try:
            write()
        except FileNotFoundError:
            os.makedirs(DISPLAY_IMAGE_DIR)
            write()

    def delete_image(self):
        ''' Delete associated display image (if exists) or do nothing '''
        if self.image:
            os.remove(self._image_path)
    
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
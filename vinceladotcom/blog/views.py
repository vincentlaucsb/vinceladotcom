from flask_login import login_required
from flask import Blueprint, request, redirect
from flask.views import View
from peewee import *

from abc import ABC, abstractmethod
import os

from .forms import *
from .. import markdown
from ..config import render_template, STATIC_DIR

DISPLAY_IMAGE_DIR = os.path.join(STATIC_DIR, 'blog', 'display')
blog = Blueprint('blog', __name__)

#################
# Blog Controls
#################

def get_post_image(id):
    ''' Return the path to image (if it exists) '''
    from os.path import isfile, join
    
    # TODO: Non JPG files?
    image_name = '{}.jpg'.format(id)
    image_path = join(DISPLAY_IMAGE_DIR, image_name)
    
    if isfile(image_path):
        return '/static/blog/display/' + image_name
    return None

def create_post_image(id, data):
    ''' Create a display image for a blog '''        
    # TODO: Non JPG files?
    image_name = '{}.jpg'.format(id)
    image_path = os.path.join(DISPLAY_IMAGE_DIR, image_name)
    
    def write():
        data.save(image_path)

    try:
        write()
    except FileNotFoundError:
        os.makedirs(image_folder)
        write()

@blog.route("/blog/", methods=['GET'])
def blog_list():
    from .. import database
    posts = []
    drafts = []
    
    for post in database.BlogPost.select().order_by(
        database.BlogPost.created.desc()):
        if not post.draft:
            posts.append(post)
        else:
            drafts.append(post)
            
    return render_template('blog/index.html', posts=posts, drafts=drafts)

@blog.route("/blog/<title>/", methods=['GET'])
def blog_article(title):
    from .. import database

    article = database.BlogPost.get(fn.title_to_url(
        database.BlogPost.title) == title)

    return render_template(
        'blog/post.html',
        post=article,
        image=get_post_image(article.id),
        content=markdown.parse_markdown(article.content)
    )
    
class blog_base(ABC, View):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(blog_base, self).__init__(*args, **kwargs)
        self.blog = None
        self.form = None

    @abstractmethod
    def target(self, *args, **kwargs):
        pass

    def get(self):
        pass

    @abstractmethod
    def submit(self):
        pass

    def dispatch_request(self, post_id=None):
        from .. import database
        # Render article
        if (post_id):
            self.blog = database.BlogPost.get(database.BlogPost.id == post_id)
            
        self.form = BlogForm(request.form)
        preview = ''
    
        if request.method == 'GET':
            self.get()
        elif request.method == 'POST':
            if self.form.submit.data: # Submit button pressed
                self.submit()
                if (request.files):  # Handle image
                    create_post_image(self.blog.id, request.files['image'])
                
                return redirect('blog/' + self.blog.url())
            else:
                # Preview button pressed
                preview = markdown.parse_markdown(self.form.content.data)
    
        return render_template(
            'blog/editor.html',
            current_user=current_user,
            form=self.form,
            preview=preview,
            target=self.target(post_id)
        )

class BlogCreator(blog_base):
    def target(self, *args, **kwargs):
        return '/blog/new'

    def submit(self):
        from .. import database
        self.blog = database.BlogPost.create(author=current_user.full_name, **self.form.data_dict())

class BlogEditor(blog_base):
    def target(self, post_id):
        return '/blog/edit/' + str(post_id)

    def submit(self):
        from .. import database
        database.BlogPost(
            id=self.blog.id,
            author=current_user.full_name,
            **self.form.data_dict()
        ).save()

    def get(self):
        # Form Attributes
        self.form.fill(self.blog)

blog_editor_view = login_required(BlogEditor.as_view('blog_editor'))
blog_new_view = login_required(BlogCreator.as_view('blog_creator'))
blog.add_url_rule('/blog/edit/<int:post_id>', view_func=blog_editor_view)
blog.add_url_rule('/blog/new', view_func=blog_new_view)
    
########
# Tags #
########

@blog.route("/blog/tags/<tag>", methods=['GET'])
def tag_list(tag):
    from .. import database
    posts = []
    
    for post in database.BlogPost.select().where(
        fn.has_tag(database.BlogPost.tags, tag)
        ).order_by(
        database.BlogPost.created.desc()):
        posts.append(post)
            
    return render_template('blog/index.html', posts=posts)
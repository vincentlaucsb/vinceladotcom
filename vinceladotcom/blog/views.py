from flask_login import login_required
from flask import Blueprint, request, redirect
from flask.views import MethodView, View
from peewee import *
import os

from .forms import *
from .. import markdown
from ..config import render_message, render_template, STATIC_DIR

blog = Blueprint('blog', __name__)

@blog.route("/blog/tags/<string:tag>", methods=['GET'])
def tag_list(tag: str):
    from .. import database            
    return render_template(
        'blog/index.html',
        posts=database.BlogPost.select().where(
            fn.has_tag(database.BlogPost.tags, tag)
            ).order_by(
            database.BlogPost.created.desc()))

#################
# Blog Controls
#################

@blog.route("/blog/<string:title>/", methods=['GET'])
def blog_article(title: str):
    from .. import database

    article = database.BlogPost.get(fn.title_to_url(
        database.BlogPost.title) == title)

    return render_template(
        'blog/post.html',
        post=article,
        content=markdown.parse_markdown(article.content)
    )

@blog.route("/blog/new", methods=['GET'])
def blog_new():
    return render_template(
        'blog/editor.html',
        current_user=current_user,
        form=BlogForm(request.form),
        target='/blog/'
    )

class BlogAPI(MethodView):

    @staticmethod
    def get_post(post_id: int):
        from .. import database
        return database.BlogPost.get(database.BlogPost.id == post_id)
    
    def get(self, post_id: int = None):
        from .. import database

        if post_id is None:
            # Return a list of users
            posts = []
            drafts = []
            deleted = []
    
            for post in database.BlogPost.select().order_by(
                database.BlogPost.created.desc()):
                if post.deleted:
                    deleted.append(post)
                elif not post.draft:
                    posts.append(post)
                else:
                    drafts.append(post)
            
            return render_template(
                'blog/index.html',
                posts=posts, drafts=drafts, deleted=deleted
            )

        else:
            # Show editor for single post
            post = self.get_post(post_id)
            form = BlogForm(request.form)
            form.fill(post)

            return render_template(
                'blog/editor.html',
                target='/blog/{}'.format(post_id),
                current_user=current_user,
                form=form,
                post=post
            )

    def post(self, post_id: int = None):
        from .. import database

        if (not post_id):
            # Create a new page
            form = BlogForm(request.form)
            post = database.BlogPost.create(author=current_user.full_name, **form.data_dict())

            if (request.files):  # Handle image
                post.save_image(request.files['image'])

            return redirect('blog/' + post.url)
        else:
            # Update a page (funnel PUT request)
            if (request.form['_method'] == 'put'):
                return self.put(post_id)
            else:
                abort(405)

    def put(self, post_id: int):
        # Update a page
        from .. import database

        form = BlogForm(request.form)
        post = database.BlogPost(
            id=post_id,
            author=current_user.full_name,
            **form.data_dict())
        post.save()

        if (request.files):  # Handle image
            post.save_image(request.files['image'])

        return redirect('blog/' + post.url)
            
    def delete(self, post_id: int):
        # Delete the specified post or image
        post = self.get_post(post_id)

        if (request.args.get('target', '') == 'image'):
            # Delete associated image
            post.delete_image()
        else:
            if (not post.deleted):
                # Mark as "deleted" without deleting
                post.deleted = True
                post.save()
            else:
                # If marked as deleted, then perma-delete
                post.delete_instance()
            
        return render_message(title='Deleted', message='Deleted item')

blog_view = BlogAPI.as_view('blog_api')
blog.add_url_rule(
    '/blog/',
    view_func=blog_view, methods=['GET', 'POST']
)

# Because HTML forms only support GET/POST, POST endpoint
# merely funnels PUT requests (or throws errors)
blog.add_url_rule('/blog/<int:post_id>', view_func=blog_view,
                  methods=['GET', 'POST', 'PUT', 'DELETE'])
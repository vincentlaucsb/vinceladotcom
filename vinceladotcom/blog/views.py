from flask_login import login_required
from flask import Blueprint, request, redirect
from peewee import *

from .forms import *
from .. import markdown
from ..config import render_template

blog = Blueprint('blog', __name__)

#################
# Blog Controls
#################

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
        content=markdown.parse_markdown(article.content)
    )
    
@blog.route("/blog/edit/<int:post_id>", methods=['GET', 'POST'])
@login_required
def blog_edit(post_id):
    from .. import database
    # Render article
    blog = database.BlogPost.get(database.BlogPost.id == post_id)
    form = BlogForm(request.form)
    
    preview = ''
    
    # Form Attributes
    if request.method == 'GET':
        form.page_title.data = blog.title
        form.created.data = blog.created
        form.content.data = blog.content
        form.draft.data = blog.draft
        form.metadata.data = blog.meta
        form.tags.data = blog.tags
    
    # Show a preview of the rendered Markdown
    elif request.method == 'POST':
    
        if form.submit.data:
            # Submit button pressed
            database.BlogPost(id=blog.id, author=current_user.full_name, **form.data_dict()).save()
            return redirect('blog/' + blog.url())
        else:
            # Preview button pressed
            preview = markdown.parse_markdown(form.content.data)
    
    return render_template(
        'blog/editor.html',
        current_user=current_user,
        form=form,
        preview=preview,
        target='/blog/edit/' + str(post_id)
    )
    
@blog.route("/blog/new", methods=['GET', 'POST'])
@login_required
def blog_post():
    from .. import database
    form = BlogForm(request.form)
    preview = ''
    
    # Show a preview of the rendered Markdown
    if request.method == 'POST':
    
        if form.submit.data:
            # Submit button pressed
            database.BlogPost.create(author=current_user.full_name, **form.data_dict())
        else:
            # Preview button pressed
            preview = markdown.parse_markdown(form.content.data)
    
    return render_template(
        'blog/editor.html',
        current_user=current_user,
        form=form,
        preview=preview,
        target='/blog/new'
    )
    
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
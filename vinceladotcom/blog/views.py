import flask_login
from flask import Blueprint, request
from .forms import *
from .. import database, markdown
from ..config import render_template

blog = Blueprint('blog', __name__)

@blog.route("/blog/", methods=['GET'])
def blog_list():
    posts = []
    drafts = []
    
    for post in database.BlogPost.select():
        if not post.draft:
            posts.append(post)
        else:
            drafts.append(post)
            
    return render_template('blog/index.html', posts=posts, drafts=drafts)

@blog.route("/blog/<title>", methods=['GET'])
def blog_article(title):
    # Load list of BlogPosts
    if not database.BlogPost.urls:
        for i in database.BlogPost.select():
            pass
    
    # Render article
    article_id = database.BlogPost.urls[title]
    article = database.BlogPost.get(database.BlogPost.id == article_id)
    return render_template(
        'blog/post.html',
        post=article,
        title=article.title,
        content=markdown.parse_markdown(article.content)
    )
    
@blog.route("/blog/edit/<int:post_id>", methods=['GET', 'POST'])
def blog_edit(post_id):
    # Render article
    blog = database.BlogPost.get(database.BlogPost.id == post_id)
    form = BlogForm(request.form)
    preview = ''
    
    # Form Attributes
    if request.method == 'GET':
        form.page_title.data = blog.title
        form.content.data = blog.content
        form.draft.data = blog.draft
    
    # Show a preview of the rendered Markdown
    elif request.method == 'POST':
    
        # Submit button pressed
        if form.submit.data:
            database.BlogPost(
                id=blog.id,
                title=form.page_title.data,
                author='Vincent La',
                draft=form.draft.data,
                content=form.content.data
            ).save()
            
        # Preview button pressed
        else:
            preview = markdown.parse_markdown(form.content.data)
    
    return render_template(
        'blog/editor.html',
        form=form,
        preview=preview,
        target='/blog/edit/' + str(post_id)
    )
    
@blog.route("/blog/new", methods=['GET', 'POST'])
def blog_post():
    form = BlogForm(request.form)
    preview = ''
    
    # Show a preview of the rendered Markdown
    if request.method == 'POST':
    
        # Submit button pressed
        if form.submit.data:
            database.BlogPost.create(
                title=form.page_title.data,
                author='Vincent La',
                draft=form.draft,
                content=form.content.data
            )
            
        # Preview button pressed
        else:
            preview = markdown.parse_markdown(form.content.data)
    
    return render_template(
        'blog/editor.html',
        form=form,
        preview=preview,
        target='/blog/new'
    )
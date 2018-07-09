from flask_login import login_required
from flask import Blueprint, request, redirect
from .forms import *
from .. import database, markdown
from ..config import render_template

blog = Blueprint('blog', __name__)

@blog.route("/blog/", methods=['GET'])
def blog_list():
    posts = []
    drafts = []
    
    for post in database.BlogPost.select().order_by(
        database.BlogPost.created.desc()):
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
        content=markdown.parse_markdown(article.content)
    )
    
@blog.route("/blog/edit/<int:post_id>", methods=['GET', 'POST'])
@login_required
def blog_edit(post_id):
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
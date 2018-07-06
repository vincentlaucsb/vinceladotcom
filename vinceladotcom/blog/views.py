import flask_login
from flask import Blueprint, request
from .forms import *
from .. import database
from ..config import render_template

blog = Blueprint('blog', __name__)

@blog.route("/blog/", methods=['GET'])
def blog_list():
    posts = []
    drafts = []
    
    for post in database.BlogPost.select():
        if post.draft:
            posts.append(post)
        else:
            drafts.append(post)
            
    return render_template('blog_index.html', posts=posts, drafts=drafts)

def blog_article(title):
    try:
        article_id = BLOG_ARTICLES[database.title_to_url(title)]
    except KeyError:
        return render_template('404.html'), 404
        
    article = database.BlogPost.get(database.BlogPost.id == article_id)
    return render_template(
        'blog_post.html',
        post=article,
        title=article.title,
        content=markdown.parse_markdown(article.content)
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
                title=form.title.data,
                author='Vincent La',
                draft=True,
                content=form.content.data
            )
            
        # Preview button pressed
        else:
            preview = markdown.parse_markdown(form.content.data)
    
    return render_template('blog_new.html', form=form, preview=preview)
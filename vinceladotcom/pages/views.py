from copy import copy

from flask_login import login_required
import flask_login

from flask import Blueprint, request, redirect
from .forms import *
from .. import database
from ..config import render_template, PAGE_GLOBALS

page = Blueprint('page', __name__)

@page.route("/pages/", methods=['GET'])
@login_required
def page_list():
    posts = []
    drafts = []
    
    for post in database.Page.select():
        posts.append(post)
        #if post.draft:
            
        #else:
            #drafts.append(post)
            
    return render_template('pages/index.html', posts=posts, drafts=drafts)
        
@page.route("/pages/<title>", methods=['GET'])
def page_view(title):
    ''' Render a page '''
    page = database.Page.get(database.Page.url == title)
    template = page.template
    if not template:
        template = 'base_page.html'
    
    return render_template(
        template,
        page = page,
        **PAGE_GLOBALS
    )
        
@page.route("/pages/new", methods=['GET', 'POST'])
@login_required
def page_new():
    ''' Create a new page '''
    form = PageForm(request.form)
    preview = ''
    
    # Show a preview of the rendered HTML
    if request.method == 'POST':
    
        # Submit button pressed
        if form.submit.data:
            database.Page(
                title=form.page_title.data,
                css=form.custom_css.data,
                url=form.url.data,
                content=form.content.data,
                markdown=form.markdown.data
            ).save()
            
        # Preview button pressed
        else:
            preview = form.content.data
    
    return render_template(
        'pages/editor.html',
        form=form,
        preview=preview,
        target="/pages/new"
    )

@page.route("/pages/edit/<int:page_id>", methods=['GET', 'POST'])
@login_required
def page_edit(page_id):
    ''' Update an existing page '''
    page = database.Page.get(database.Page.id == page_id)
    form = PageForm(request.form)
    error = ''
    preview = ''
    
    # Show a preview of the rendered HTML
    if request.method == 'GET':
        # Form Attributes
        form.page_title.render_kw = { 'value': page.title }
        form.template.render_kw = { 'value': page.template }
        form.url.render_kw = { 'value': page.url }
        form.markdown.render_kw = { 'markdown': page.markdown }
        form.content.data = page.content
        form.metadata.data = page.meta
    
    elif request.method == 'POST':
        if not form.validate():
            error = copy(form.errors)
            form.errors.clear()
        elif form.submit.data:
            # Submit button pressed
            database.Page(
                id=page.id,  # So Peewee knows we want to do an UPDATE
                created=page.created,
                **form.data_dict()
            ).save()
            return redirect('pages/' + page.url)
        else:
            # Preview button pressed
            preview = form.content.data
    
    return render_template(
        'pages/editor.html', 
        current_user = flask_login.current_user,
        form=form, 
        error=error,
        preview=preview,
        target="/pages/edit/" + str(page_id)
    )

@page.route("/pages/delete/<int:page_id>", methods=['GET', 'POST'])
@login_required
def page_delete(page_id):
    page = database.Page.get(database.Page.id == page_id)
    page.delete_instance()
    
    return flask.redirect('/')
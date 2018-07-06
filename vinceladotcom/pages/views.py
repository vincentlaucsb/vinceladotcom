import flask_login
from flask import Blueprint, request
from .forms import *
from .. import database
from ..config import render_template

page = Blueprint('page', __name__)

@page.route("/pages/new", methods=['GET', 'POST'])
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
                content=form.content.data
            ).save()
            
        # Preview button pressed
        else:
            preview = form.content.data
    
    return render_template(
        'pages/new.html',
        form=form,
        preview=preview,
        target="/pages/new"
    )

@page.route("/pages/<int:page_id>", methods=['GET', 'POST'])
def page_edit(page_id):
    ''' Update an existing page '''
    page = database.Page.get(database.Page.id == page_id)
    form = PageForm(request.form)
    
    # Form Attributes
    form.page_title.render_kw = { 'value': page.title }
    form.template.render_kw = { 'value': page.template }
    form.url.render_kw = { 'value': page.url }
    
    preview = ''
    
    # Show a preview of the rendered HTML
    if request.method == 'GET':
        form.content.data = page.content
    
    elif request.method == 'POST':
    
        # Submit button pressed
        if form.submit.data:
            new_page(
                id=page.id,  # So Peewee knows we want to do an UPDATE
                title=form.page_title.data,
                content=form.content.data,
                css=form.custom_css.data,
                url=form.url.data
            )
            
        # Preview button pressed
        else:
            preview = form.content.data
    
    return render_template('pages/new.html', 
        current_user = flask_login.current_user,
        form=form, content=page.content, preview=preview,
        target="/pages/" + str(page_id)
    )

@page.route("/pages/delete/<int:page_id>", methods=['GET', 'POST'])
def page_delete(page_id):
    page = database.Page.get(database.Page.id == page_id)
    page.delete_instance()
    
    return flask.redirect('/')
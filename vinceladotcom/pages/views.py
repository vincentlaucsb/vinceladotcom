import os
from copy import copy

import flask_login
import flask
import peewee

from flask_login import login_required
from flask import Blueprint, request, redirect, jsonify
from .forms import *
from .. import database
from ..config import CURRENT_DIR, render_template, PAGE_GLOBALS

from jinja2 import Template

page = Blueprint('page', __name__)

with open(os.path.join(CURRENT_DIR, "templates/macros.html")) as macros:
    MACROS = macros.read()

@page.route("/pages/", methods=['GET'])
@login_required
def page_list():
    posts = [i for i in database.Page.select()]
   
    return render_template('pages/index.html', posts=posts)
        
@page.route("/pages/<path:url>", methods=['GET'])
def page_view(url):
    ''' Render a page '''
    
    try:
        page = database.Page.get(database.Page.url == url)
        template = page.template
        if not template:
            template = 'base_page.html'
        
        page.content = Template(page.content).render(
            page=page,
            current_user=flask_login.current_user,
            **PAGE_GLOBALS
        )
        
        return render_template(
            template,
            page=page,
            current_user=flask_login.current_user,
            **PAGE_GLOBALS
        )
        
    except peewee.DoesNotExist:
        flask.abort(404)
        
@page.route("/pages/new", methods=['GET', 'POST'])
@login_required
def page_new():
    ''' Create a new page '''
    form = PageForm(request.form)
    preview = ''
    
    # Show a preview of the rendered HTML
    if request.method == 'POST':
        if form.submit.data:
            # Submit button pressed
            database.Page(**form.data_dict()).save()
        else:
            # Preview button pressed
            preview = Template(MACROS + form.content.data).render(
                page=form.data_dict(),
                current_user=flask_login.current_user,
                **PAGE_GLOBALS
            )
    
    return render_template(
        'pages/editor.html',
        form=form,
        current_user = flask_login.current_user,
        preview=preview,
        target="/pages/new",
        page_globals = PAGE_GLOBALS
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
        form.url.render_kw = { 'value': page.url }
        form.markdown.render_kw = { 'markdown': page.markdown }
        form.content.data = page.content
        form.metadata.data = page.meta
        form.created.data = page.created
        form.template.data = page.template
    
    elif request.method == 'POST':
        if not form.validate():
            error = copy(form.errors)
            form.errors.clear()
        elif form.submit.data:
            # Submit button pressed
            database.Page(
                id=page.id,  # So Peewee knows we want to do an UPDATE
                **form.data_dict()
            ).save()
            return redirect('pages/' + page.url)
        else:
            # Preview button pressed
            preview = Template(MACROS + form.content.data).render(page=page,
                current_user = flask_login.current_user,
                **PAGE_GLOBALS)
    
    return render_template(
        'pages/editor.html', 
        current_user = flask_login.current_user,
        form=form, 
        error=error,
        preview=preview,
        target="/pages/edit/" + str(page_id),
        page_globals = PAGE_GLOBALS
    )
    
@page.route("/pages/history/<int:page_id>", methods=['GET', 'POST'])
def page_history(page_id):
    past_revisions = database.PageRevisions.select().where(
        database.PageRevisions.id == page_id
    )
    
    return render_template(
        'pages/history.html',
        history = past_revisions
    )
    
@page.route("/pages/edit/globals", methods=['GET', 'POST'])
@login_required
def page_globals():
    return jsonify(PAGE_GLOBALS)

@page.route("/pages/delete/<int:page_id>", methods=['GET', 'POST'])
@login_required
def page_delete(page_id):
    page = database.Page.get(database.Page.id == page_id)
    page.delete_instance()
    
    return flask.redirect('/')
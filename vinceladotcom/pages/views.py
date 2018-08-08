import os
import flask
import peewee

from flask_login import current_user, login_required
from flask import Blueprint, request, redirect, jsonify
from jinja2 import Template
from copy import copy

from vinceladotcom.pages.forms import *
from vinceladotcom.config import CURRENT_DIR, render_template, PAGE_GLOBALS

page = Blueprint('page', __name__)

@page.route("/pages/", methods=['GET'])
@login_required
def page_list():
    posts = [i for i in database.Page.select()]
   
    return render_template('pages/index.html', posts=posts)
        
@page.route("/pages/<path:url>", methods=['GET'])
def page_view(url):
    ''' Render a page '''
    from vinceladotcom import database

    try:
        page = database.Page.get(database.Page.url == url)
        template = page.template
        if not template:
            template = 'pages/page.html'
        
        page.content = Template(page.content).render(
            page=page,
            current_user=current_user,
            **PAGE_GLOBALS
        )
        
        return render_template(
            template,
            page=page,
            current_user=current_user,
            **PAGE_GLOBALS
        )
        
    except peewee.DoesNotExist:
        flask.abort(404)
        
@page.route("/pages/new", methods=['GET', 'POST'])
@login_required
def page_new():
    ''' Create a new page '''
    from vinceladotcom import database
    form = PageForm(request.form)
    preview = ''
    
    # Show a preview of the rendered HTML
    if request.method == 'POST':
        if form.submit.data:
            # Submit button pressed
            database.Page(**form.data_dict()).save()
        else:
            # Preview button pressed
            preview = Template(form.content.data).render(
                page=form.data_dict(),
                current_user=current_user,
                **PAGE_GLOBALS
            )
    
    return render_template(
        'pages/editor.html',
        form=form,
        current_user = current_user,
        preview=preview,
        target="/pages/new",
        page_globals = PAGE_GLOBALS
    )

@page.route("/pages/edit/<int:page_id>", methods=['GET', 'POST'])
@login_required
def page_edit(page_id):
    ''' Update an existing page '''
    from vinceladotcom import database
    page = database.Page.get(database.Page.id == page_id)
    form = PageForm(request.form)
    error = ''
    preview = ''
    
    # Show a preview of the rendered HTML
    if request.method == 'GET':
        form.fill(page)
    
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
            preview = Template(form.content.data).render(page=page,
                current_user = current_user,
                **PAGE_GLOBALS)
    
    return render_template(
        'pages/editor.html', 
        current_user = current_user,
        form=form, 
        error=error,
        preview=preview,
        target="/pages/edit/" + str(page_id),
        page_globals = PAGE_GLOBALS
    )
    
@page.route("/pages/history/<int:page_id>", methods=['GET', 'POST'])
def page_history(page_id):
    from vinceladotcom import database
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
    from vinceladotcom import database
    page = database.Page.get(database.Page.id == page_id)
    page.delete_instance()
    
    return flask.redirect('/')
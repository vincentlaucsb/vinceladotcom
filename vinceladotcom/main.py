# Third Party
import flask
from flask import abort, redirect, flash, request

import wtforms
from wtforms import validators, Form, FileField, SelectField, TextField, \
    TextAreaField, StringField, SubmitField
from markupsafe import Markup, escape
    
import datetime
import os
from os import path

# My Libraries
from .sitemap import SitemapEntry
from .config import *
from . import auth, markdown, database, blog, pages

import json

''' Authentication '''

from flask_login import login_required
import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return database.Users.get(user_id)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = auth.LoginForm(request.form)
    error = ""
    
    if (request.method == 'POST'):
        user = form.validate()
        if user:
            flask_login.login_user(user)
            
            flask.flash('Logged in succesfully.')
            next = flask.request.args.get('next')
            
            #if not is_safe_url(next):
            #    return flask.abort(400)
            
            return flask.redirect(next or flask.url_for('index'))
    else:
        error = "Login failed"
    
    return flask.render_template('login.html', form=form,
        error=error)
    
@app.route('/logout')
@login_required
def logout():
    # flask_login.current_user.is_authenticated = False
    flask_login.logout_user()
    return redirect('/')
    
'''
Beginning of App
'''

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/pages/", methods=['GET'])
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
    
@app.route("/sitemap.xml", methods=['GET'])
def sitemap():
    ''' Generate a sitemap.xml at the root '''
    
    entries = ''

    for post in database.BlogPost.select():
        entry = SitemapEntry()
        entry['loc'] = 'blog/' + post.url()
        entry['lastmod'] = post.modified
        
        entries += entry.to_string(request.url_root)
        
    for post in database.Page.select():
        entry = SitemapEntry()
        entry['loc'] = post.url[1:] # Strip out leading /
        
        entries += entry.to_string(request.url_root)

    sitemap_xml = render_template('sitemap.xml', entries=entries)
    response = flask.make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

def run():
    # Route blog posts
    for post in database.BlogPost.select():
        app.add_url_rule('/blog/' + post.url(), view_func=blog.views.blog_article, methods=['GET'])
        
    # Route pages
    for page in database.Page.select():
        router = pages.urls.make_router(page)
        app.add_url_rule(router.url, view_func=router)
        print("Routing {}".format(router.url))

    app.register_blueprint(blog.views.blog)
    app.register_blueprint(pages.views.page)
    app.run(host='0.0.0.0')
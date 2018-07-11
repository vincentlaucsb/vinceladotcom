# Third Party
import flask
from flask import abort, redirect, flash, request

import wtforms
from wtforms import validators, Form, FileField, SelectField, TextField, \
    TextAreaField, StringField, SubmitField
from markupsafe import Markup, escape
    
import requests
import datetime
import os
from os import path

# My Libraries
from .sitemap import Sitemap, SitemapEntry
from .config import *
from . import auth, database, markdown, blog, pages

import json

# App config
from .secret import SECRET_KEY
DEBUG = True
application = Flask(__name__, static_url_path='/static')
application.config.from_object(__name__)
application.config['SECRET_KEY'] = SECRET_KEY

def init_db():
    database.db.create_tables([
        database.Users,
        database.BlogPost,
        database.Page,
        database.BlogRevisions,
        database.PageRevisions
    ])

init_db()
application.register_blueprint(blog.views.blog)
application.register_blueprint(pages.views.page)

''' Authentication '''
from flask_login import login_required
import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return database.Users.get(user_id)
    
@application.route('/login', methods=['GET', 'POST'])
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
    
    return render_template(
        'login.html',
        form=form,
        error=error
    )
    
@application.route('/logout')
@login_required
def logout():
    flask_login.logout_user()
    return render_template(
        'message.html',
        title='Logged out',
        message='You have been logged out.'
    )
    
####################
# Beginning of App #
####################

@application.route("/", methods=['GET'])
def index():
    return render_template('index.html')
    
@application.route("/sitemap.xml", methods=['GET'])
def sitemap():
    ''' Generate a sitemap.xml at the root '''
    
    _sitemap = Sitemap(request.url_root)
    
    for i in application.url_map.iter_rules():
        url = str(i)
        
        entry = SitemapEntry()
        entry['loc'] = url
        
        if (url.find('<') < 0 or url.find('>') < 0):
            _sitemap.add(entry)
        
    for post in database.BlogPost.select():
        entry = SitemapEntry()
        entry['loc'] = 'blog/' + post.url()
        entry['lastmod'] = post.modified
        _sitemap.add(entry)
        
    for post in database.Page.select():
        entry = SitemapEntry()
        entry['loc'] = 'pages/' + post.url
        entry['lastmod'] = post.modified
        _sitemap.add(entry)

    sitemap_xml = render_template('sitemap.xml', entries=str(_sitemap))
    response = flask.make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response
from typing import *
import flask
from flask import Flask, abort, redirect, flash, request

import wtforms
from wtforms import validators, Form, FileField, SelectField, TextField, \
    TextAreaField, StringField, SubmitField
from markupsafe import Markup, escape
    
import requests
import datetime
import os
from os import path

# My Libraries
from vinceladotcom.sitemap import Sitemap, SitemapEntry
from vinceladotcom.config import *

import json

DEBUG = True

from . import secret
application = Flask(__name__, static_url_path='/static')
application.config.from_object(__name__)
application.config['SECRET_KEY'] = secret.SECRET_KEY
application.config['DATABASE'] = 'vince.sqlite'

from vinceladotcom import auth, blog, pages
application.register_blueprint(blog.views.blog)
application.register_blueprint(pages.views.page)

''' Authentication '''
from flask_login import login_required
import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    from . import database
    return database.Users.get(user_id)
    
@login_manager.unauthorized_handler
def unauthorized_handler():
    from . import database
    return redirect('/login')
    
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
        'plain.html',
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
    from . import database
    
    _sitemap = Sitemap(request.url_root)
    
    # Add US Commutes Times Map
    usa = SitemapEntry()
    usa['loc'] = 'usa/'
    _sitemap.add(usa)
    
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
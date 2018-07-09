from flask import Flask
from os import path
import json
import flask

CURRENT_DIR = path.dirname(path.realpath(__file__))
STATIC_DIR = path.join(CURRENT_DIR, 'static')
GLOBALS_PATH = path.join(CURRENT_DIR, 'globals.json')

# App config
from .secret import SECRET_KEY
DEBUG = True
app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def settings_loader():
    with open(GLOBALS_PATH, 'r') as globals:
        return json.loads(globals.read())

# Global variables that all pages can access
PAGE_GLOBALS = settings_loader()

def render_template(*args, **kwargs):
    ''' Overload of render_template() which injects global variables '''
    for k in PAGE_GLOBALS.keys():
        kwargs[k] = PAGE_GLOBALS[k]
    
    return flask.render_template(*args, **kwargs)
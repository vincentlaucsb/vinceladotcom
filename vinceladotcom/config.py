from typing import *
from flask import Flask
from os import path
import json
import flask
import requests

CURRENT_DIR = path.dirname(path.realpath(__file__))
STATIC_DIR = path.join(CURRENT_DIR, 'static')
GLOBALS_PATH = path.join(CURRENT_DIR, 'globals.json')

def settings_loader():
    with open(GLOBALS_PATH, 'r') as globals:
        return json.loads(globals.read())

def get_github_repos():
    github_repos = {}

    try:
        with open('github.json', 'r') as github_data:
            github_repos = json.loads(github_data.read())
            
    except:
        temp = requests.get("https://api.github.com/users/vincentlaucsb/repos").text
        github_repos = json.loads(temp)
        
        # Save data
        with open('github.json', 'w') as github_data:
            github_data.write(temp)
            
    return { i['full_name'] : i for i in github_repos }
        
# Global variables that all pages can access
PAGE_GLOBALS = settings_loader()
PAGE_GLOBALS['github'] = get_github_repos()

# Helpers
def invert_dict(d: dict) -> dict:
    ''' Invert a dictionary, throwing an error if duplicate keys are found '''
    ret = {}

    for k, v in d.items():
        if (v in ret.keys()):
            raise ValueError("Duplicate key found")

        ret[v] = k

    return ret

def render_template(*args, **kwargs):
    ''' Overload of render_template() which injects global variables '''
    for k in PAGE_GLOBALS.keys():
        kwargs[k] = PAGE_GLOBALS[k]
    
    return flask.render_template(*args, **kwargs)
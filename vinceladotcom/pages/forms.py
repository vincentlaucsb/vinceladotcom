import os

from wtforms import validators, Form, BooleanField, TextAreaField, \
    TextField, SelectField, SubmitField
from ..config import CURRENT_DIR

def get_templates():
    templates = []
    for i in os.listdir(os.path.join(CURRENT_DIR, 'templates')):
        current_file = os.path.join(CURRENT_DIR, 'templates', i)
        if (os.path.isfile(current_file)):
            templates.append(i)
            
    return templates

class PageForm(Form):
    content = TextAreaField()
    custom_css = TextAreaField()
    page_title = TextField()
    url = TextField()
    template = SelectField(
        'Template',
        choices=[ (i, i) for i in get_templates() ]
    )
    submit = SubmitField()
    preview = SubmitField()
    markdown = BooleanField(default=False)
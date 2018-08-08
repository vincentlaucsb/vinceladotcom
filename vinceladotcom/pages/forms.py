import os
import json

from wtforms import validators, ValidationError, Form, BooleanField, TextAreaField, \
    TextField, SelectField, SubmitField
from vinceladotcom.config import CURRENT_DIR
from vinceladotcom.forms import *

def get_templates():
    templates = []
    for i in os.listdir(os.path.join(CURRENT_DIR, 'templates')):
        current_file = os.path.join(CURRENT_DIR, 'templates', i)
        if (os.path.isfile(current_file)):
            templates.append(i)
            
    return templates
    
class PageForm(BaseForm):
    # Mapping of database column names to form names
    db_mapping = dict(
        title = 'page_title',
        content = 'content',
        custom_css = 'custom_css',
        url = 'url',
        markdown = 'markdown',
        meta = 'metadata',
        created = 'created',
        tags = 'tags',
        template = 'template'
    )

    content = AceTextPreviewField()
    metadata = AceTextField()
    custom_css = TextAreaField()
    page_title = TextField('')
    url = TextField()
    template = SelectField(
        'Template',
        choices=[ ('', '') ] +[ (i, i) for i in get_templates() ]
    )
    submit = SubmitField()
    preview = SubmitField()
    markdown = BooleanField(default=False)
    
    def validate_metadata(form, field):
        try:
            if field.data:
                parse_metadata(field.data)
        except:
            form.errors.append("Invalid metadata")
            raise ValidationError()
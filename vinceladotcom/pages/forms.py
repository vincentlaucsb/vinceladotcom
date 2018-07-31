import os
import json

from wtforms import validators, ValidationError, Form, BooleanField, TextAreaField, \
    TextField, SelectField, SubmitField
from ..config import CURRENT_DIR
from ..forms import *

def get_templates():
    templates = []
    for i in os.listdir(os.path.join(CURRENT_DIR, 'templates')):
        current_file = os.path.join(CURRENT_DIR, 'templates', i)
        if (os.path.isfile(current_file)):
            templates.append(i)
            
    return templates

def parse_metadata(data):
    '''
    Given colon delimited lines of key-value pairs, return 
    a JSON representation
    '''
    
    temp = {}
    for row in data.split('\n'):
        try:
            k, v = row.split(':')
        except ValueError:
            # More than 2 colons
            splitted = row.split(':')
            k = ':'.join(splitted[:-1])
            v = splitted[-1]
        
        # Remove carriage return
        v = v.replace('\r', '')
        
        # Strip leading space
        if v.startswith(' '):
            temp[k] = v[1:]
        else:
            temp[k] = v

    return json.dumps(temp)
    
def deserialize_metadata(_json):
    ''' Deserialize metadata '''
    
    temp = ''
    
    try:
        for k, v in json.loads(_json).items():
            temp += '{}: {}\n'.format(k, v)
    except json.decoder.JSONDecodeError:
        pass
    
    return temp
    
class PageForm(BaseForm):
    # Mapping of database column names to form names
    db_mapping = dict(
        title = 'page_title',
        content = 'content',
        css = 'custom_css',
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
    
    def data_dict(self):
        ''' Parse metadata '''
        data = super(PageForm, self).data_dict()
        data['meta'] = parse_metadata(data['meta'])
        return data
    
    def validate_metadata(form, field):
        try:
            if field.data:
                parse_metadata(field.data)
        except:
            form.errors.append("Invalid metadata")
            raise ValidationError()
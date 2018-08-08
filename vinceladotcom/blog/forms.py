from flask_login import current_user
from wtforms import validators, Form, FileField, BooleanField, TextAreaField, \
    TextField, SubmitField
from ..forms import BaseForm, AceTextField

class BlogForm(BaseForm):
    # Mapping of database column names to form names
    db_mapping = dict(
        title = 'page_title',
        content = 'content',
        draft = 'draft',
        created = 'created',
        meta = 'metadata', # Can't use meta because it's an instance attribute
        tags = 'tags'
    )

    content = AceTextField(mode='ace/mode/markdown')
    metadata = AceTextField(mode='ace/mode/javascript')
    image = FileField(u'Image File')
    page_title = TextField()
    submit = SubmitField()
    preview = SubmitField()
    draft = BooleanField(default=True)
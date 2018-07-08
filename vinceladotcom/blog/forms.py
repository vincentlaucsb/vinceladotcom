from wtforms import validators, Form, BooleanField, TextAreaField, \
    TextField, SubmitField
from ..forms import AceTextField

class BlogForm(Form):
    content = AceTextField()
    page_title = TextField()
    author = TextField()
    submit = SubmitField()
    preview = SubmitField()
    draft = BooleanField(default=True)
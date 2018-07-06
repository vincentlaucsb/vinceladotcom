from wtforms import validators, Form, BooleanField, TextAreaField, \
    TextField, SubmitField

class BlogForm(Form):
    content = TextAreaField()
    page_title = TextField()
    author = TextField()
    submit = SubmitField()
    preview = SubmitField()
    draft = BooleanField(default=True)
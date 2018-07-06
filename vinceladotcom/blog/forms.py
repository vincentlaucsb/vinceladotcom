from wtforms import validators, Form, TextAreaField, TextField, SubmitField

class BlogForm(Form):
    content = TextAreaField()
    title = TextField()
    author = TextField()
    submit = SubmitField()
    preview = SubmitField()
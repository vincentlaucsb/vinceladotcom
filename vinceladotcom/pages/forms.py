from wtforms import validators, Form, TextAreaField, TextField, SubmitField

class PageForm(Form):
    content = TextAreaField()
    custom_css = TextAreaField()
    page_title = TextField()
    url = TextField()
    template = TextField()
    submit = SubmitField()
    preview = SubmitField()
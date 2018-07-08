import os

import markupsafe
from wtforms import validators, Form, BooleanField, TextAreaField, \
    TextField, SelectField, SubmitField, widgets, core
from .config import CURRENT_DIR

def get_templates():
    templates = []
    for i in os.listdir(os.path.join(CURRENT_DIR, 'templates')):
        current_file = os.path.join(CURRENT_DIR, 'templates', i)
        if (os.path.isfile(current_file)):
            templates.append(i)
            
    return templates

class AceText(widgets.TextArea):
    ''' Custom widget for my ACE text editor hack '''

    def __init__(self, *args, **kwargs):
        super(AceText, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        text_area = super(AceText, self).__call__(field, **kwargs)
        return text_area + markupsafe.Markup('''
            <div id="editor">&lt;h1&gt;Title&lt;/h1&gt;</div>
            <script src="/static/js/ace-builds/src-noconflict/ace.js" type="text/javascript" charset="utf-8"></script>
            <script>
                var editor = ace.edit("editor");
                editor.setTheme("ace/theme/monokai");
                editor.session.setMode("ace/mode/html");
                
                <!-- Hack: Swap contents of content and ACE editor -->
                var html_code = document.getElementById("content").value;
                editor.setValue(html_code);
                editor.clearSelection();
                
                editor.session.on('change', function(delta) {
                    document.getElementById("content").value = editor.getValue();
                });
            </script>
        ''')
    
class AceTextField(core.StringField):
    widget = AceText()
import datetime
import os
import json

__all__ = [
    "get_templates", "BaseForm", "AceTextField"
]

import markupsafe
from wtforms import validators, ValidationError, Form, BooleanField, TextAreaField, \
    TextField, SelectField, SubmitField, widgets, core, DateField
from .config import CURRENT_DIR

def get_templates():
    templates = []
    for i in os.listdir(os.path.join(CURRENT_DIR, 'templates')):
        current_file = os.path.join(CURRENT_DIR, 'templates', i)
        if (os.path.isfile(current_file)):
            templates.append(i)
            
    return templates

class BaseForm(Form):
    errors = []
    created = DateField(default=datetime.datetime.now())
    tags = TextField()

    def data_dict(self):
        ''' So instead of this:
        database.Page(
                    id=page.id,  # So Peewee knows we want to do an UPDATE
                    title=form.page_title.data,
                    content=form.content.data,
                    css=form.custom_css.data,
                    url=form.url.data,
                    markdown=form.markdown.data
                ).save()
                
        We can do this:
        database.Page(
            id=page.id,
            **form.data_dict()            
        ).save()
        '''
        
        temp =  { k: getattr(self, v).data for k, v in self.__class__.db_mapping.items() }
        
        # Convert datetime objects to strings
        temp['created'] = str(temp['created'])        
        return temp
    
class AceText(widgets.TextArea):
    ''' Custom widget for my ACE text editor hack '''

    def __init__(self, *args, **kwargs):
        super(AceText, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        text_area = super(AceText, self).__call__(field, **kwargs)
        return text_area + markupsafe.Markup('''
        <div id="{name}-editor-wrapper" class="editor-wrapper">
            <div class="editor-preview">
                <div id="{name}-editor" class="editor">&lt;h1&gt;Title&lt;/h1&gt;</div>
                <div id="{name}-preview-wrapper" class="preview">
                    <iframe id="{name}-preview"></iframe>
                </div>
            </div>
            <div class="editor-options">
                <nav>
                    <a id="{name}-fullscreen" class="fullscreen-trigger"></a>
                    <a id="{name}-minimize" class="minimize-trigger"></a>
                </nav>
            </div>
        </div>
        
        <script type="text/javascript">
            // Create ACE Editor
            var {name}_editor = ace.edit("{name}-editor");
            {name}_editor.setTheme("ace/theme/monokai");
            {name}_editor.session.setMode("{mode}");
            
            // Hack: Swap contents of WTForms textarea and ACE editor
            var {name}_html_code = document.getElementById("{name}").value;
            {name}_editor.setValue({name}_html_code);
            {name}_editor.clearSelection();
            
            {name}_editor.session.on('change', function(delta) {{
                document.getElementById("{name}").value = {name}_editor.getValue();
            }});

            // Create Live Preview
            var preview = LiveHTMLPreview(
                {name}_editor,
                document.getElementById("{name}-preview")
            );
            
            // Maximizer
            var maximizer = Fullscreen(
                document.getElementById("{name}-fullscreen"),
                document.getElementById("{name}-editor-wrapper")
            );
            
            // Minimizer
            var minimizer = Minimizer(
                document.getElementById("{name}-minimize"),
                document.getElementById("{name}-preview-wrapper")
            );
        </script>
        ''').format(
            name = field.name,
            mode = kwargs['mode']
        )
    
class AceTextField(core.StringField):
    widget = AceText()
    
    def __init__(self, mode="ace/mode/html", *args, **kwargs):
        kwargs['render_kw'] = {
            'mode': mode
        }
        
        super(AceTextField, self).__init__(*args, **kwargs)
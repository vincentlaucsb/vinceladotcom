''' Handles authentication '''

from . import database
from wtforms import *
import wtforms
import flask
import passlib
from passlib.hash import pbkdf2_sha256

class UserForm(wtforms.Form):
    name = TextField()
    password = PasswordField() # Should not be plaintext
    email = TextField()
    is_admin = BooleanField()
    
class LoginForm(wtforms.Form):
    name = TextField()
    password = PasswordField()
    submit = wtforms.SubmitField()
    
    def validate(self):
        try:
            user = database.Users.select().where(
                database.Users.name == self.name.data)[0]
        except IndexError:
            return False
                
        if pbkdf2_sha256.verify(
            self.password.data,
            user.password   # Hashed
        ):
            return user
        
        return None
        
def new_user(name, password, email, is_admin=False):
    database.Users(
        name=name,
        password=pbkdf2_sha256.hash(password),
        email=email,
        is_admin=is_admin
    ).save()
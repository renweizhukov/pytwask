# -*- coding: utf-8 -*-

'''
Courtesy of http://flask.pocoo.org/snippets/64/
'''

from flask_wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired

class SignInForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def check_login_credentials(self):
        '''
        Check the login credentials (username, password).
        '''
        # TODO: Check the login credentials (username, password) match 
        # the record in the backend database.
        if self.username.data == 'renwei' and self.password.data == '111111':
            return True
        else:
            return False

class PostTweetForm(Form):
    tweet = StringField('Tweet', validators=[DataRequired()])
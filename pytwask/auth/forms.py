# -*- coding: utf-8 -*-
"""
This module defines all the authentication-related forms.

Courtesy of http://flask.pocoo.org/snippets/64/
"""

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class SignInForm(FlaskForm):
    """The form for signing into an existing user."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign in')


class SignUpForm(FlaskForm):
    """The form for signing up a new user."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class ChangePasswordForm(FlaskForm):
    """The form for changing the user password."""
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', 
                                 validators=[
                                     DataRequired(),
                                     EqualTo('new_password2', 
                                             message='New passwords must match')])
    new_password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Submit')
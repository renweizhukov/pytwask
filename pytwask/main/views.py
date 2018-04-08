# -*- coding: utf-8 -*-
"""This module defines all the main views."""

from flask import render_template, redirect, url_for

from . import main
from .. import login_manager
from ..models import User


@login_manager.user_loader
def load_user(session_token):
    """This function is required by flask_login to get 
    the 'User' instance from the session token.
    
    Parameters
    ----------
    session_token: str
    
    Returns
    -------
    A 'User' instance if the session token is valid; 
    None otherwise.
    """
    return User.get(session_token)


@main.route('/')
def index():
    """This view renders the main index page. 
    
    Since the main index page has the login form, so it is 
    redirected to the auth Blueprint right away.
    """
    return redirect(url_for('auth.index'))


@main.app_errorhandler(400)
def bad_request(e):
    """This view handles the 400 error."""
    return render_template('400.html'), 400


@main.app_errorhandler(403)
def forbidden(e):
    """This view handles the 403 error."""
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    """This view handles the 404 error."""
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    """This view handles the 500 error."""
    return render_template('500.html'), 500  
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for

from . import main
from .. import login_manager
from ..models import User


@login_manager.user_loader
def load_user(session_token):
    return User.get(session_token)


# The main index page has the login form, so it is 
# redirected to the auth Blueprint right away.
@main.route('/')
def index():
    return redirect(url_for('auth.index'))


@main.app_errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500  
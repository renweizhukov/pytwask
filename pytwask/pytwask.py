#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

from forms import PostTweetForm, SignInForm, SignUpForm, ChangePasswordForm

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'index'

# Enable debugtoolbar
toolbar = DebugToolbarExtension()

# For displaying timestamps
moment = Moment()

app = Flask(__name__)
app.config['SECRET_KEY'] = b'c\x04\x14\x00;\xe44 \xf4\xf3-_9B\x1d\x15u\x02g\x1a\xcc\xd8\x04~'
# Change the duration of how long the Remember Cookie is valid on the users computer. 
# This can not really be trusted as a user can edit it. 
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(days=7)

login_manager.init_app(app)
moment.init_app(app)
toolbar.init_app(app)

from models import Tweet, User

@login_manager.user_loader
def load_user(session_token):
    return User.get(session_token)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.get_by_username_and_password(form.username.data, form.password.data)
        if user is not None:
            login_user(user, form.remember_me.data)
            return redirect(url_for('user_timeline', username=user.username, tweets=user.get_user_timeline()))
        else:
            flash("Invalid username or password")

    return render_template('index.html', form=form)


@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/general_timeline')
def general_timeline():
    return render_template('timeline.html', tweets=Tweet.get_general_timeline())


@app.route('/user_timeline', methods=['GET', 'POST'])
@login_required
def user_timeline(username=None):
    form = PostTweetForm()
    if form.validate_on_submit():
        try:
            current_user.post_tweet(form.tweet.data)
            flash('Tweet successfully posted')
        except ValueError as e:
            flash(str(e))
            return render_template('timeline.html', 
                                   username=current_user.username, 
                                   tweets=current_user.get_user_timeline(), 
                                   form=form)
    
    return render_template('timeline.html', 
                           username=current_user.username, 
                           tweets=current_user.get_user_timeline(), 
                           form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            User.create_new_user(form.username.data, form.password.data)
            flash('Welcome, {}! Please login'.format(form.username.data))
            return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e))
            return render_template('signup.html', form=form)
        
    return render_template('signup.html', form=form)


@app.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            current_user.change_password(form.old_password.data, form.new_password.data)
            flash('Password successfully changed')
        except ValueError as e:
            flash(str(e))
            return render_template('user_settings.html', 
                                   followings=current_user.get_followings(), 
                                   followers=current_user.get_followers(),
                                   form=form)
            
    return render_template('user_settings.html', 
                           followings=current_user.get_followings(), 
                           followers=current_user.get_followers(),
                           form=form)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500  


if __name__ == '__main__':
    app.run(debug=True)
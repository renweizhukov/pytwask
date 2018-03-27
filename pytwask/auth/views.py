from flask import flash, redirect, render_template, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import SignInForm, SignUpForm, ChangePasswordForm
from ..models import User

@auth.route('/', methods=['GET', 'POST'])
def index():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.get_by_username_and_password(form.username.data, form.password.data)
        if user is not None:
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('tweets.user_timeline'))
        else:
            flash("Invalid username or password")

    return render_template('index.html', form=form)


@auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            User.create_new_user(form.username.data, form.password.data)
            flash('Welcome, {}! Please login'.format(form.username.data))
            return redirect(url_for('auth.index'))
        except ValueError as e:
            flash(str(e))
            return render_template('signup.html', form=form)
        
    return render_template('signup.html', form=form)


@auth.route('/user_settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            current_user.change_password(form.old_password.data, form.new_password.data)
            flash('Password successfully changed')
        except ValueError as e:
            flash(str(e))
            return render_template('user_settings.html', form=form)
            
    return render_template('user_settings.html', form=form)
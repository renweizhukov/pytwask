from urllib.parse import urlparse, urljoin
from flask import flash, redirect, render_template, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user

from . import auth
from .forms import SignInForm, SignUpForm, ChangePasswordForm
from ..models import User

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@auth.route('/', methods=['GET', 'POST'])
def index():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.get_by_username_and_password(form.username.data, form.password.data)
        if user is not None:
            login_user(user, form.remember_me.data)
            
            flash('Logged in successfully.')
            
            next_url = request.args.get('next')
            if not is_safe_url(next_url):
                return abort(400)
            
            return redirect(next_url or url_for('tweets.user_timeline'))
        else:
            flash("Invalid username or password")

    return render_template('index.html', form=form)


@auth.route('/signout')
def signout():
    logout_user()
    flash('Logged out successfully.')
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
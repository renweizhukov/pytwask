# -*- coding: utf-8 -*-

from flask import flash, render_template
from flask_login import login_required, current_user

from . import tweets
from .forms import PostTweetForm
from ..models import Tweet


@tweets.route('/general_timeline')
def general_timeline():
    return render_template('timeline.html', general=True)


@tweets.route('/user_timeline', methods=['GET', 'POST'])
@login_required
def user_timeline(username=None):
    form = PostTweetForm()
    if form.validate_on_submit():
        try:
            current_user.post_tweet(form.tweet.data)
            flash('Tweet successfully posted')
        except ValueError as e:
            flash(str(e))
            return render_template('timeline.html', general=False, form=form)
    
    return render_template('timeline.html', general=False, form=form)
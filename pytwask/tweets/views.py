# -*- coding: utf-8 -*-
"""This module defines all the tweet-related views."""

from flask import flash, render_template
from flask_login import login_required, current_user

from . import tweets
from .forms import PostTweetForm, FollowForm, UnfollowForm
from ..models import Tweet


@tweets.route('/general_timeline')
def general_timeline():
    """This view renders the general timeline."""
    return render_template('timeline.html', general=True, show_username=True)


@tweets.route('/user_timeline', methods=['GET', 'POST'])
@login_required
def user_timeline(username=None):
    """This view renders the user timeline. 
    It also allows the user to post tweets.
    """
    form = PostTweetForm()
    if form.validate_on_submit():
        try:
            current_user.post_tweet(form.tweet.data)
            flash('Tweet successfully posted')
        except ValueError as e:
            flash(str(e))
            return render_template('timeline.html', 
                                   general=False, 
                                   show_username=True, 
                                   form=form)
    
    return render_template('timeline.html', 
                           general=False, 
                           show_username=True,
                           form=form)


@tweets.route('/user_history/<username>')
def user_history(username):
    """This view renders the user history. It will 
    
    - display all the tweets posted by this user;
    - allow the logged-in user to follow/unfollow this user if they are different.
    """
    follow_form = FollowForm()
    unfollow_form = UnfollowForm()
    return render_template('user_history.html', 
                           username=username,
                           follow_form=follow_form, 
                           unfollow_form=unfollow_form)


@tweets.route('/follow/<username>', methods=['POST'])
def follow(username):
    """This view handles the follow form in the user history page."""
    follow_form = FollowForm()
    unfollow_form = UnfollowForm()
    
    if follow_form.validate_on_submit():
        try:
            current_user.follow(username)
            flash('Followed {}'.format(username))
        except ValueError as e:
            flash(str(e))
            return render_template('user_history.html',
                                   username=username,
                                   follow_form=follow_form,
                                   unfollow_form=unfollow_form)
    
    return render_template('user_history.html',
                           username=username,
                           follow_form=follow_form,
                           unfollow_form=unfollow_form)


@tweets.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    """This view handles the unfollow form in the user history page."""
    follow_form = FollowForm()
    unfollow_form = UnfollowForm()
    
    if unfollow_form.validate_on_submit():
        try:
            current_user.unfollow(username)
            flash('Unfollowed {}'.format(username))
        except ValueError as e:
            flash(str(e))
            return render_template('user_history.html',
                                   username=username,
                                   follow_form=follow_form,
                                   unfollow_form=unfollow_form)
    
    return render_template('user_history.html',
                           username=username,
                           follow_form=follow_form,
                           unfollow_form=unfollow_form)


@tweets.app_context_processor
def inject_general_timeline():
    """This function injects the function object 'Tweet.get_general_timeline' 
    into the application context so that 'get_general_timeline' can be accessed 
    in Jinja2 templates.
    """
    return dict(get_general_timeline=Tweet.get_general_timeline)
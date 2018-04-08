# -*- coding: utf-8 -*-
"""
This module defines all the tweet-related forms.

Courtesy of http://flask.pocoo.org/snippets/64/
"""

from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostTweetForm(FlaskForm):
    """The form for posting a tweet."""
    tweet = TextAreaField('', 
                          render_kw={"rows": 10, "cols": 30}, 
                          validators=[DataRequired()])
    submit = SubmitField('Post')
    
class FollowForm(FlaskForm):
    """The form for following a user."""
    submit = SubmitField('Follow')

class UnfollowForm(FlaskForm):
    """The form for unfollowing a user."""
    submit = SubmitField('Unfollow')
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostTweetForm(FlaskForm):
    tweet = TextAreaField('', 
                          render_kw={"rows": 10, "cols": 30}, 
                          validators=[DataRequired()])
    submit = SubmitField('Post')
    
class FollowForm(FlaskForm):
    submit = SubmitField('Follow')

class UnfollowForm(FlaskForm):
    submit = SubmitField('Unfollow')
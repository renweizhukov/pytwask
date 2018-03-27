# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired


class PostTweetForm(FlaskForm):
    tweet = StringField('Tweet', validators=[DataRequired()])
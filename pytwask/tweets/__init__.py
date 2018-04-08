# -*- coding: utf-8 -*-
"""The blueprint which contains all the tweet-related views."""

from flask import Blueprint

tweets = Blueprint('tweets', __name__)

from . import views
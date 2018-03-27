# -*- coding: utf-8 -*-

from flask import Blueprint

tweets = Blueprint('tweets', __name__)

from . import views
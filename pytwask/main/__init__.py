# -*- coding: utf-8 -*-
"""The blueprint which contains all the main views."""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
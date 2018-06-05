# -*- coding: utf-8 -*-
"""The blueprint which contains all the views related to authentication."""

from flask import Blueprint

auth = Blueprint('auth', __name__)  # pylint: disable=invalid-name

from . import views  # pylint: disable=wrong-import-position

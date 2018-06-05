# -*- coding: utf-8 -*-
"""The blueprint which contains all the main views."""

from flask import Blueprint

main = Blueprint('main', __name__)  # pylint: disable=invalid-name

from . import views  # pylint: disable=wrong-import-position

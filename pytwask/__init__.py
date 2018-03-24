# -*- coding: utf-8 -*-

import datetime

from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'index'

# Enable debugtoolbar
toolbar = DebugToolbarExtension()

# For displaying timestamps
moment = Moment()

app = Flask(__name__)
app.config['SECRET_KEY'] = b'c\x04\x14\x00;\xe44 \xf4\xf3-_9B\x1d\x15u\x02g\x1a\xcc\xd8\x04~'
# Change the duration of how long the Remember Cookie is valid on the users computer. 
# This can not really be trusted as a user can edit it. 
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(days=7)
# Need to set 'DEBUG` to True, otherwise the debug toolbar won't be shown.
app.config['DEBUG'] = True

login_manager.init_app(app)
toolbar.init_app(app)
moment.init_app(app)

from pytwask import views
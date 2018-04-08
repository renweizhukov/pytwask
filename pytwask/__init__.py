# -*- coding: utf-8 -*-
"""Package pytwask"""

import datetime

from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

from .config import config_by_name

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.index'

# Enable debugtoolbar
toolbar = DebugToolbarExtension()

# For displaying timestamps
moment = Moment()

def create_app(config_name):
    """Create and initialize the Flask application. 
    
    Here we follow the Flask typical pattern of "Application Factories". 
    For details, please refer to: 
    
    http://flask.pocoo.org/docs/0.12/patterns/appfactories/
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    login_manager.init_app(app)
    toolbar.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .tweets import tweets as tweets_blueprint
    app.register_blueprint(tweets_blueprint, url_prefix='/tweets')
    
    return app
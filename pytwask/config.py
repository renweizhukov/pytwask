# -*- coding: utf-8 -*-

import datetime
import os

class Config:
    # TODO: Use Unix domain socket to connect to the local Redis database
    REDIS_DB_HOSTNAME = os.getenv('REDIS_DB_HOSTNAME', '127.0.0.1')
    REDIS_DB_PORT = int(os.getenv('REDIS_DB_PORT', '6379'))
    REDIS_DB_INDEX = int(os.getenv('REDIS_DB_INDEX', '0'))
    REDIS_DB_PASSWORD = os.getenv('REDIS_DB_PASSWORD', '')
    SECRET_KEY = b'c\x04\x14\x00;\xe44 \xf4\xf3-_9B\x1d\x15u\x02g\x1a\xcc\xd8\x04~'
    # Change the duration of how long the Remember Cookie is valid on the users computer. 
    # This can not really be trusted as a user can edit it. 
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=7)
    DEBUG = False
    
class DevelopmentConfig(Config):
    REDIS_DB_INDEX = 1
    # Need to set 'DEBUG` to True, otherwise the debug toolbar won't be shown.
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
    REDIS_DB_INDEX = 15
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'
    
class ProductionConfig(Config):
    pass
    
config_by_name = dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProductionConfig,
)
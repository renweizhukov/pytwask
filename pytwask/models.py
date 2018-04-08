# -*- coding: utf-8 -*-
"""This module defines the two data models 'Tweet' and 'User' which 
are used by views and templates.
"""

import datetime
from flask_login import UserMixin
from flask.config import Config
#from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import os

from pytwis import Pytwis, PytwisConstant

from .config import config_by_name

# BUGBUG: Read the configuration of the Flask app again since we can't 
# find a way to access the configuration outside an application context.
config_name = os.getenv('PYTWASK_ENV', 'dev')
app_config = Config(None)
app_config.from_object(config_by_name[config_name])

# Connect to the local Redis database.
twis = Pytwis(hostname=app_config['REDIS_DB_HOSTNAME'], 
              port=app_config['REDIS_DB_PORT'], 
              socket=app_config['REDIS_DB_SOCKET'],
              db=app_config['REDIS_DB_INDEX'], 
              password =app_config['REDIS_DB_PASSWORD'])

class Tweet():
    """This 'Tweet' class encapsulates all the information related to one tweet.
    
    Note that it will convert the posted UNIX timestamp into a datetime.
    """
    def __init__(self, username, post_unix_time, body):
        self.username = username
        self.post_datetime = datetime.datetime.fromtimestamp(post_unix_time)
        self.body = body
        
    @staticmethod
    def get_general_timeline():
        """Get the general timeline.
        Since the general timeline doesn't belong to any user, it is defined 
        as a static method of the 'Tweet' class.
        
        Returns
        -------
        A list of 'Tweet' instances.
        """
        succeeded, result = twis.get_timeline('', -1)
        if succeeded:
            return [Tweet(tweet[PytwisConstant.USERNAME_KEY], 
                          int(tweet[PytwisConstant.TWEET_UNIXTIME_KEY]), 
                          tweet[PytwisConstant.TWEET_BODY_KEY]) 
                    for tweet in result[PytwisConstant.TWEETS_KEY]]
        else:
            print('Failed to get the general timeline with error = {}'.\
                  format(result[PytwisConstant.ERROR_KEY]))
            return []

# Login_serializer used to encryt and decrypt the cookie token for the remember
# me option of flask-login
login_serializer = URLSafeTimedSerializer(app_config['SECRET_KEY'])

class User(UserMixin):
    """This 'User' class is mainly used by flask-login to manage the user authentication. 
    It can also be used to retrieve and modify user-specific data, e.g., getting user timeline, 
    changing user password.
    """
    def __init__(self, username, auth_secret, session_token):
        self.username = username
        self.auth_secret = auth_secret
        self.session_token = session_token
        
    def get_id(self):
        """Get the user ID which is the session token in our case."""
        return str(self.session_token)

    def change_password(self, old_password, new_password):
        """Change the user password.
        
        Parameters
        ----------
        old_password: str
            The old password
        new_password: str
            The new password
        
        Raises
        ------
        ValueError
            If failed to change the password.
        """
        succeeded, result = twis.change_password(self.auth_secret, old_password, new_password)
        if not succeeded:
            raise ValueError("Couldn't change the password with error = {}".\
                             format(result[PytwisConstant.ERROR_KEY]))
    
    def get_user_tweets(self, username):
        """Get the tweets posted by a given user.
        
        Parameters
        ----------
        username: str
        
        Returns
        -------
        A list of 'Tweet' instances.
        """
        succeeded, result = twis.get_user_tweets(self.auth_secret, username, -1)
        if succeeded:
            return [Tweet(tweet[PytwisConstant.USERNAME_KEY], 
                          int(tweet[PytwisConstant.TWEET_UNIXTIME_KEY]), 
                          tweet[PytwisConstant.TWEET_BODY_KEY]) 
                    for tweet in result[PytwisConstant.TWEETS_KEY]]
        else:
            print('Failed to get the tweets posted by {} with error = {}'.\
                  format(username, result[PytwisConstant.ERROR_KEY]))
            return []
        
    def get_user_timeline(self):
        """Get the user timeline.
        
        Returns
        -------
        A list of 'Tweet' instances.
        """
        succeeded, result = twis.get_timeline(self.auth_secret, -1)
        if succeeded:
            return [Tweet(tweet[PytwisConstant.USERNAME_KEY], 
                          int(tweet[PytwisConstant.TWEET_UNIXTIME_KEY]), 
                          tweet[PytwisConstant.TWEET_BODY_KEY]) 
                    for tweet in result[PytwisConstant.TWEETS_KEY]]
        else:
            print('Failed to get the timeline of {} with error = {}'.\
                  format(self.username, result[PytwisConstant.ERROR_KEY]))
            return []
        
    def post_tweet(self, body):
        """Post a tweet.
        
        Parameters
        ----------
        body: str
            The tweet body that will be posted.
            
        Raises
        ------
        ValueError
            If failed to post the tweet.
        """
        succeeded, result = twis.post_tweet(self.auth_secret, body)
        if not succeeded:
            raise ValueError("Couldn't post the tweet with error = {}".\
                             format(result[PytwisConstant.ERROR_KEY]))
        
    def follow(self, followee_username):
        """Follow another user by his/her username.
        
        Parameters
        ----------
        followee_username: str
        
        Raises
        ------
        ValueError
            If failed to follow the user
        """
        succeeded, result = twis.follow(self.auth_secret, followee_username)
        if not succeeded:
            raise ValueError("Couldn't follow {} with error = {}".\
                             format(result[PytwisConstant.ERROR_KEY]))
        
    def unfollow(self, followee_username):
        """Unfollow another user by his/her username.
        
        Parameters
        ----------
        followee_username: str
        
        Raises
        ------
        ValueError
            If failed to unfollow the user.
        """
        succeeded, result = twis.unfollow(self.auth_secret, followee_username)
        if not succeeded:
            raise ValueError("Couldn't unfollow {} with error = {}".\
                             format(result[PytwisConstant.ERROR_KEY]))
    
    def get_followings(self):
        """Get the following list.
        
        Returns
        -------
        A set of the usernames of the followings.
        """
        succeeded, result = twis.get_following(self.auth_secret)
        if succeeded:
            # Create a set from the returned list to speed up search later.
            return set(result[PytwisConstant.FOLLOWING_LIST_KEY])
        else:
            print('Failed to get the following list of {} with error = {}'.\
                  format(self.username, result[PytwisConstant.ERROR_KEY]))
            return set()
        
    def get_followers(self):
        """Get the follower list.
        
        Returns
        -------
        A set of the usernames of the followers.
        """
        succeeded, result = twis.get_followers(self.auth_secret)
        if succeeded:
            # Create a set from the returned list to speed up search later.
            return set(result[PytwisConstant.FOLLOWER_LIST_KEY])
        else:
            print('Failed to get the follower list of {} with error = {}'.\
                  format(self.username, result[PytwisConstant.ERROR_KEY]))
            return set()
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    @staticmethod
    def get(session_token):
        """
        Get a 'User' instance from the session token.
        
        Parameters
        ----------
        session_token: str
        
        Returns
        -------
        A 'User' instance if session_token exists; otherwise None.
        """
        max_age = app_config["REMEMBER_COOKIE_DURATION"].total_seconds()
        try:
            data = login_serializer.loads(session_token, max_age=max_age)
        except (BadSignature, SignatureExpired) as e:
            print('Failed to load the session token with error = {}'.format(str(e)))
            return None
        
        auth_secret = data[0]
        succeeded, result = twis.get_user_profile(auth_secret)
        if succeeded:
            return User(result[PytwisConstant.USERNAME_KEY], auth_secret, session_token)
        else:
            return None
        
    @staticmethod
    def get_by_username_and_password(username, password):
        """
        Get a 'User' instance from the username and the password.
        
        Parameters
        ----------
        username: str
        password: str
        
        Returns
        -------
        A 'User' instance if username and password are correct; otherwise None.
        """
        succeeded, result = twis.login(username, password)
        if succeeded:
            session_token = login_serializer.dumps([result[PytwisConstant.AUTH_KEY]])
            return User(username, result[PytwisConstant.AUTH_KEY], session_token)
        else:
            print('Failed to create a user instance with error ={}'.\
                  format(result[PytwisConstant.ERROR_KEY]))
            return None
    
    @staticmethod
    def create_new_user(username, password):
        """
        Create a new user with the given username and password.
        
        Parameters
        ----------
        username: str
        password: str
        
        Raises
        ------
        ValueError
            If failed to create the new user.
        """
        succeeded, result = twis.register(username, password)
        if not succeeded:
            raise ValueError("Can't create new user with error {}".\
                             format(result[PytwisConstant.ERROR_KEY]))
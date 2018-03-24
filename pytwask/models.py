# -*- coding: utf-8 -*-

from flask_login import UserMixin
#from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import datetime
from datetime import datetime as dt

from pytwis import Pytwis

# Connect to the local Redis database.
twis = Pytwis()

class Tweet():
    """Tweet class"""
    def __init__(self, username, post_time, body):
        self.username = username
        self.post_time = post_time
        self.body = body
        
    @staticmethod
    def get_general_timeline():
        succeeded, result = twis.get_timeline('', -1)
        if succeeded:
            return [Tweet(tweet['username'], 
                          dt.fromtimestamp(int(tweet['unix_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                          tweet['body']) for tweet in result['tweets']]
        else:
            print('Failed to get the general timeline with error = {}'.format(result['error']))
            return []

# Login_serializer used to encryt and decrypt the cookie token for the remember
# me option of flask-login
# BUGBUG: Can't use app.config['SECRET_KEY'] due to circular import.
login_serializer = URLSafeTimedSerializer(b'c\x04\x14\x00;\xe44 \xf4\xf3-_9B\x1d\x15u\x02g\x1a\xcc\xd8\x04~')

class User(UserMixin):
    """User class for flask-login"""
    def __init__(self, username, password, auth_secret, session_token):
        self.username = username
        self.password = password
        self.auth_secret = auth_secret
        self.session_token = session_token
        
    def get_id(self):
        return str(self.session_token)
    
    def change_password(self, old_password, new_password):
        """Change the password."""
        succeeded, result = twis.change_password(self.auth_secret, old_password, new_password)
        if not succeeded:
            raise ValueError("Couldn't change the password with error = {}".format(result['error']))
    
    def get_user_tweets(self):
        """Get the tweets posted by this user."""
        succeeded, result = twis.get_user_tweets(self.auth_secret, self.username, -1)
        if succeeded:
            return [Tweet(tweet['username'], 
                          dt.fromtimestamp(int(tweet['unix_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                          tweet['body']) for tweet in result['tweets']]
        else:
            print('Failed to get the tweets posted by {} with error = {}'.format(self.username, result['error']))
            return []
        
    def get_user_timeline(self):
        """Get the user timeline."""
        succeeded, result = twis.get_timeline(self.auth_secret, -1)
        if succeeded:
            return [Tweet(tweet['username'], 
                          dt.fromtimestamp(int(tweet['unix_time'])).strftime('%Y-%m-%d %H:%M:%S'),
                          tweet['body']) for tweet in result['tweets']]
        else:
            print('Failed to get the timeline of {} with error = {}'.format(self.username, result['error']))
            return []
        
    def get_general_timeline(self):
        """Get the general timeline."""
        return Tweet.get_general_timeline()
        
    def post_tweet(self, body):
        """Post a tweet."""
        succeeded, result = twis.post_tweet(self.auth_secret, body)
        if not succeeded:
            raise ValueError("Couldn't post the tweet with error = {}".format(result['error']))
    
    def get_followings(self):
        """Get the following list."""
        succeeded, result = twis.get_following(self.auth_secret)
        if succeeded:
            return result['following_list']
        else:
            print('Failed to get the following list of {} with error = {}'.format(self.username, result['error']))
            return []
        
    def get_followers(self):
        """Get the follower list."""
        succeeded, result = twis.get_followers(self.auth_secret)
        if succeeded:
            return result['follower_list']
        else:
            print('Failed to get the follower list of {} with error = {}'.format(self.username, result['error']))
            return []
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    @staticmethod
    def get(session_token):
        """Return a User instance if session_token exists; otherwise return None."""
        # BUGBUG: Can't use app.config["REMEMBER_COOKIE_DURATION"] due to circular import.
        max_age = datetime.timedelta(days=7).total_seconds()
        try:
            data = login_serializer.loads(session_token, max_age=max_age)
        except (BadSignature, SignatureExpired) as e:
            print('Failed to load the session token with error = {}'.format(str(e)))
            return None
        
        auth_secret = data[0]
        succeeded, result = twis.get_user_profile(auth_secret)
        if succeeded:
            return User(result['username'], result['password'], auth_secret, session_token)
        else:
            return None
        
    @staticmethod
    def get_by_username_and_password(username, password):
        """Return a User instance if username and password are correct; 
        otherwise return None.
        """
        # BUGBUG: Verify the hash of the salted password.
        succeeded, result = twis.login(username, password)
        if succeeded:
            session_token = login_serializer.dumps([result['auth']])
            return User(username, password, result['auth'], session_token)
        else:
            print('Failed to create a user instance with error ={}'.format(result['error']))
            return None
    
    @staticmethod
    def create_new_user(username, password):
        # BUGBUG: Store the hash of the salted password
        succeeded, result = twis.register(username, password)
        if not succeeded:
            raise ValueError("Can't create new user with error {}".format(result['error']))
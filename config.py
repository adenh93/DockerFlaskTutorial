import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object): 
    POSTS_PER_PAGE = 15
    RECAPTCHA_PUBLIC_KEY = "6LesqJwUAAAAAHwYA5459Zxsj373s80Fo7b9V7YW"
    RECAPTCHA_PRIVATE_KEY = "6LesqJwUAAAAANWhDTxkIOBFmbp9ytEB3Qd1qYrz"
    
    TWITTER_API_KEY = "XXX"
    TWITTER_API_SECRET = "XXXX"
    FACEBOOK_CLIENT_ID = "YYY"
    FACEBOOK_CLIENT_SECRET = "YYYY"

class ProdConfig(Config): 
    pass 


class DevConfig(Config): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'temp/TestDatabase.db')
    SECRET_KEY = '\x17\xa5\xe8\xb7)\xde\xcd4\x9fQ\xe9\x8c\x11VT\x7f\x80\xab\xab1\xea\x1f\x17\xa1'
    CELERY_BROKER_URL = "redis://password@localhost/0" 
    CELERY_RESULT_BACKEND = "redis://password@localhost/0"

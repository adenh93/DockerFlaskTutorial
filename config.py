class Config(object): 
    pass 
 
class ProdConfig(Config): 
    pass 
 
class DevConfig(Config): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///temp/TestDatabase.db"
    SECRET_KEY = '\x17\xa5\xe8\xb7)\xde\xcd4\x9fQ\xe9\x8c\x11VT\x7f\x80\xab\xab1\xea\x1f\x17\xa1'
import os 
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    ORACLE_DB_PASSWORD=os.environ.get("ORACLE_DB_USER_PASSWORD")
    ORACLE_DB_USERNAME=os.environ.get("ORACLE_DB_USERNAME")
    ORACLE_DB_DSN=os.environ.get("ORACLE_DB_DSN")
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    'sqlite://'
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}
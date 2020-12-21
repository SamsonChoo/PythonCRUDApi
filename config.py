import os


class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'IHateThisFluPandemic'


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    FLASK_DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    FLASK_DEBUG = False
    SQLALCHEMY_ECHO = False


class TestConfig(Config):
    """
    Testing configurations
    """

    TESTING = True
    FLASK_DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_TEST')
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}
